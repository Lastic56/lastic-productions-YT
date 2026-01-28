@echo off
title Lastic Productions - Starting Server...
echo ==========================================
echo    LASTIC PRODUCTIONS - WEB DOWNLOADER
echo ==========================================
echo.
echo [1/2] Checking dependencies...
pip install flask yt-dlp ffmpeg-python >nul 2>&1

echo [2/2] Starting server...
echo.
echo * Note: This window must stay open while using the app.
echo * You can close this window to stop the server.
echo.

cd "Flask app"
python app.py

pause
