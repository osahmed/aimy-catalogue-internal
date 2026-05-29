@echo off
REM ============================================
REM AiMY Complete Update Script
REM ============================================
REM This master script:
REM 1. Fetches latest Jira data through the API token in .env
REM 2. Updates the catalogue repository
REM 3. Deploys changes to GitHub
REM ============================================

echo.
echo ============================================
echo   AiMY COMPLETE UPDATE - ALL REPOS
echo ============================================
echo.
echo This will:
echo  - Fetch latest Jira data through ATLASSIAN_API_TOKEN
echo  - Update the catalogue repository
echo  - Push all changes to GitHub
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul
echo.

REM Change to repository directory
cd /d "%~dp0"

echo.
echo ============================================
echo  UPDATE CATALOGUE REPOSITORY
echo ============================================
echo.
call update-and-deploy.bat
if errorlevel 1 (
    echo.
    echo [ERROR] Catalogue update failed!
    echo Fix the errors above before continuing.
    pause
    exit /b 1
)

echo.
echo ============================================
echo  UPDATE COMPLETE!
echo ============================================
echo.
echo [SUCCESS] Catalogue repository updated and deployed
echo.
echo Repository: https://github.com/osahmed/aimy-catalogue-internal
echo Deployment: https://aimy-pitch-report.vercel.app
echo.
echo NOTE: Vercel auto-deploys from private repo (instant)
echo.
pause
