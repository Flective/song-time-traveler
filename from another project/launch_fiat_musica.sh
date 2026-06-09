#!/bin/bash
# Fiat Musica App Launcher
# Double-click this file in Finder, or run it from Terminal

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_FILE="$APP_DIR/fiat_musica_v8_1.py"

echo "Starting Fiat Musica v8..."
echo "App will open in your browser at http://localhost:8501"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Streamlit not found. Installing..."
    pip3 install streamlit --quiet
fi

# Launch
cd "$APP_DIR"
streamlit run fiat_musica_v8_1.py --server.port 8501
