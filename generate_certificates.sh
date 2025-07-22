#!/bin/bash

echo "====================================="
echo "   CEU Certificate Generator"
echo "====================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed"
    echo "Please install Python from https://python.org"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check if requirements are installed
if ! $PYTHON_CMD -c "import pandas, jinja2, pdfkit" &> /dev/null; then
    echo "Installing required Python packages..."
    if ! pip3 install -r requirements.txt 2>/dev/null && ! pip install -r requirements.txt 2>/dev/null; then
        echo "ERROR: Failed to install requirements"
        echo "Try: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# Check if attendees.csv exists
if [ ! -f "attendees.csv" ]; then
    echo "ERROR: attendees.csv not found"
    echo "Please create attendees.csv with your event data"
    echo "See README.md for format details"
    exit 1
fi

# Run the certificate generator
echo "Generating certificates..."
$PYTHON_CMD generate_certs.py

if [ $? -eq 0 ]; then
    echo
    echo "====================================="
    echo "   Certificates generated successfully!"
    echo "====================================="
    echo "Check the output folder for your PDFs"
else
    echo
    echo "Generation failed. Check error messages above."
    exit 1
fi 