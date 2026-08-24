@echo off
title KrishiDrishti AI - Public Internet Tunnel
cls
echo ======================================================================
echo       KrishiDrishti AI - Launch to Live Public Internet
echo ======================================================================
echo.
echo Step 1: Starting local server on port 8080...
start /B python -m http.server 8080 >nul 2>&1

echo Step 2: Creating instant public HTTPS internet tunnel (via localtunnel)...
echo.
echo ======================================================================
echo  Your Public Internet URL will appear below:
echo  (Share this link with anyone, anywhere in the world on any phone/PC!)
echo ======================================================================
echo.

npx -y localtunnel --port 8080

if %errorlevel% neq 0 (
    echo.
    echo Node.js/npx not found or tunnel failed.
    echo.
    echo Alternative: You can deploy free in 30 seconds using:
    echo 1. Netlify Drop: Open https://app.netlify.com/drop and drag this folder!
    echo 2. Vercel: npx vercel deploy
    echo 3. GitHub Pages: Push folder to a GitHub repository and enable Pages.
    pause
)
pause
