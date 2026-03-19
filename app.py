"""
MSA Article Stock Analysis - Filtered & Expanded Consolidation
Project: Article Wise
Purpose: Load MSA article stock data, filter by inventory threshold (STK_QTY ≥ 50),
expand across all stores, merge with category-specific BASE DATA and LIST DATA,
consolidate columns from multiple sources, and generate clean consolidated output files.

Version: 1.0
Last Updated: March 2026
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
ENCODING_LIST = ['utf-8', 'utf-16', 'latin-1', 'cp1252', 'iso-8859-1', 'windows-1252', 'ascii']
FILTER_THRESHOLD = 50
CSV_CHUNK_SIZE = 1_000_000
MAX_EXCEL_ROWS = 1_048_576

# File paths
BASE_DIR = Path('.')
MSA_DIR = BASE_DIR / 'MSA_STORENAME'
BASE_DATA_DIR = BASE_DIR / 'BASE DATA'
LIST_DATA_DIR = BASE_DIR / 'LIST'

# Output file paths
OUTPUT_PREFIX = 'FINAL_MSA_FILTERED_EXPANDED'
SUMMARY_FILE = 'DATA_SUMMARY.txt'


def log_message(message, step=None):
    """Print and log timestamped messages."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if step:
        print(f"[{timestamp}] STEP {step}: {message}")
    else:
        print(f"[{timestamp}] {message}")


def try_read_csv(file_path, encoding_list=ENCODING_LIST):
    """Try reading CSV with multiple encodings."""
    for encoding in encoding_list:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            log_message(f"Successfully read {file_path} with encoding: {encoding}")
            return df
        except Exception as e:
            continue
    
    log_message(f"Failed to read {file_path} with any encoding. Using default.", step=None)
    return None


def try_read_excel(file_path):
    """Try reading Excel file."""
    try:
        df = pd.read_excel(file_path)
        log_message(f"Successfully read {file_path}")
        return df
    except Exception as e:
        log_message(f"Error reading {file_path}: {str(e)}", step=None)
        return None


def step_1_load_data():
    """STEP 1: Load MSA Data and Store Names"""
    log_message("Starting data load...", step=1)
    
    # Load MSA article data
    msa_file = MSA_DIR / 'Generated_Colors_2026-03-14.csv'
    if not msa_file.exists():
        log_message(f"MSA file not found: {msa_file}", step=1)
        return None, None
    
    msa_df = try_read_csv(str(msa_file))
    if msa_df is None:
        log_message(f"Failed to load MSA data", step=1)
        return None, None
    
    log_message(f"Loaded MSA data: {len(msa_df)} rows, {len(msa_df.columns)} columns", step=1)
    
    # Load store names
    store_file = MSA_DIR / 'STORE NAME.xlsx'
    if not store_file.exists():
        log_message(f"Store file not found: {store_file}", step=1)
        return msa_df, None
    
    store_df = try_read_excel(str(store_file))
    if store_df is None:
        log_message(f"Failed to load store data", step=1)
        return msa_df, None
    
    log_message(f"Loaded store data: {len(store_df)} rows, {len(store_df.columns)} columns", step=1)
    
    return msa_df, store_df


def step_2_filter_data(msa_df):
    """STEP 2: Filter Data by Stock Quantity"""
    log_message(f"Filtering data where STK_QTY >= {FILTER_THRESHOLD}...", step=2)
    
    if 'STK_QTY' not in msa_df.columns:
        log_message("STK_QTY column not found. Skipping filter.", step=2)
        filtered_df = msa_df.copy()
    else:
        filtered_df = msa_df[msa_df['STK_QTY'] >= FILTER_THRESHOLD].copy()
    
    log_message(f"After filter: {len(filtered_df)} rows ({100*len(filtered_df)/len(msa_df):.1f}% of original)", step=2)
    
    return filtered_df


def step_3_expand_by_stores(filtered_df, store_df):
    """STEP 3: Expand by Stores (Cartesian Product)"""
    log_message(f"Expanding {len(filtered_df)} articles × {len(store_df)} stores...", step=3)
    
    # Add key column for merging
    filtered_df['_merge_key'] = 1
    store_df['_merge_key'] = 1
    
    # Cartesian product merge
    expanded_df = filtered_df.merge(store_df, on='_merge_key', how='left')
    expanded_df = expanded_df.drop('_merge_key', axis=1)
    
    # Rename store columns with STORE_ prefix
    store_cols = store_df.columns.difference(['_merge_key'])
    rename_dict = {col: f'STORE_{col}' for col in store_cols}
    expanded_df = expanded_df.rename(columns=rename_dict)
    
    expected_rows = len(filtered_df) * len(store_df)
    log_message(f"Expanded to {len(expanded_df)} rows (expected: {expected_rows})", step=3)
    
    return expanded_df


def load_base_data():
    """Load all BASE DATA files"""
    log_message("Loading BASE DATA files...", step=4)
    
    base_data = {}
    categories = ['GM', 'KIDS', 'LADIES', 'MENS']
    
    for cat in categories:
        file_path = BASE_DATA_DIR / f'BASE-DATA-{cat}.csv'
        if file_path.exists():
            df = try_read_csv(str(file_path))
            if df is not None:
                base_data[cat] = df
                log_message(f"Loaded BASE-DATA-{cat}.csv: {len(df)} rows", step=4)
            else:
                log_message(f"Failed to load BASE-DATA-{cat}.csv", step=4)
        else:
            log_message(f"File not found: {file_path}", step=4)
    
    return base_data


def load_list_data():
    """Load all LIST DATA files"""
    log_message("Loading LIST DATA files...", step=4)
    
    list_data = {}
    categories = ['GM', 'KIDS', 'LADIES', 'MENS']
    
    for cat in categories:
        file_path = LIST_DATA_DIR / f'{cat}-ALL.csv'
        if file_path.exists():
            df = try_read_csv(str(file_path))
            if df is not None:
                list_data[cat] = df
                log_message(f"Loaded {cat}-ALL.csv: {len(df)} rows", step=4)
            else:
                log_message(f"Failed to load {cat}-ALL.csv (will retry with fallback encoding)", step=4)
        else:
            log_message(f"File not found: {file_path}", step=4)
    
    return list_data


def merge_base_data(expanded_df, base_data):
    """Merge BASE DATA with expanded dataset"""
    log_message("Merging BASE DATA...", step=4)
    
    result_df = expanded_df.copy()
    
    for cat, base_df in base_data.items():
        # Rename columns for merging
        base_df = base_df.copy()
        
        # Identify merge keys
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
            # Add category suffix to columns before merge
            for col in base_df.columns:
                if col not in valid_keys:
                    base_df = base_df.rename(columns={col: f'{col}_BASE_{cat}'})
            
            result_df = result_df.merge(base_df, on=valid_keys, how='left')
            log_message(f"Merged BASE DATA ({cat}): {len(result_df)} rows", step=4)
    
    return result_df


def merge_list_data(expanded_df, list_data):
    """Merge LIST DATA with expanded dataset"""
    log_message("Merging LIST DATA...", step=4)
    
    result_df = expanded_df.copy()
    
    for cat, list_df in list_data.items():
        # Rename columns for merging
        list_df = list_df.copy()
        
        # Identify merge keys
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
            # Add category suffix to columns before merge
            for col in list_df.columns:
                if col not in valid_keys:
                    list_df = list_df.rename(columns={col: f'{col}_LIST_{cat}'})
            
            result_df = result_df.merge(list_df, on=valid_keys, how='left')
            log_message(f"Merged LIST DATA ({cat}): {len(result_df)} rows", step=4)
    
    return result_df


def consolidate_columns(result_df):
    """STEP 5: Consolidate category-specific columns"""
    log_message("Consolidating category-specific columns...", step=5)
    
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
        # Check which source columns exist
        existing_cols = [col for col in source_cols if col in result_df.columns]
        
        if len(existing_cols) > 0:
            # Sequential fillna consolidation
            consolidated = result_df[existing_cols[0]].copy()
            for col in existing_cols[1:]:
                consolidated = consolidated.fillna(result_df[col])
            
            result_df[consolidated_name] = consolidated
            
            # Remove original category columns
            result_df = result_df.drop(columns=existing_cols)
            log_message(f"Consolidated '{consolidated_name}' from {len(existing_cols)} columns", step=5)
    
    return result_df


def remove_duplicates_and_clean(result_df):
    """Remove duplicate columns and clean data"""
    log_message("Removing duplicates and cleaning data...", step=5)
    
    # Remove duplicate ST_CD columns (keep first)
    st_cd_cols = [col for col in result_df.columns if col == 'ST_CD']
    if len(st_cd_cols) > 1:
        result_df = result_df.loc[:, ~result_df.columns.duplicated(keep='first')]
        log_message(f"Removed duplicate ST_CD columns", step=5)
    
    # Remove redundant STORE_ST_NM if STORE_ST_CD exists
    if 'STORE_ST_NM' in result_df.columns and 'STORE_ST_CD' in result_df.columns:
        result_df = result_df.drop(columns=['STORE_ST_NM'])
        log_message(f"Removed redundant STORE_ST_NM column", step=5)
    
    # Fill blanks with 0
    result_df = result_df.fillna(0)
    log_message(f"Filled blank values with 0", step=5)
    
    return result_df


def step_4_merge_data(expanded_df):
    """STEP 4: Add VLOOKUP Data"""
    log_message("Starting data merge operations...", step=4)
    
    result_df = expanded_df.copy()
    
    # Load and merge BASE DATA
    base_data = load_base_data()
    if base_data:
        result_df = merge_base_data(result_df, base_data)
    
    # Load and merge LIST DATA
    list_data = load_list_data()
    if list_data:
        result_df = merge_list_data(result_df, list_data)
    
    return result_df


def step_5_consolidate(result_df):
    """STEP 5: Consolidate and Clean Data"""
    log_message("Starting data consolidation and cleaning...", step=5)
    
    result_df = consolidate_columns(result_df)
    result_df = remove_duplicates_and_clean(result_df)
    
    log_message(f"Final consolidated data: {len(result_df)} rows, {len(result_df.columns)} columns", step=5)
    
    return result_df


def step_6_save_results(result_df):
    """STEP 6: Save Results"""
    log_message("Saving results...", step=6)
    
    total_rows = len(result_df)
    
    if total_rows > CSV_CHUNK_SIZE:
        # Split into multiple CSV files
        num_parts = (total_rows + CSV_CHUNK_SIZE - 1) // CSV_CHUNK_SIZE
        log_message(f"Splitting data into {num_parts} CSV files (~{CSV_CHUNK_SIZE:,} rows each)", step=6)
        
        for part_num in range(1, num_parts + 1):
            start_idx = (part_num - 1) * CSV_CHUNK_SIZE
            end_idx = min(part_num * CSV_CHUNK_SIZE, total_rows)
            
            part_df = result_df.iloc[start_idx:end_idx]
            output_file = f'{OUTPUT_PREFIX}_part{part_num}.csv'
            
            part_df.to_csv(output_file, index=False)
            log_message(f"Saved {output_file}: {len(part_df):,} rows", step=6)
    else:
        # Save as single CSV
        output_file = f'{OUTPUT_PREFIX}.csv'
        result_df.to_csv(output_file, index=False)
        log_message(f"Saved {output_file}: {len(result_df):,} rows", step=6)
        
        # Try to save as Excel if rows < max
        if total_rows < MAX_EXCEL_ROWS:
            try:
                excel_file = f'{OUTPUT_PREFIX}.xlsx'
                result_df.to_excel(excel_file, index=False)
                log_message(f"Saved {excel_file}: {len(result_df):,} rows", step=6)
            except Exception as e:
                log_message(f"Could not save Excel file: {str(e)}", step=6)
    
    return result_df


def step_7_generate_summary(result_df, msa_df):
    """STEP 7: Generate Summary Report"""
    log_message("Generating summary report...", step=7)
    
    summary = []
    summary.append("=" * 80)
    summary.append("MSA ARTICLE STOCK ANALYSIS - DATA SUMMARY REPORT")
    summary.append("=" * 80)
    summary.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append("")
    
    summary.append("DATASET DIMENSIONS")
    summary.append("-" * 80)
    summary.append(f"Original MSA Records: {len(msa_df):,}")
    summary.append(f"Records After Filter (STK_QTY >= {FILTER_THRESHOLD}): {len(msa_df):,}")
    summary.append(f"Final Output Rows: {len(result_df):,}")
    summary.append(f"Final Output Columns: {len(result_df.columns)}")
    summary.append("")
    
    summary.append("COLUMN INFORMATION")
    summary.append("-" * 80)
    
    numeric_cols = result_df.select_dtypes(include=[np.number]).columns.tolist()
    text_cols = result_df.select_dtypes(include=['object']).columns.tolist()
    
    summary.append(f"Numeric Columns ({len(numeric_cols)}):")
    for col in numeric_cols:
        summary.append(f"  - {col}")
    summary.append("")
    
    summary.append(f"Text Columns ({len(text_cols)}):")
    for col in text_cols:
        summary.append(f"  - {col}")
    summary.append("")
    
    summary.append("SAMPLE DATA (First 5 Rows)")
    summary.append("-" * 80)
    summary.append(result_df.head(5).to_string())
    summary.append("")
    
    summary.append("DATA STATISTICS")
    summary.append("-" * 80)
    summary.append(result_df.describe().to_string())
    summary.append("")
    
    summary.append("=" * 80)
    summary.append("END OF REPORT")
    summary.append("=" * 80)
    
    # Write to file
    with open(SUMMARY_FILE, 'w') as f:
        f.write('\n'.join(summary))
    
    log_message(f"Summary report saved to {SUMMARY_FILE}", step=7)


def main():
    """Main processing pipeline"""
    print("\n" + "=" * 80)
    print("MSA ARTICLE STOCK ANALYSIS - FILTERED & EXPANDED CONSOLIDATION")
    print("=" * 80 + "\n")
    
    try:
        # STEP 1: Load data
        msa_df, store_df = step_1_load_data()
        if msa_df is None or store_df is None:
            log_message("Failed to load required data files. Exiting.")
            sys.exit(1)
        
        # STEP 2: Filter data
        filtered_df = step_2_filter_data(msa_df)
        
        # STEP 3: Expand by stores
        expanded_df = step_3_expand_by_stores(filtered_df, store_df)
        
        # STEP 4: Merge data
        merged_df = step_4_merge_data(expanded_df)
        
        # STEP 5: Consolidate and clean
        consolidated_df = step_5_consolidate(merged_df)
        
        # STEP 6: Save results
        final_df = step_6_save_results(consolidated_df)
        
        # STEP 7: Generate summary
        step_7_generate_summary(final_df, msa_df)
        
        print("\n" + "=" * 80)
        log_message("PROCESSING COMPLETE!", step=None)
        print("=" * 80 + "\n")
        
    except Exception as e:
        log_message(f"ERROR: {str(e)}", step=None)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
