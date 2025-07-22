@echo off
echo =====================================
echo   CEU Certificate Generator
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import pandas, jinja2, pdfkit" >nul 2>&1
if errorlevel 1 (
    echo Installing required Python packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
)

REM Check if attendees.csv exists
if not exist "attendees.csv" (
    echo ERROR: attendees.csv not found
    echo Please create attendees.csv with your event data
    echo See README.md for format details
    pause
    exit /b 1
)

REM Run the certificate generator
echo Generating certificates...
python generate_certs.py

if errorlevel 1 (
    echo.
    echo Generation failed. Check error messages above.
) else (
    echo.
    echo =====================================
    echo   Certificates generated successfully!
    echo =====================================
    echo Check the output folder for your PDFs
)

echo.
pause 