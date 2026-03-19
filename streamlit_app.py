"""
MSA Article Stock Analysis - Streamlit Web Application
File Upload & Processing Interface with Download Options
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO
import zipfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="MSA Article Stock Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_resource
def get_encoding_list():
    """List of encodings to try"""
    return ['utf-8', 'utf-16', 'latin-1', 'cp1252', 'iso-8859-1', 'windows-1252', 'ascii']


def try_read_csv(file_obj, encoding_list=None):
    """Try reading CSV with multiple encodings"""
    if encoding_list is None:
        encoding_list = get_encoding_list()
    
    for encoding in encoding_list:
        try:
            df = pd.read_csv(file_obj, encoding=encoding)
            return df, encoding
        except Exception:
            continue
    
    return None, None


def try_read_excel(file_obj):
    """Try reading Excel file"""
    try:
        df = pd.read_excel(file_obj)
        return df
    except Exception as e:
        return None


def validate_uploaded_files(uploaded_files):
    """Validate that all required files are uploaded and readable"""
    validation_results = {
        'valid': True,
        'messages': [],
        'files': {}
    }
    
    # Check required files
    if 'msa_file' not in uploaded_files or uploaded_files['msa_file'] is None:
        validation_results['valid'] = False
        validation_results['messages'].append("❌ MSA Article File is required")
    else:
        msa_file = uploaded_files['msa_file']
        msa_df, encoding = try_read_csv(msa_file)
        if msa_df is None:
            validation_results['valid'] = False
            validation_results['messages'].append(f"❌ Could not read MSA file (encoding issue)")
        else:
            validation_results['files']['msa'] = msa_df
            validation_results['messages'].append(f"✅ MSA file loaded: {len(msa_df):,} rows, {len(msa_df.columns)} columns")
    
    if 'store_file' not in uploaded_files or uploaded_files['store_file'] is None:
        validation_results['valid'] = False
        validation_results['messages'].append("❌ Store Name File is required")
    else:
        store_file = uploaded_files['store_file']
        store_df = try_read_excel(store_file)
        if store_df is None:
            validation_results['valid'] = False
            validation_results['messages'].append(f"❌ Could not read Store file")
        else:
            validation_results['files']['store'] = store_df
            validation_results['messages'].append(f"✅ Store file loaded: {len(store_df):,} rows, {len(store_df.columns)} columns")
    
    # Check BASE DATA files
    base_data_files = uploaded_files.get('base_data_files', {})
    if not base_data_files:
        validation_results['messages'].append("⚠️  No BASE DATA files uploaded (processing will continue without them)")
    else:
        base_data = {}
        for cat, file_obj in base_data_files.items():
            df, encoding = try_read_csv(file_obj)
            if df is not None:
                base_data[cat] = df
                validation_results['messages'].append(f"✅ BASE-DATA-{cat} loaded: {len(df):,} rows")
            else:
                validation_results['messages'].append(f"⚠️  Could not read BASE-DATA-{cat}")
        validation_results['files']['base_data'] = base_data
    
    # Check LIST DATA files
    list_data_files = uploaded_files.get('list_data_files', {})
    if not list_data_files:
        validation_results['messages'].append("⚠️  No LIST DATA files uploaded (processing will continue without them)")
    else:
        list_data = {}
        for cat, file_obj in list_data_files.items():
            df, encoding = try_read_csv(file_obj)
            if df is not None:
                list_data[cat] = df
                validation_results['messages'].append(f"✅ LIST-{cat} loaded: {len(df):,} rows")
            else:
                validation_results['messages'].append(f"⚠️  Could not read LIST-{cat}")
        validation_results['files']['list_data'] = list_data
    
    return validation_results


def process_data(files, filter_threshold=50):
    """Main data processing pipeline"""
    
    processing_steps = []
    
    try:
        # STEP 1: Load data
        processing_steps.append("Loading data...")
        msa_df = files['msa']
        store_df = files['store']
        base_data = files.get('base_data', {})
        list_data = files.get('list_data', {})
        
        processing_steps.append(f"✅ Loaded: {len(msa_df):,} articles, {len(store_df):,} stores")
        
        # STEP 2: Filter data
        processing_steps.append(f"Filtering articles with STK_QTY >= {filter_threshold}...")
        if 'STK_QTY' in msa_df.columns:
            filtered_df = msa_df[msa_df['STK_QTY'] >= filter_threshold].copy()
        else:
            filtered_df = msa_df.copy()
        
        processing_steps.append(f"✅ After filter: {len(filtered_df):,} rows ({100*len(filtered_df)/len(msa_df):.1f}%)")
        
        # STEP 3: Expand by stores
        processing_steps.append(f"Expanding across {len(store_df)} stores (this may take a moment)...")
        filtered_df['_merge_key'] = 1
        store_df_copy = store_df.copy()
        store_df_copy['_merge_key'] = 1
        
        expanded_df = filtered_df.merge(store_df_copy, on='_merge_key', how='left')
        expanded_df = expanded_df.drop('_merge_key', axis=1)
        
        # Rename store columns
        store_cols = store_df.columns.tolist()
        rename_dict = {col: f'STORE_{col}' for col in store_cols}
        expanded_df = expanded_df.rename(columns=rename_dict)
        
        processing_steps.append(f"✅ Expanded to: {len(expanded_df):,} rows (cartesian product)")
        
        # STEP 4: Merge BASE DATA
        if base_data:
            processing_steps.append("Merging BASE DATA...")
            result_df = merge_base_data(expanded_df, base_data)
            processing_steps.append(f"✅ BASE DATA merged: {len(result_df):,} rows")
        else:
            result_df = expanded_df.copy()
            processing_steps.append("⚠️  Skipping BASE DATA merge (no files provided)")
        
        # STEP 5: Merge LIST DATA
        if list_data:
            processing_steps.append("Merging LIST DATA...")
            result_df = merge_list_data(result_df, list_data)
            processing_steps.append(f"✅ LIST DATA merged: {len(result_df):,} rows")
        else:
            processing_steps.append("⚠️  Skipping LIST DATA merge (no files provided)")
        
        # STEP 6: Consolidate
        processing_steps.append("Consolidating columns...")
        result_df = consolidate_columns(result_df)
        result_df = remove_duplicates_and_clean(result_df)
        processing_steps.append(f"✅ Consolidation complete: {len(result_df):,} rows, {len(result_df.columns)} columns")
        
        # STEP 7: Generate summary
        processing_steps.append("Generating summary...")
        summary = generate_summary(result_df, msa_df)
        processing_steps.append("✅ Summary generated")
        
        return {
            'success': True,
            'data': result_df,
            'steps': processing_steps,
            'summary': summary,
            'row_count': len(result_df),
            'col_count': len(result_df.columns)
        }
    
    except Exception as e:
        processing_steps.append(f"❌ ERROR: {str(e)}")
        return {
            'success': False,
            'steps': processing_steps,
            'error': str(e)
        }


def merge_base_data(expanded_df, base_data):
    """Merge BASE DATA files"""
    result_df = expanded_df.copy()
    
    for cat, base_df in base_data.items():
        base_df = base_df.copy()
        
        # Rename columns for merging
        if 'MAJCAT' in base_df.columns:
            base_df = base_df.rename(columns={'MAJCAT': 'MAJ_CAT'})
        if 'GEN_ART' in base_df.columns:
            base_df = base_df.rename(columns={'GEN_ART': 'GEN_ART_NUMBER'})
        if 'Store_Code' in base_df.columns:
            base_df = base_df.rename(columns={'Store_Code': 'STORE_ST_CD'})
        
        # Convert merge keys to string
        for key in ['MAJ_CAT', 'GEN_ART_NUMBER', 'STORE_ST_CD']:
            if key in result_df.columns:
                result_df[key] = result_df[key].astype(str)
            if key in base_df.columns:
                base_df[key] = base_df[key].astype(str)
        
        # Merge keys
        merge_keys = ['MAJ_CAT', 'GEN_ART_NUMBER', 'STORE_ST_CD']
        valid_keys = [k for k in merge_keys if k in result_df.columns and k in base_df.columns]
        
        if len(valid_keys) > 0:
            for col in base_df.columns:
                if col not in valid_keys:
                    base_df = base_df.rename(columns={col: f'{col}_BASE_{cat}'})
            
            result_df = result_df.merge(base_df, on=valid_keys, how='left')
    
    return result_df


def merge_list_data(expanded_df, list_data):
    """Merge LIST DATA files"""
    result_df = expanded_df.copy()
    
    for cat, list_df in list_data.items():
        list_df = list_df.copy()
        
        # Rename columns for merging
        if 'MAJCAT' in list_df.columns:
            list_df = list_df.rename(columns={'MAJCAT': 'MAJ_CAT'})
        if 'GEN_ART' in list_df.columns:
            list_df = list_df.rename(columns={'GEN_ART': 'GEN_ART_NUMBER'})
        if 'ST_CD' in list_df.columns:
            list_df = list_df.rename(columns={'ST_CD': 'STORE_ST_CD'})
        
        # Convert merge keys to string
        for key in ['MAJ_CAT', 'GEN_ART_NUMBER', 'STORE_ST_CD']:
            if key in result_df.columns:
                result_df[key] = result_df[key].astype(str)
            if key in list_df.columns:
                list_df[key] = list_df[key].astype(str)
        
        # Merge keys
        merge_keys = ['MAJ_CAT', 'GEN_ART_NUMBER', 'STORE_ST_CD']
        valid_keys = [k for k in merge_keys if k in result_df.columns and k in list_df.columns]
        
        if len(valid_keys) > 0:
            for col in list_df.columns:
                if col not in valid_keys:
                    list_df = list_df.rename(columns={col: f'{col}_LIST_{cat}'})
            
            result_df = result_df.merge(list_df, on=valid_keys, how='left')
    
    return result_df


def consolidate_columns(result_df):
    """Consolidate category-specific columns"""
    consolidation_map = {
        'ST-STK': ['ST-STK_BASE_GM', 'ST-STK_BASE_KIDS', 'ST-STK_BASE_LADIES', 'ST-STK_BASE_MENS'],
        'TAG ART-STATUS (L/X)': ['TAG ART-STATUS (L/X)_LIST_GM', 'TAG ART-STATUS (L/X)_LIST_KIDS', 
                                   'TAG ART-STATUS (L/X)_LIST_LADIES', 'TAG ART-STATUS (L/X)_LIST_MENS'],
        'TAG ART-STATUS-2 (L/X)': ['TAG ART-STATUS-2 (L/X)_LIST_GM', 'TAG ART-STATUS-2 (L/X)_LIST_KIDS',
                                     'TAG ART-STATUS-2 (L/X)_LIST_LADIES', 'TAG ART-STATUS-2 (L/X)_LIST_MENS'],
        'ST MBQ + HOLD-MBQ (L-ART)': ['ST MBQ + HOLD-MBQ (L-ART)_LIST_GM', 'ST MBQ + HOLD-MBQ (L-ART)_LIST_KIDS',
                                        'ST MBQ + HOLD-MBQ (L-ART)_LIST_LADIES', 'ST MBQ + HOLD-MBQ (L-ART)_LIST_MENS'],
        'ST MBQ (L-ART)': ['ST MBQ (L-ART)_LIST_GM', 'ST MBQ (L-ART)_LIST_KIDS',
                            'ST MBQ (L-ART)_LIST_LADIES', 'ST MBQ (L-ART)_LIST_MENS'],
        'LISTING CAP': ['LISTING CAP_LIST_GM', 'LISTING CAP_LIST_KIDS',
                        'LISTING CAP_LIST_LADIES', 'LISTING CAP_LIST_MENS'],
    }
    
    for consolidated_name, source_cols in consolidation_map.items():
        existing_cols = [col for col in source_cols if col in result_df.columns]
        
        if len(existing_cols) > 0:
            consolidated = result_df[existing_cols[0]].copy()
            for col in existing_cols[1:]:
                consolidated = consolidated.fillna(result_df[col])
            
            result_df[consolidated_name] = consolidated
            result_df = result_df.drop(columns=existing_cols)
    
    return result_df


def remove_duplicates_and_clean(result_df):
    """Remove duplicate columns and clean data"""
    # Remove duplicate columns
    result_df = result_df.loc[:, ~result_df.columns.duplicated(keep='first')]
    
    # Remove redundant columns
    if 'STORE_ST_NM' in result_df.columns and 'STORE_ST_CD' in result_df.columns:
        result_df = result_df.drop(columns=['STORE_ST_NM'])
    
    # Fill blanks with 0
    result_df = result_df.fillna(0)
    
    return result_df


def generate_summary(result_df, msa_df):
    """Generate summary report"""
    summary = {
        'total_rows': len(result_df),
        'total_columns': len(result_df.columns),
        'original_rows': len(msa_df),
        'columns': result_df.columns.tolist(),
        'data_types': result_df.dtypes.to_dict(),
        'memory_usage': result_df.memory_usage(deep=True).sum() / 1024**2  # MB
    }
    return summary


def export_to_csv(df):
    """Export dataframe to CSV bytes"""
    return df.to_csv(index=False).encode('utf-8')


def export_to_excel(df):
    """Export dataframe to Excel bytes"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)
    output.seek(0)
    return output.getvalue()


# ============================================================================
# STREAMLIT APP
# ============================================================================

def main():
    # Header
    st.title("📊 MSA Article Stock Analysis")
    st.markdown("**Upload your data files and process them instantly**")
    
    # Sidebar
    st.sidebar.title("ℹ️ About")
    st.sidebar.info(
        """
        **MSA Article Stock Analysis System**
        
        Upload your data files to:
        - Filter articles by stock quantity
        - Expand across stores
        - Merge with BASE and LIST data
        - Consolidate columns
        - Download processed results
        """
    )
    
    # Tabs
    tab1, tab2 = st.tabs(["📤 Upload & Process", "📊 Results"])
    
    with tab1:
        st.header("Step 1: Upload Files")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Required Files")
            msa_file = st.file_uploader(
                "MSA Article File (CSV)",
                type=['csv'],
                key='msa_file',
                help="Generated_Colors_2026-03-14.csv"
            )
            
            store_file = st.file_uploader(
                "Store Name File (Excel)",
                type=['xlsx', 'xls'],
                key='store_file',
                help="STORE NAME.xlsx"
            )
        
        with col2:
            st.subheader("📚 Optional: BASE DATA Files")
            base_files = {}
            col_base1, col_base2 = st.columns(2)
            
            with col_base1:
                base_gm = st.file_uploader("BASE-DATA-GM.csv", type=['csv'], key='base_gm')
                if base_gm:
                    base_files['GM'] = base_gm
                
                base_ladies = st.file_uploader("BASE-DATA-LADIES.csv", type=['csv'], key='base_ladies')
                if base_ladies:
                    base_files['LADIES'] = base_ladies
            
            with col_base2:
                base_kids = st.file_uploader("BASE-DATA-KIDS.csv", type=['csv'], key='base_kids')
                if base_kids:
                    base_files['KIDS'] = base_kids
                
                base_mens = st.file_uploader("BASE-DATA-MENS.csv", type=['csv'], key='base_mens')
                if base_mens:
                    base_files['MENS'] = base_mens
        
        st.subheader("📋 Optional: LIST DATA Files")
        col_list1, col_list2, col_list3, col_list4 = st.columns(4)
        
        list_files = {}
        with col_list1:
            list_gm = st.file_uploader("GM-ALL.csv", type=['csv'], key='list_gm')
            if list_gm:
                list_files['GM'] = list_gm
        
        with col_list2:
            list_kids = st.file_uploader("KIDS-ALL.csv", type=['csv'], key='list_kids')
            if list_kids:
                list_files['KIDS'] = list_kids
        
        with col_list3:
            list_ladies = st.file_uploader("LADIES-ALL.csv", type=['csv'], key='list_ladies')
            if list_ladies:
                list_files['LADIES'] = list_ladies
        
        with col_list4:
            list_mens = st.file_uploader("MENS-ALL.csv", type=['csv'], key='list_mens')
            if list_mens:
                list_files['MENS'] = list_mens
        
        st.divider()
        
        # Configuration
        st.header("Step 2: Configure Processing")
        
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            filter_threshold = st.number_input(
                "Stock Quantity Filter (>=)",
                value=50,
                min_value=0,
                step=10,
                help="Filter articles with stock quantity >= this value"
            )
        
        with col_config2:
            st.info(f"Will filter articles with STK_QTY >= {filter_threshold}")
        
        st.divider()
        
        # Process button
        st.header("Step 3: Process Data")
        
        if st.button("🚀 Process Data", use_container_width=True, type="primary"):
            
            # Validate files
            uploaded_files = {
                'msa_file': msa_file,
                'store_file': store_file,
                'base_data_files': base_files,
                'list_data_files': list_files
            }
            
            validation = validate_uploaded_files(uploaded_files)
            
            # Display validation messages
            with st.container():
                for msg in validation['messages']:
                    if "✅" in msg:
                        st.success(msg)
                    elif "❌" in msg:
                        st.error(msg)
                    else:
                        st.info(msg)
            
            if not validation['valid']:
                st.error("❌ Please fix the errors above before processing")
            else:
                # Process data
                with st.spinner("🔄 Processing data (this may take a few minutes)..."):
                    result = process_data(validation['files'], filter_threshold)
                
                if result['success']:
                    st.success("✅ Processing complete!")
                    
                    # Store in session state for download
                    st.session_state.processed_data = result['data']
                    st.session_state.processing_steps = result['steps']
                    st.session_state.summary = result['summary']
                    
                    # Display processing steps
                    st.subheader("Processing Steps:")
                    for step in result['steps']:
                        if "✅" in step:
                            st.success(step)
                        elif "⚠️" in step:
                            st.warning(step)
                        else:
                            st.info(step)
                    
                    # Display summary
                    st.subheader("📈 Processing Summary")
                    col_summary1, col_summary2, col_summary3, col_summary4 = st.columns(4)
                    
                    with col_summary1:
                        st.metric("Total Rows", f"{result['row_count']:,}")
                    with col_summary2:
                        st.metric("Total Columns", result['col_count'])
                    with col_summary3:
                        st.metric("Memory Usage", f"{result['summary']['memory_usage']:.2f} MB")
                    with col_summary4:
                        st.metric("Processing Time", "Completed")
                    
                    # Show sample data
                    st.subheader("📋 Data Preview (First 10 rows)")
                    st.dataframe(result['data'].head(10), use_container_width=True)
                    
                else:
                    st.error(f"❌ Processing failed: {result['error']}")
                    for step in result['steps']:
                        if "❌" in step:
                            st.error(step)
                        else:
                            st.info(step)
    
    with tab2:
        st.header("📥 Download Results")
        
        if 'processed_data' not in st.session_state:
            st.info("👈 Process your data first in the 'Upload & Process' tab")
        else:
            df = st.session_state.processed_data
            summary = st.session_state.summary
            
            # Summary statistics
            col_sum1, col_sum2, col_sum3 = st.columns(3)
            
            with col_sum1:
                st.metric("📊 Total Rows", f"{summary['total_rows']:,}")
            with col_sum2:
                st.metric("📋 Total Columns", summary['total_columns'])
            with col_sum3:
                st.metric("💾 Memory Size", f"{summary['memory_usage']:.2f} MB")
            
            st.divider()
            
            # Download options
            st.subheader("💾 Download Processed Data")
            
            col_download1, col_download2, col_download3 = st.columns(3)
            
            with col_download1:
                csv_data = export_to_csv(df)
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_data,
                    file_name=f"MSA_PROCESSED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_download2:
                excel_data = export_to_excel(df)
                st.download_button(
                    label="📊 Download as Excel",
                    data=excel_data,
                    file_name=f"MSA_PROCESSED_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col_download3:
                st.info("✅ Click to download your processed data")
            
            st.divider()
            
            # Column information
            st.subheader("📋 Column Information")
            
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.write("**Numeric Columns**")
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                for col in numeric_cols:
                    st.write(f"• {col}")
            
            with col_info2:
                st.write("**Text Columns**")
                text_cols = df.select_dtypes(include=['object']).columns.tolist()
                for col in text_cols:
                    st.write(f"• {col}")
            
            st.divider()
            
            # Data statistics
            st.subheader("📊 Data Statistics")
            st.dataframe(df.describe(), use_container_width=True)
            
            st.divider()
            
            # Full data viewer
            st.subheader("👀 View Full Dataset")
            st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()
