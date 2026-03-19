# MSA Article Stock Analysis - Setup Instructions

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Sujeet597/article_wise.git
cd article_wise
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Folder Structure
```bash
python setup_folders.py
```

This will create:
- `MSA_STORENAME/`
- `BASE DATA/`
- `LIST/`

### 4. Add Your Data Files

Copy your data files to the correct locations:

```
article_wise/
├── app.py
├── config.py
├── requirements.txt
├── setup_folders.py
├── validate_data.py
│
├── MSA_STORENAME/
│   ├── Generated_Colors_2026-03-14.csv
│   └── STORE NAME.xlsx
│
├── BASE DATA/
│   ├── BASE-DATA-GM.csv
│   ├── BASE-DATA-KIDS.csv
│   ├── BASE-DATA-LADIES.csv
│   └── BASE-DATA-MENS.csv
│
└── LIST/
    ├── GM-ALL.csv
    ├── KIDS-ALL.csv
    ├── LADIES-ALL.csv
    └── MENS-ALL.csv
```

### 5. Validate Your Data (Optional)
```bash
python validate_data.py
```

This checks that all files exist and are readable.

### 6. Run the Processor
```bash
python app.py
```

Processing will take 6-10 minutes depending on your hardware.

### 7. Check Results
After processing, you'll see:
- `FINAL_MSA_FILTERED_EXPANDED_part1.csv`
- `FINAL_MSA_FILTERED_EXPANDED_part2.csv`
- `FINAL_MSA_FILTERED_EXPANDED_part3.csv`
- `FINAL_MSA_FILTERED_EXPANDED_part4.csv`
- `DATA_SUMMARY.txt`

## File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main processing script (687 lines) |
| `config.py` | Configuration and customization |
| `requirements.txt` | Python dependencies |
| `validate_data.py` | Pre-flight data validation |
| `setup_folders.py` | Folder structure creation |
| `README.md` | Detailed documentation |
| `QUICK_START.md` | Quick start guide |
| `PROJECT_SUMMARY.md` | Technical specifications |

## Documentation

- **README.md** - Comprehensive guide with troubleshooting
- **QUICK_START.md** - 5-minute setup guide
- **PROJECT_SUMMARY.md** - Technical specifications and data structure

## Processing Pipeline

The script performs 7 steps:
1. **Load** MSA articles and store data
2. **Filter** articles with stock ≥ 50
3. **Expand** articles across all 353 stores
4. **Merge** with BASE DATA (stock information)
5. **Merge** with LIST DATA (listing & status information)
6. **Consolidate** category-specific columns
7. **Save** results and generate summary

## Customization

Edit `config.py` to customize:
- Filter threshold
- Output file sizes
- Consolidation rules
- Merge key mappings
- Encoding support

No changes needed to `app.py` for most customizations.

## Troubleshooting

### File Not Found
Ensure files are in correct folders with exact names (case-sensitive)

### Encoding Errors
Script tries 7 encodings automatically. If still failing, convert file to UTF-8 in Excel.

### Memory Issues
Use a machine with 8+ GB RAM. Processing 3.3M rows requires 5-8 GB.

### Slow Processing
This is normal! 3.3M rows takes 6-10 minutes. Close other applications to free resources.

## Support

Refer to README.md and QUICK_START.md for detailed help.

---

**Ready to start?** Run:
```bash
python setup_folders.py
python validate_data.py
python app.py
```
