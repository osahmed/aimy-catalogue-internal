@echo off
REM ============================================
REM Update Public Pitch Page
REM ============================================
REM Copies the latest one-page-pitch.html to
REM the public repository and deploys it
REM ============================================

echo.
echo ========================================
echo  Update Public Pitch Page
echo ========================================
echo.

REM Change to repository directory
cd /d "%~dp0"

REM Check if one-page-pitch.html exists
if not exist "one-page-pitch.html" (
    echo [ERROR] one-page-pitch.html not found in this repository!
    pause
    exit /b 1
)

REM Check if public repo exists
set PUBLIC_REPO=%USERPROFILE%\Documents\aimy-pitch-public
if not exist "%PUBLIC_REPO%" (
    echo [ERROR] Public repository not found at: %PUBLIC_REPO%
    echo Please clone it first: git clone https://github.com/osahmed/aimy-pitch-public.git
    pause
    exit /b 1
)

echo [1/4] Copying pitch page to public repository...
copy /Y "one-page-pitch.html" "%PUBLIC_REPO%\index.html"
if errorlevel 1 (
    echo [ERROR] Failed to copy file!
    pause
    exit /b 1
)
echo [SUCCESS] File copied
echo.

REM Change to public repo
cd /d "%PUBLIC_REPO%"

REM Check if there are changes
git diff --quiet index.html
if %errorlevel% equ 0 (
    echo [INFO] No changes in pitch page. Already up to date.
    echo.
    pause
    exit /b 0
)

echo [2/4] Changes detected in pitch page
echo.

REM Stage and commit
echo [3/4] Committing changes...
git add index.html

for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)

git commit -m "Update pitch page - %mydate% %mytime%" -m "Synced from aimy-catalogue-internal" -m "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

if errorlevel 1 (
    echo [ERROR] Commit failed!
    pause
    exit /b 1
)

REM Push to GitHub
echo [4/4] Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo [ERROR] Push failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  PUBLIC PITCH UPDATE COMPLETE!
echo ========================================
echo.
echo [SUCCESS] Public pitch page updated
echo Live URL: https://osahmed.github.io/aimy-pitch-public/
echo.
echo Note: GitHub Pages deployment takes 1-2 minutes.
echo.
pause
