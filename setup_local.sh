#!/bin/bash

# MSA Article Stock Analysis - Local Setup Script
# Supports Python 3.10, 3.11+

set -e

echo "=========================================="
echo "🚀 MSA Article Stock Analysis - Setup"
echo "=========================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "🐍 Python version: $PYTHON_VERSION"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "❌ ERROR: Python 3.10+ required"
    echo "   Your version: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python version compatible"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "antenv" ]; then
    echo "⚠️  Virtual environment already exists (antenv)"
    read -p "Do you want to delete and recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf antenv
        python -m venv antenv
    fi
else
    python -m venv antenv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source antenv/bin/activate

echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel --quiet

echo "✅ Pip upgraded"
echo ""

# Select requirements file based on Python version
echo "📋 Selecting requirements file..."
if [ "$PYTHON_MINOR" -eq 10 ]; then
    REQUIREMENTS="requirements-py310.txt"
    echo "   Using: requirements-py310.txt (Python 3.10 optimized)"
else
    REQUIREMENTS="requirements.txt"
    echo "   Using: requirements.txt (Python 3.11+ compatible)"
fi
echo ""

# Install requirements
echo "📦 Installing dependencies from $REQUIREMENTS..."
if [ ! -f "$REQUIREMENTS" ]; then
    echo "❌ ERROR: $REQUIREMENTS not found"
    exit 1
fi

pip install -r "$REQUIREMENTS"

echo ""
echo "✅ Dependencies installed successfully"
echo ""

# Verify installation
echo "🔍 Verifying installation..."
python -c "import streamlit; print(f'✅ Streamlit {streamlit.__version__} OK')"
python -c "import pandas; print(f'✅ Pandas {pandas.__version__} OK')"
python -c "import numpy; print(f'✅ NumPy {numpy.__version__} OK')"
python -c "import openpyxl; print(f'✅ OpenPyXL {openpyxl.__version__} OK')"

echo ""
echo "=========================================="
echo "🎉 Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate venv: source antenv/bin/activate"
echo "2. Run app: streamlit run streamlit_app.py"
echo "3. Or run CLI: python app.py"
echo ""
