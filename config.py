"""
Configuration file for MSA Article Stock Analysis Project
Modify these settings to customize the processing behavior
"""

# ============================================================================
# DATA FILTERING
# ============================================================================

# Minimum stock quantity threshold for filtering
FILTER_THRESHOLD = 50

# ============================================================================
# INPUT FILE PATHS
# ============================================================================

# Main input directories
MSA_DIRECTORY = './MSA_STORENAME'
BASE_DATA_DIRECTORY = './BASE DATA'
LIST_DATA_DIRECTORY = './LIST'

# Specific input files
MSA_ARTICLE_FILE = 'Generated_Colors_2026-03-14.csv'
STORE_FILE = 'STORE NAME.xlsx'

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

# Output file prefix
OUTPUT_PREFIX = 'FINAL_MSA_FILTERED_EXPANDED'

# Summary report filename
SUMMARY_FILE = 'DATA_SUMMARY.txt'

# Split CSV files if they exceed this row count
CSV_CHUNK_SIZE = 1_000_000

# Maximum rows for Excel export
MAX_EXCEL_ROWS = 1_048_576

# ============================================================================
# ENCODING SUPPORT
# ============================================================================

# List of encodings to try when reading CSV files (in priority order)
ENCODING_LIST = [
    'utf-8',
    'utf-16',
    'latin-1',
    'cp1252',
    'iso-8859-1',
    'windows-1252',
    'ascii'
]

# ============================================================================
# MERGE CONFIGURATION
# ============================================================================

# Merge key mappings for BASE DATA
BASE_DATA_MERGE_KEYS = {
    'msa_keys': ['MAJ_CAT', 'GEN_ART_NUMBER', 'STORE_ST_CD'],
    'base_keys': ['MAJCAT', 'GEN_ART', 'Store_Code']
}

# Merge key mappings for LIST DATA
LIST_DATA_MERGE_KEYS = {
    'msa_keys': ['MAJ_CAT', 'GEN_ART_NUMBER', 'STORE_ST_CD'],
    'list_keys': ['MAJCAT', 'GEN_ART', 'ST_CD']
}

# ============================================================================
# COLUMN CONSOLIDATION
# ============================================================================

# Define which columns should be consolidated from category-specific sources
# Format: 'consolidated_name': ['col_category_1', 'col_category_2', ...]
# These will be combined using sequential fillna in the specified order
CONSOLIDATION_RULES = {
    'ST-STK': [
        'ST-STK_BASE_GM',
        'ST-STK_BASE_KIDS',
        'ST-STK_BASE_LADIES',
        'ST-STK_BASE_MENS'
    ],
    'TAG ART-STATUS (L/X)': [
        'TAG ART-STATUS (L/X)_LIST_GM',
        'TAG ART-STATUS (L/X)_LIST_KIDS',
        'TAG ART-STATUS (L/X)_LIST_LADIES',
        'TAG ART-STATUS (L/X)_LIST_MENS'
    ],
    'TAG ART-STATUS-2 (L/X)': [
        'TAG ART-STATUS-2 (L/X)_LIST_GM',
        'TAG ART-STATUS-2 (L/X)_LIST_KIDS',
        'TAG ART-STATUS-2 (L/X)_LIST_LADIES',
        'TAG ART-STATUS-2 (L/X)_LIST_MENS'
    ],
    'ST MBQ + HOLD-MBQ (L-ART)': [
        'ST MBQ + HOLD-MBQ (L-ART)_LIST_GM',
        'ST MBQ + HOLD-MBQ (L-ART)_LIST_KIDS',
        'ST MBQ + HOLD-MBQ (L-ART)_LIST_LADIES',
        'ST MBQ + HOLD-MBQ (L-ART)_LIST_MENS'
    ],
    'ST MBQ (L-ART)': [
        'ST MBQ (L-ART)_LIST_GM',
        'ST MBQ (L-ART)_LIST_KIDS',
        'ST MBQ (L-ART)_LIST_LADIES',
        'ST MBQ (L-ART)_LIST_MENS'
    ],
    'LISTING CAP': [
        'LISTING CAP_LIST_GM',
        'LISTING CAP_LIST_KIDS',
        'LISTING CAP_LIST_LADIES',
        'LISTING CAP_LIST_MENS'
    ]
}

# ============================================================================
# LOGGING & REPORTING
# ============================================================================

# Enable verbose logging
VERBOSE = True

# Log to file in addition to console
LOG_TO_FILE = True
LOG_FILE = 'processing.log'

# ============================================================================
# PROCESSING OPTIONS
# ============================================================================

# Remove columns with these prefixes if found (to clean up intermediate columns)
COLUMNS_TO_REMOVE_PREFIXES = ['_BASE_', '_LIST_']

# Fill NaN values with this value
FILL_NAN_VALUE = 0

# Remove duplicate columns (keep first occurrence)
REMOVE_DUPLICATE_COLUMNS = True

# Store prefix for expanded store columns
STORE_COLUMN_PREFIX = 'STORE_'

# ============================================================================
# PERFORMANCE TUNING
# ============================================================================

# Number of rows to process at a time (for memory management)
# Set to None for no batching
BATCH_SIZE = None

# Number of parallel jobs for operations that support it
NUM_JOBS = 1

# ============================================================================
# CATEGORY DEFINITIONS
# ============================================================================

# Data categories for BASE DATA and LIST DATA
CATEGORIES = ['GM', 'KIDS', 'LADIES', 'MENS']

# ============================================================================
# DEBUGGING
# ============================================================================

# Show first N rows of data at each step
DEBUG_SAMPLE_ROWS = 5

# Verify data at each step
DEBUG_MODE = False
