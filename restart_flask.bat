@echo off
echo.
echo ============================================
echo FLASK RESTART SCRIPT
echo ============================================
echo.
echo This script will:
echo 1. Kill any running Flask processes
echo 2. Clear Python cache
echo 3. Start Flask with fresh code
echo.
echo Press Ctrl+C now if you want to cancel
echo Otherwise, press any key to continue...
pause > nul

echo.
echo [1/3] Stopping Flask processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" 2>nul
timeout /t 2 /nobreak > nul

echo [2/3] Clearing Python cache...
if exist __pycache__ rmdir /S /Q __pycache__
echo Cache cleared!

echo [3/3] Starting Flask server...
echo.
python app.py
