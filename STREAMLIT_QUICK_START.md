# Streamlit Web App - Quick Start (2 Minutes)

## Installation (1 minute)

### 1. Install Streamlit
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run streamlit_app.py
```

**That's it!** The app opens in your browser at `http://localhost:8501`

---

## Using the App (1 minute)

### Step 1: Upload Files
1. Click **"Browse Files"** under "MSA Article File"
2. Select your `Generated_Colors_2026-03-14.csv`
3. Click **"Browse Files"** under "Store Name File"
4. Select your `STORE NAME.xlsx`

### Step 2 (Optional): Upload Extra Data
- Drag & drop your BASE-DATA-*.csv files
- Drag & drop your [CATEGORY]-ALL.csv files

### Step 3: Configure
- Adjust **"Stock Quantity Filter"** (default: 50)
- Leave as-is for standard processing

### Step 4: Process
- Click **"🚀 Process Data"** button
- Wait for ✅ messages (2-10 minutes depending on size)

### Step 5: Download
- Click **"📥 Download as CSV"** OR **"📊 Download as Excel"**
- File downloads automatically!

---

## What You'll See

**During Upload:**
- ✅ Green check = File loaded successfully
- ❌ Red X = File error (re-upload)
- ⚠️ Yellow warning = Optional file missing (OK)

**During Processing:**
- Shows each step: Load → Filter → Expand → Merge → Consolidate
- Shows row counts
- Shows data preview
- Shows statistics

**On Results Tab:**
- 4 big metrics (Rows, Columns, Memory, Status)
- 2 download buttons (CSV & Excel)
- Full data viewer
- Statistics & columns

---

## Keyboard Shortcuts

| Action | Key |
|--------|-----|
| Rerun app | R |
| Clear cache | C |
| Settings | S |

---

## Troubleshooting (30 seconds)

**Problem: "File not found"**
→ Make sure filename matches EXACTLY (case-sensitive)

**Problem: "Encoding error"**
→ App tries 7 encodings automatically. If still fails:
- Open file in Excel
- Save As → CSV UTF-8 Encoding
- Try again

**Problem: "Takes too long"**
→ This is normal for 1M+ rows. Just wait or use a faster computer.

**Problem: "Downloaded file is empty"**
→ Check that processing completed with ✅ checkmarks

---

## File Format Guide

| File | Format | Required? | Example |
|------|--------|-----------|---------|
| MSA | CSV | ✅ Yes | `Generated_Colors_2026-03-14.csv` |
| Store | Excel | ✅ Yes | `STORE NAME.xlsx` |
| BASE DATA | CSV | ❌ Optional | `BASE-DATA-GM.csv` |
| LIST DATA | CSV | ❌ Optional | `GM-ALL.csv` |

---

## Common Settings

**For Filtering:**
- `50` (default) = Most common
- `100` = Stricter filter
- `0` = No filtering

**For Large Files:**
- Use default settings
- Don't upload > 5GB files
- Consider splitting files first

---

## Tips & Tricks

💡 **Tip 1:** Start without BASE/LIST data first to test
💡 **Tip 2:** Keep file names consistent for tracking
💡 **Tip 3:** Excel format is easier to view in Excel
💡 **Tip 4:** CSV format works with Python/R analysis

---

## Next Steps

✅ Need help? See **STREAMLIT_README.md**
✅ Command line version? See **app.py** and run `python app.py`
✅ Technical details? See **PROJECT_SUMMARY.md**

---

**Ready?** Run:
```bash
streamlit run streamlit_app.py
```

Then open `http://localhost:8501` 🚀
