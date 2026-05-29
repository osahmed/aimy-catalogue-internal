@echo off
REM ============================================
REM AiMY Catalogue - Update & Deploy Script
REM ============================================
REM This script:
REM 1. Fetches latest Jira data through the API token in .env
REM 2. Regenerates catalogue files
REM 3. Commits and pushes to GitHub
REM ============================================

echo.
echo ========================================
echo  AiMY Catalogue Update Script
echo ========================================
echo.

REM Change to repository directory
cd /d "%~dp0"
echo [1/5] Changed to repository directory: %CD%
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please create .env with your Jira credentials.
    echo See .env.example for reference.
    pause
    exit /b 1
)

REM Run the Python refresh script
echo [2/5] Fetching latest Jira data through ATLASSIAN_API_TOKEN...
python scripts\refresh-catalogue.py
if errorlevel 1 (
    echo [ERROR] Failed to fetch Jira data!
    pause
    exit /b 1
)
echo [SUCCESS] Jira data fetched successfully
echo.

REM Check if there are any changes to commit
git diff --quiet
if %errorlevel% equ 0 (
    git diff --cached --quiet
    if %errorlevel% equ 0 (
        echo [INFO] No changes detected. Repository is up to date.
        echo.
        pause
        exit /b 0
    )
)

REM Show changes
echo [3/5] Changes detected:
git status --short
echo.

REM Stage all changes
echo [4/5] Staging changes...
git add catalogue-public.json
git add index.html
git add aimy-catalogue-site\index.html
git add aimy-catalogue-site\catalogue-public.json
git add data/
echo [SUCCESS] Changes staged
echo.

REM Create commit with timestamp
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)

echo [5/5] Committing and pushing to GitHub...
git commit -m "Update AiMY catalogue data from Jira - %mydate% %mytime%" -m "Automated update via update-and-deploy.bat" -m "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

if errorlevel 1 (
    echo [ERROR] Commit failed!
    pause
    exit /b 1
)

REM Push to GitHub
git push origin main
if errorlevel 1 (
    echo [ERROR] Push to GitHub failed!
    echo Please check your internet connection and GitHub authentication.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  UPDATE COMPLETE!
echo ========================================
echo.
echo [SUCCESS] Private repository updated: https://github.com/osahmed/aimy-catalogue-internal
echo.
pause
