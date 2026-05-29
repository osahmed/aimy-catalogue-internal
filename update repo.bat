@echo off
REM ============================================
REM AiMY Catalogue - Desktop Update Launcher
REM ============================================
REM Runs the repository update workflow from any location.
REM Jira credentials are read from the repository .env file.
REM ============================================

setlocal

set "REPO_DIR=C:\Users\osama.ramadan\OneDrive - FlairsTech for Software Development\Projects\Jira replication"

echo.
echo ========================================
echo  AiMY Catalogue Repo Update
echo ========================================
echo.

if not exist "%REPO_DIR%\update-and-deploy.bat" (
    echo [ERROR] Repository update script not found:
    echo %REPO_DIR%\update-and-deploy.bat
    echo.
    pause
    exit /b 1
)

cd /d "%REPO_DIR%"
call update-and-deploy.bat
exit /b %ERRORLEVEL%
