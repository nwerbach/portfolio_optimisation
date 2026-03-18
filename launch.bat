@echo off
REM Portfolio Optimizer Advanced - Windows Launcher
REM This batch file launches the Portfolio Optimizer GUI application

echo ========================================
echo Portfolio Optimizer Pro - Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

echo Checking dependencies...
python -c "import pulp, pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing required dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Launching Portfolio Optimizer...
python portfolio_optimizer_advanced.py

if errorlevel 1 (
    echo.
    echo Error: Application failed to start
    pause
    exit /b 1
)

exit /b 0
