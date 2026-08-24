@echo off
echo ==========================================================
echo Starting KrishiDrishti AI Local Web Server...
echo Open in any browser: http://localhost:8080
echo ==========================================================
start http://localhost:8080
python -m http.server 8080
if %errorlevel% neq 0 (
    echo Python not found, opening directly via file system...
    start "" "%~dp0index.html"
)
pause
