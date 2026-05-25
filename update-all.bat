@echo off
REM ============================================
REM AiMY Complete Update Script
REM ============================================
REM This master script:
REM 1. Fetches latest Jira data
REM 2. Updates private catalogue repository
REM 3. Updates public pitch page
REM 4. Deploys everything to GitHub
REM ============================================

echo.
echo ============================================
echo   AiMY COMPLETE UPDATE - ALL REPOS
echo ============================================
echo.
echo This will:
echo  - Fetch latest Jira data
echo  - Update private catalogue repository
echo  - Update public pitch page
echo  - Push all changes to GitHub
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul
echo.

REM Change to repository directory
cd /d "%~dp0"

echo.
echo ============================================
echo  STEP 1: UPDATE PRIVATE CATALOGUE
echo ============================================
echo.
call update-and-deploy.bat
if errorlevel 1 (
    echo.
    echo [ERROR] Private catalogue update failed!
    echo Fix the errors above before continuing.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  STEP 2: UPDATE PUBLIC PITCH PAGE
echo ============================================
echo.
call update-public-pitch.bat
if errorlevel 1 (
    echo.
    echo [WARNING] Public pitch update failed!
    echo Private catalogue was updated successfully.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  ALL UPDATES COMPLETE!
echo ============================================
echo.
echo [SUCCESS] Both repositories updated and deployed
echo.
echo Private Catalogue: https://github.com/osahmed/aimy-catalogue-internal
echo.
echo Public Pitch Deployments:
echo  - Vercel (Primary):     https://aimy-pitch-report.vercel.app
echo  - GitHub Pages (Backup): https://osahmed.github.io/aimy-pitch-public/
echo.
echo NOTE: Vercel auto-deploys from private repo (instant)
echo       GitHub Pages deployment takes 1-2 minutes.
echo.
pause
