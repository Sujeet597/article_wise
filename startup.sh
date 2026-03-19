#!/bin/bash

# MSA Article Stock Analysis - Streamlit Startup Script
# Designed for Azure App Service deployment

set -e

echo "=========================================="
echo "🚀 Starting Streamlit Application"
echo "=========================================="

# Set environment variables
export STREAMLIT_SERVER_PORT=${WEBSITES_PORT:-8000}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_CLIENT_TOOLBAR_MODE=minimal
export PYTHONUNBUFFERED=1

echo "📊 Configuration:"
echo "   Port: $STREAMLIT_SERVER_PORT"
echo "   Address: $STREAMLIT_SERVER_ADDRESS"
echo "   Headless Mode: $STREAMLIT_SERVER_HEADLESS"

# Check if streamlit_app.py exists
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ ERROR: streamlit_app.py not found!"
    echo "📁 Current directory: $(pwd)"
    echo "📁 Files present:"
    ls -la
    exit 1
fi

echo "✅ streamlit_app.py found"

# Check Python
echo ""
echo "🐍 Python Information:"
python --version
which python

# Check Streamlit
echo ""
echo "📦 Streamlit Information:"
streamlit --version

# Install requirements if not already installed
echo ""
echo "📦 Checking dependencies..."
if [ -f "requirements.txt" ]; then
    echo "   Installing from requirements.txt..."
    pip install --upgrade -q pip setuptools wheel
    pip install -q -r requirements.txt
    echo "   ✅ Dependencies installed"
else
    echo "   ⚠️  requirements.txt not found"
fi

# Create .streamlit directory and config if needed
echo ""
echo "⚙️  Setting up Streamlit configuration..."
mkdir -p ~/.streamlit

# Create streamlit config file
cat > ~/.streamlit/config.toml << EOF
[server]
port = ${STREAMLIT_SERVER_PORT}
address = "${STREAMLIT_SERVER_ADDRESS}"
headless = true
enableCORS = false

[client]
showErrorDetails = false
toolbarMode = "minimal"

[logger]
level = "info"

[theme]
primaryColor = "#0066CC"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#262730"
font = "sans serif"
EOF

echo "✅ Streamlit configuration created"

# Display startup information
echo ""
echo "=========================================="
echo "🌐 Application will start on:"
echo "   URL: http://${STREAMLIT_SERVER_ADDRESS}:${STREAMLIT_SERVER_PORT}"
echo "=========================================="
echo ""

# Start Streamlit application
echo "▶️  Starting application..."
streamlit run streamlit_app.py \
    --server.port=${STREAMLIT_SERVER_PORT} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --client.toolbar.mode=minimal \
    --logger.level=info

# This line should only execute if streamlit exits
echo "❌ Application terminated unexpectedly"
exit 1
