@echo off
title CEU Certificate Generator
color 0a

echo.
echo ===============================================
echo           CEU Certificate Generator
echo ===============================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if there are any CSV files to process
set csv_found=0
for %%f in (*.csv) do (
    if not "%%f"=="attendees_test.csv" if not "%%f"=="attendees_salesforce_format.csv" (
        set csv_found=1
        echo Found CSV file: %%f
        echo.
        set /p choice="Process %%f? (Y/N): "
        if /i "!choice!"=="Y" (
            echo.
            echo Generating certificates from %%f...
            python generate_certs.py --csv "%%f"
            echo.
            echo ===============================================
            echo Certificates generated! Check the output folder.
            echo ===============================================
        )
    )
)

if %csv_found%==0 (
    echo No CSV files found in the current directory.
    echo.
    echo Please add your attendee CSV file and run again.
    echo Format: SubscriberKey,EmailAddress,FirstName,LastName,Credentials,EventTitle,EventDate
)

echo.
pause 