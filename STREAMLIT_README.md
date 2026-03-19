# MSA Article Stock Analysis - Web Application

A powerful web-based interface for processing MSA article stock data with file uploads and instant downloads.

## Features

✨ **Easy File Upload**
- Upload MSA article files (CSV)
- Upload store names (Excel)
- Upload BASE DATA files (optional)
- Upload LIST DATA files (optional)

🚀 **Real-time Processing**
- Filter articles by stock quantity
- Expand across stores (Cartesian product)
- Merge with BASE DATA and LIST DATA
- Consolidate category columns
- Real-time progress tracking

📥 **Multiple Download Formats**
- Download as **CSV** file
- Download as **Excel** file
- Instant download with one click

📊 **Data Analytics**
- Preview processed data
- View statistics & summaries
- Column information
- Memory usage tracking

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web framework
- `pandas` - Data processing
- `numpy` - Numerical operations
- `openpyxl` - Excel handling
- `xlrd` - Excel reading

### 2. Run the Web Application

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage Guide

### Step 1: Upload Your Files

**Required Files:**
- **MSA Article File** (CSV) - Your article data with stock quantities
- **Store Name File** (Excel) - List of all stores

**Optional Files:**
- **BASE DATA** (4 CSV files)
  - `BASE-DATA-GM.csv`
  - `BASE-DATA-KIDS.csv`
  - `BASE-DATA-LADIES.csv`
  - `BASE-DATA-MENS.csv`

- **LIST DATA** (4 CSV files)
  - `GM-ALL.csv`
  - `KIDS-ALL.csv`
  - `LADIES-ALL.csv`
  - `MENS-ALL.csv`

### Step 2: Configure Processing

Set the **Stock Quantity Filter** (default: 50)
- Articles with STK_QTY >= this value will be included
- Adjust to filter your data

### Step 3: Process Data

Click the **"🚀 Process Data"** button to start processing

You'll see:
- ✅ File validation status
- 🔄 Processing progress
- 📈 Summary statistics
- 📋 Data preview

### Step 4: Download Results

Choose your download format:
- 📥 **CSV** - For data analysis tools
- 📊 **Excel** - For spreadsheet applications

## Web Interface Overview

### Upload & Process Tab

1. **Required Files Section**
   - MSA Article File (CSV)
   - Store Name File (Excel)

2. **Optional BASE DATA Section**
   - Upload up to 4 BASE DATA CSV files
   - Files are automatically detected by category (GM, KIDS, LADIES, MENS)

3. **Optional LIST DATA Section**
   - Upload up to 4 LIST DATA CSV files
   - Files are automatically detected by category

4. **Configuration**
   - Set the stock quantity filter threshold
   - View filter settings in real-time

5. **Process Data Button**
   - Large, prominent button to start processing
   - Shows progress while processing

### Results Tab

1. **Summary Metrics**
   - Total rows in output
   - Total columns
   - Memory usage

2. **Download Buttons**
   - CSV download
   - Excel download
   - Timestamped filenames

3. **Data Preview**
   - View first 10 rows
   - Full dataset viewer
   - Statistics summary

## Processing Pipeline

The web app performs 7 steps:

1. **Load Data** - Reads all uploaded files
2. **Filter** - Articles with STK_QTY >= threshold
3. **Expand** - Cartesian product with stores
4. **Merge BASE DATA** - Add stock information
5. **Merge LIST DATA** - Add listing information
6. **Consolidate** - Combine category columns
7. **Clean** - Remove duplicates, fill blanks

## File Requirements

### MSA Article File (CSV)

**Required Columns:**
- `STK_QTY` - Stock quantity (used for filtering)
- `MAJ_CAT` - Major category
- `GEN_ART_NUMBER` - Generic article number
- `STORE_ST_CD` - Store code
- Other columns as needed

### Store Name File (Excel)

**Required Columns:**
- At least one column with store codes or names
- Data should have one row per store

### BASE DATA Files (CSV)

**Required Columns for Merge:**
- `MAJCAT` or `MAJ_CAT`
- `GEN_ART` or `GEN_ART_NUMBER`
- `Store_Code` or `STORE_ST_CD`
- Other columns with stock data

### LIST DATA Files (CSV)

**Required Columns for Merge:**
- `MAJCAT` or `MAJ_CAT`
- `GEN_ART` or `GEN_ART_NUMBER`
- `ST_CD` or `STORE_ST_CD`
- Other columns with listing data

## Encoding Support

The app automatically tries to read CSV files with these encodings (in order):
1. UTF-8
2. UTF-16
3. Latin-1
4. CP1252
5. ISO-8859-1
6. Windows-1252
7. ASCII

If a file fails to read with all encodings, the app will notify you.

## Performance

**Typical Processing Times:**
- Small datasets (< 100K rows): 10-30 seconds
- Medium datasets (100K - 1M rows): 30 seconds - 2 minutes
- Large datasets (1M - 5M rows): 2-10 minutes

**Hardware Requirements:**
- Minimum: 4GB RAM, 1GB disk space
- Recommended: 8GB+ RAM, 10GB disk space

## Troubleshooting

### "File not found" Error
- Check that file names match exactly
- Ensure file is in correct format (CSV or Excel)
- Try re-uploading the file

### "Encoding error" Error
- The file might have special characters
- Try opening in Excel and saving as UTF-8
- Re-upload the file

### Processing Takes Too Long
- This is normal for large datasets (1M+ rows)
- Close other applications to free resources
- Consider using a more powerful computer

### Downloaded File is Empty
- Check that the processing completed successfully
- Ensure data was available in uploaded files
- Try processing again

### "Merge key not found" Warning
- Your files might have different column names
- Check column names in your data
- Refer to column naming requirements above

## Column Consolidation

The app automatically consolidates these columns from BASE DATA:
- `ST-STK` (from BASE-DATA-GM/KIDS/LADIES/MENS)

And from LIST DATA:
- `TAG ART-STATUS (L/X)`
- `TAG ART-STATUS-2 (L/X)`
- `ST MBQ + HOLD-MBQ (L-ART)`
- `ST MBQ (L-ART)`
- `LISTING CAP`

Consolidation priority: **GM → KIDS → LADIES → MENS**

## Output File Formats

### CSV Format
- Comma-separated values
- Compatible with Excel, Python, R, etc.
- Can be opened with any text editor
- Recommended for large datasets

### Excel Format
- XLSX format (Excel 2007+)
- Easier to view in Excel
- Includes automatic column formatting
- Recommended for smaller datasets

## Advanced Tips

### Filtering Large Datasets
- Use a higher filter threshold to reduce output size
- Example: Set to 100 instead of 50 for smaller output

### Combining Multiple Downloads
- If you process the same data multiple times, you can combine CSV files using Excel or pandas
- Keep timestamps consistent for tracking

### Automating Processing
- Save your processing parameters
- Document file naming conventions
- Use consistent folder structures

## Development

### Running in Development Mode
```bash
streamlit run streamlit_app.py --logger.level=debug
```

### Running with Custom Port
```bash
streamlit run streamlit_app.py --server.port 8080
```

### Running with Multi-threading
```bash
streamlit run streamlit_app.py --client.toolbarMode=minimal
```

## Deployment

### Local Network Access
```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

Access from other computers at: `http://<your-ip>:8501`

### Docker Deployment
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0"]
```

### Cloud Deployment
- **Streamlit Cloud** - https://streamlit.io/cloud
- **AWS** - EC2 + Streamlit
- **Heroku** - Simple deployment platform
- **Azure** - App Service

See Streamlit documentation for detailed deployment guides.

## FAQ

**Q: Can I upload files larger than 200MB?**
A: Yes, Streamlit supports large file uploads. For very large files (>1GB), consider splitting them first.

**Q: Can I process the same data multiple times?**
A: Yes, you can upload the same files and process with different filter settings.

**Q: Is my data secure?**
A: Data is processed locally on your machine. For shared deployments, ensure proper security measures.

**Q: Can I customize the column consolidation?**
A: Yes, edit the consolidation logic in the `consolidate_columns()` function in streamlit_app.py.

**Q: How do I update the app?**
A: Pull latest changes and reinstall dependencies: `pip install -r requirements.txt --upgrade`

## Support & Documentation

For more information:
- See **README.md** for full documentation
- See **PROJECT_SUMMARY.md** for technical specifications
- See **QUICK_START.md** for quick setup guide
- See **app.py** for CLI version

## License
Internal Use Only

## Version
1.0.0 - March 2026
