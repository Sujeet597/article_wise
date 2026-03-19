# MSA Article Stock Analysis - Complete Project Guide

## 📚 Project Files Overview

This project contains everything you need to process MSA article stock data. Here's what each file does:

---

## 🎯 Quick Start Files

### 1. **streamlit_app.py** ⭐ START HERE
**The Web Interface** - Upload files, process data, download results

```bash
streamlit run streamlit_app.py
```

- 📤 Upload files through web interface
- 🔄 Real-time processing with progress tracking
- 📥 Download as CSV or Excel
- 📊 View statistics and data preview

**Best For:** Users who want a graphical interface

---

### 2. **app.py** 
**Command Line Version** - For automation and batch processing

```bash
python app.py
```

- 🏃 Process data from pre-configured folders
- ⚙️ No user interface needed
- 🔄 Good for scheduled tasks
- 📁 Requires specific folder structure

**Best For:** Developers and automation scripts

---

## 📖 Documentation Files

### 3. **STREAMLIT_QUICK_START.md** ⭐
**2-Minute Quick Start** for web app

- ✅ Installation in 1 minute
- ✅ Usage in 1 minute
- ✅ Simple troubleshooting

**Read This First** if using the web app

---

### 4. **STREAMLIT_README.md**
**Complete Web App Documentation**

- 📖 Detailed usage guide
- 🎨 Interface overview
- 🔧 Configuration options
- 🐛 Troubleshooting

**Read This For:** In-depth web app information

---

### 5. **DEPLOYMENT_GUIDE.md**
**How to Deploy to Cloud or Network**

- 🌐 Local deployment
- 🔗 Network sharing
- ☁️ Streamlit Cloud (free)
- 🐳 Docker deployment
- 🚀 AWS, Heroku, other platforms

**Read This For:** Sharing app with team or deploying to production

---

### 6. **README.md**
**Complete CLI Documentation**

- 📋 Detailed specification
- 🔧 Configuration guide
- 📊 Column mapping
- 🎯 Advanced usage

**Read This For:** Using the command-line version (app.py)

---

### 7. **QUICK_START.md**
**Quick Start for CLI Version**

- ⚡ 5-minute setup
- 🚀 Step-by-step instructions
- ✅ Customization tips

**Read This For:** Quick setup of CLI version

---

### 8. **PROJECT_SUMMARY.md**
**Technical Specifications**

- 📐 Data structure details
- 📋 Column definitions
- 🔄 Processing pipeline
- 💾 File format specifications

**Read This For:** Understanding the data flow and technical details

---

## ⚙️ Configuration Files

### 9. **config.py**
**Settings for CLI Version**

- 🎯 Filter threshold (default: 50)
- 📂 File paths
- 📊 Output settings
- 🔤 Column consolidation rules

**Edit This To:** Customize CLI processing behavior

---

### 10. **requirements.txt**
**Python Dependencies**

```bash
pip install -r requirements.txt
```

**Contains:**
- pandas (data processing)
- numpy (numerical operations)
- openpyxl (Excel handling)
- streamlit (web interface)

---

### 11. **.streamlit/config.toml**
**Streamlit Configuration**

- 🎨 Theme settings
- 🖥️ Server configuration
- 📱 Client settings

**Edit This To:** Customize web app appearance

---

## 🛠️ Helper Scripts

### 12. **setup_folders.py**
**Create Folder Structure**

```bash
python setup_folders.py
```

**Creates:**
- `MSA_STORENAME/`
- `BASE DATA/`
- `LIST/`

**Use This:** First time setup only

---

### 13. **validate_data.py**
**Check Data Files**

```bash
python validate_data.py
```

**Checks:**
- All files exist
- Files are readable
- Required columns present

**Use This:** Before processing to catch errors early

---

## 📊 Data Files (You Provide These)

### 14. **MSA Article File** (Required)
- Filename: `Generated_Colors_2026-03-14.csv`
- Location: `MSA_STORENAME/`
- Format: CSV

**Contains:** Article data with stock quantities

---

### 15. **Store File** (Required)
- Filename: `STORE NAME.xlsx`
- Location: `MSA_STORENAME/`
- Format: Excel

**Contains:** List of all stores (353 stores typically)

---

### 16. **BASE DATA Files** (Optional)
- Location: `BASE DATA/`
- Format: CSV (4 files)
- Files:
  - `BASE-DATA-GM.csv`
  - `BASE-DATA-KIDS.csv`
  - `BASE-DATA-LADIES.csv`
  - `BASE-DATA-MENS.csv`

**Contains:** Stock information by category

---

### 17. **LIST DATA Files** (Optional)
- Location: `LIST/`
- Format: CSV (4 files)
- Files:
  - `GM-ALL.csv`
  - `KIDS-ALL.csv`
  - `LADIES-ALL.csv`
  - `MENS-ALL.csv`

**Contains:** Listing and status information by category

---

## 📁 Project Structure

```
msa-article-analysis/
│
├── 🌐 WEB INTERFACE
│   ├── streamlit_app.py          ← Start here for web app
│   └── .streamlit/config.toml    ← Web app configuration
│
├── 🖥️ COMMAND LINE
│   ├── app.py                    ← CLI version
│   ├── config.py                 ← CLI configuration
│   └── setup_folders.py          ← Create folders
│
├── 📖 DOCUMENTATION
│   ├── STREAMLIT_QUICK_START.md  ← 2-min web setup
│   ├── STREAMLIT_README.md       ← Full web guide
│   ├── DEPLOYMENT_GUIDE.md       ← Deploy to cloud
│   ├── README.md                 ← CLI guide
│   ├── QUICK_START.md            ← 5-min CLI setup
│   └── PROJECT_SUMMARY.md        ← Technical specs
│
├── ⚙️ SETUP
│   ├── requirements.txt          ← Dependencies
│   ├── validate_data.py          ← Check files
│   └── setup_folders.py          ← Create structure
│
└── 📂 DATA (you create these)
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

---

## 🚀 How to Use

### Option 1: Web Interface (EASIEST) ⭐

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. Run web app
   ```bash
   streamlit run streamlit_app.py
   ```

3. Upload files through browser
4. Download results

**See:** STREAMLIT_QUICK_START.md

---

### Option 2: Command Line (ADVANCED)

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. Create folder structure
   ```bash
   python setup_folders.py
   ```

3. Copy data files to correct folders

4. Validate data
   ```bash
   python validate_data.py
   ```

5. Run processor
   ```bash
   python app.py
   ```

6. Check results in output files

**See:** QUICK_START.md

---

### Option 3: Deploy to Cloud (SHARE WITH TEAM)

1. Push code to GitHub
2. Use Streamlit Cloud or Heroku
3. Share URL with team

**See:** DEPLOYMENT_GUIDE.md

---

## 📋 Processing Steps

Both web and CLI versions perform these 7 steps:

1. **Load Data**
   - Read CSV and Excel files
   - Detect encoding automatically

2. **Filter**
   - Keep articles with STK_QTY >= threshold (default: 50)

3. **Expand**
   - Create Cartesian product with all stores
   - ~3M rows for typical data

4. **Merge BASE DATA**
   - Add stock information from BASE-DATA-*.csv
   - Consolidate by category

5. **Merge LIST DATA**
   - Add listing information from [CATEGORY]-ALL.csv
   - Consolidate by category

6. **Consolidate**
   - Combine category-specific columns
   - Fill missing values intelligently

7. **Clean & Export**
   - Remove duplicates
   - Fill blanks with 0
   - Save as CSV/Excel

---

## 🔍 File Selection Guide

| Need | Use | File |
|------|-----|------|
| Quick web upload | Web interface | `streamlit_app.py` |
| Batch processing | Command line | `app.py` |
| Deploy to cloud | Deployment guide | `DEPLOYMENT_GUIDE.md` |
| Troubleshoot | Validation | `validate_data.py` |
| Understand data | Technical specs | `PROJECT_SUMMARY.md` |
| Configure | Settings | `config.py` |

---

## 💡 Tips

**Tip 1: Start Simple**
- Upload only required files first
- Test with smaller filter threshold
- Add optional data later if needed

**Tip 2: Validate Early**
- Run `validate_data.py` before processing
- Catches errors early
- Saves time debugging

**Tip 3: Monitor Progress**
- Web app shows real-time progress
- CLI version shows step-by-step output
- Large files take 5-10 minutes (normal!)

**Tip 4: Keep Original Files**
- Don't delete source files
- Processed files are new (not overwritten)
- Easy to retry with different settings

**Tip 5: Version Your Data**
- Use timestamps in filenames
- Track which version was processed
- Example: `MSA_processed_20260319_1430.xlsx`

---

## 🆘 Need Help?

| Question | Answer Location |
|----------|-----------------|
| How do I use the web app? | STREAMLIT_QUICK_START.md |
| How do I deploy to cloud? | DEPLOYMENT_GUIDE.md |
| What do the columns mean? | PROJECT_SUMMARY.md |
| Command-line setup? | QUICK_START.md |
| Detailed CLI docs? | README.md |
| My data isn't working? | validate_data.py |

---

## ✅ Checklist

Before starting:
- [ ] Installed Python 3.8+
- [ ] Ran `pip install -r requirements.txt`
- [ ] Have your data files ready
- [ ] Know if you want web or CLI

---

## 🎯 Next Steps

1. **Choose Your Interface**
   - Web (easiest) → `streamlit run streamlit_app.py`
   - CLI (advanced) → `python app.py`

2. **Read the Guide**
   - Web → STREAMLIT_QUICK_START.md
   - CLI → QUICK_START.md

3. **Gather Your Data**
   - Required: MSA file + Store file
   - Optional: BASE DATA and LIST DATA files

4. **Start Processing**
   - Upload files
   - Click Process
   - Download results

---

## 📞 Support

For detailed help:
- Web app issues → Check STREAMLIT_README.md
- CLI issues → Check README.md
- Data issues → Run validate_data.py
- Deployment → Check DEPLOYMENT_GUIDE.md

---

**Ready to start?** 🚀

For web: `streamlit run streamlit_app.py`
For CLI: `python app.py`

See you in the docs! 📚
