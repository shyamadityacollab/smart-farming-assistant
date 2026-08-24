@echo off
setlocal enabledelayedexpansion
title KrishiDrishti AI - Mobile Web Server
cls
echo ======================================================================
echo       KrishiDrishti AI - Launch on Mobile Phone (Same Wi-Fi)
echo ======================================================================
echo.

:: Detect local IPv4 address
for /f "tokens=4" %%a in ('route print ^| findstr 0.0.0.0 ^| findstr /v "0.0.0.0.*0.0.0.0"') do (
    set LOCAL_IP=%%a
)

if "%LOCAL_IP%"=="" (
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
        set LOCAL_IP=%%a
        set LOCAL_IP=!LOCAL_IP: =!
    )
)

echo [OK] Your PC's Local Network IP is: %LOCAL_IP%
echo.
echo ======================================================================
echo  1. Make sure your Mobile Phone is on the SAME Wi-Fi as this PC.
echo.
echo  2. Open Chrome, Safari, or Brave on your phone and type this URL:
echo.
echo        http://%LOCAL_IP%:8080
echo.
echo ======================================================================
echo.
echo Starting web server on port 8080 (Press Ctrl+C to stop)...
echo.

python -m http.server 8080 --bind 0.0.0.0
if %errorlevel% neq 0 (
    echo.
    echo Python command failed. Please ensure Python is installed, or use Node.js http-server.
    pause
)
pause
