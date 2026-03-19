# Quick Start Guide - MSA Article Stock Analysis

## 5-Minute Setup

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Folder Structure
Create these directories in your project folder:
```bash
mkdir "MSA_STORENAME"
mkdir "BASE DATA"
mkdir "LIST"
```

### Step 3: Place Your Data Files

Move your data files to the correct locations:

```
Your Project Folder/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── PROJECT_SUMMARY.md
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

### Step 4: Run the Script
```bash
python app.py
```

### Step 5: Check Results
After 6-10 minutes, you'll see:
- `FINAL_MSA_FILTERED_EXPANDED_part1.csv`
- `FINAL_MSA_FILTERED_EXPANDED_part2.csv`
- `FINAL_MSA_FILTERED_EXPANDED_part3.csv`
- `FINAL_MSA_FILTERED_EXPANDED_part4.csv`
- `DATA_SUMMARY.txt`

---

## What Happens During Processing?

| Step | What It Does | Input | Output |
|------|-------------|-------|--------|
| 1 | Loads MSA articles & store data | CSV + Excel | Data in memory |
| 2 | Filters articles with stock ≥ 50 | 8,519 articles | 8,519 articles |
| 3 | Expands across all 353 stores | 8,519 articles | 3M+ rows |
| 4 | Joins with BASE DATA & LIST DATA | Lookup CSVs | Added columns |
| 5 | Consolidates category columns | Multi-column | Single column |
| 6 | Saves to CSV (splits if >1M) | 3M rows | Part files |
| 7 | Generates summary report | Final data | DATA_SUMMARY.txt |

---

## Common Issues & Solutions

### Issue: "File not found" error
**Solution:** Check that:
- File names match EXACTLY (case-sensitive)
- Files are in the correct folders
- Folder names have correct spacing (e.g., "BASE DATA" not "BASE_DATA")

### Issue: "Encoding error" when reading a file
**Solution:** The script tries 7 encodings automatically. If it still fails:
1. Open the file in Excel
2. Save As → CSV UTF-8
3. Run the script again

### Issue: Script is taking a very long time
**Solution:** This is normal! Processing 3M rows takes 6-10 minutes depending on:
- Your computer's RAM and CPU
- File size
- Hard drive speed

### Issue: "No module named pandas" error
**Solution:** Run this first:
```bash
pip install -r requirements.txt
```

### Issue: Output CSV is too large to open
**Solution:** This is normal for 3M+ rows. Use:
- **Excel**: Open with Data → From Text for large files
- **Python**: Use pandas to read specific parts
- **Terminal**: Use `head -n 1000 filename.csv` to view samples

---

## Customizing the Script

### Change Filter Threshold
Edit `config.py`:
```python
FILTER_THRESHOLD = 100  # Changed from 50
```

### Change Output File Size
Edit `config.py`:
```python
CSV_CHUNK_SIZE = 500_000  # Changed from 1M to 500K
```

### Modify Consolidation Rules
Edit `config.py`:
```python
CONSOLIDATION_RULES = {
    'MY_COLUMN': ['col_gm', 'col_kids', 'col_ladies', 'col_mens']
}
```

---

## Understanding Your Output

### FINAL_MSA_FILTERED_EXPANDED_part1.csv
Contains columns like:
- Original: DATE, ST_CD, GEN_ART_NUMBER, GEN_ART_DESC, etc.
- Store expansion: STORE_ST_CD, STORE_RDC-TAG, STORE_[other columns]
- BASE DATA: ST-STK (consolidated)
- LIST DATA: TAG ART-STATUS (L/X), LISTING CAP, etc.

### DATA_SUMMARY.txt
Shows:
- Total rows & columns
- All column names
- First 5 rows of data
- Statistical summary

---

## Next Steps

1. **Review Results**: Open `DATA_SUMMARY.txt` to see what was processed
2. **Combine CSV Parts** (if needed): Use Python or Excel to merge part files
3. **Analyze Data**: Import CSV files into your BI tool or data platform
4. **Automate**: Set up a scheduled task to run this script regularly

---

## Performance Tips

- **Run on a powerful machine**: Larger RAM = faster processing
- **Use SSD storage**: Faster I/O than HDD
- **Close other applications**: Free up system resources
- **Run during off-hours**: Avoid disk usage from other processes

---

## File Size Reference

For typical datasets:
- Input data: ~100 MB
- Processing (peak RAM): 5-8 GB
- Output files: 800+ MB (split into 4 parts)

---

## Getting Help

1. Check `README.md` for detailed documentation
2. Review `PROJECT_SUMMARY.md` for technical specifications
3. Look at script comments in `app.py`
4. Check `DATA_SUMMARY.txt` output for data insights

---

**Ready to go? Run:** `python app.py`
