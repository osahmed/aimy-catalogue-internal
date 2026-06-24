@echo off
REM ============================================================
REM  AiMY Catalogue - Full Update & Deploy Pipeline
REM ============================================================
REM  Jira is evidence. The website is the pitch.
REM
REM  This script runs the FULL transformation pipeline:
REM    1. Fetch Jira updates (secure .env credentials)
REM    2. Humanize + classify into a curated, customer-safe catalogue
REM    3. Generate public + private (evidence / review) data files
REM    4. Validate that NO internal Jira data leaked (hard fail)
REM    5. Show a summary
REM    6. Ask for confirmation BEFORE publishing
REM    7. Push only customer-safe files to GitHub
REM    8. Deploy the customer-safe site to Vercel (production)
REM
REM  Live site : https://aimy-catalogue-internal-617r.vercel.app/
REM  Vercel project: aimy-catalogue-internal-617r
REM    org    = team_zau3neWoVzklLuacmBS4FoKF
REM    project= prj_0St3XYJ6FQ8vyL4u2aSlbIV0ctRD
REM  Internal files are blocked from deploy by .vercelignore.
REM
REM  AUTH: The site is gated by AWS Cognito SSO (middleware.js + api/auth/*).
REM  The deploy ships these functions automatically. The required Cognito env
REM  vars (COGNITO_DOMAIN, COGNITO_ISSUER, COGNITO_CLIENT_ID,
REM  COGNITO_CLIENT_SECRET, APP_BASE_URL, SESSION_SECRET) live in the Vercel
REM  PROJECT settings (Production) - NOT in this repo. If those are missing,
REM  the live site returns a login/500 loop. Manage them with:
REM    vercel env ls production
REM    vercel env add <NAME> production
REM ============================================================

echo.
echo ========================================
echo   AiMY Catalogue Update Pipeline
echo ========================================
echo.

cd /d "%~dp0"
echo [1/6] Working directory: %CD%
echo.

if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Create .env with your Jira credentials. See .env.example.
    pause
    exit /b 1
)

REM --- Run the full pipeline. It fetches Jira, curates, writes 3 files, ---
REM --- and runs the safety check. It exits non-zero if a leak is found. ---
echo [2/6] Running transformation pipeline (fetch -^> humanize -^> validate)...
echo.
python scripts\refresh-catalogue.py
if errorlevel 1 (
    echo.
    echo [ABORTED] Pipeline failed or safety check detected a leak.
    echo Nothing was pushed. Review the output above and internal-review-notes.md.
    pause
    exit /b 1
)
echo.

REM --- Show what changed (customer-safe files only are tracked) ---
echo [3/6] Git status:
git status --short
echo.

git diff --quiet
if %errorlevel% equ 0 (
    git diff --cached --quiet
    if %errorlevel% equ 0 (
        echo [INFO] No changes detected. Repository is already up to date.
        pause
        exit /b 0
    )
)

REM --- Confirmation gate: human must approve before publishing ---
echo [4/7] Review the summary above.
echo.
echo The following CUSTOMER-SAFE files will be committed and pushed:
echo   - catalogue-public.json
echo   - data\catalogue-public.json
echo   - aimy-catalogue-site\catalogue-public.json
echo   - index.html
echo   - aimy-catalogue-site\index.html
echo.
echo Internal files (evidence, review-needed, cache) are gitignored and stay local.
echo.
set /p CONFIRM="Publish customer-safe catalogue (GitHub + Vercel)? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo.
    echo [CANCELLED] Nothing published. Local files are updated for your review.
    pause
    exit /b 0
)

REM --- Stage ONLY customer-safe files. Never 'git add data/' wholesale. ---
echo.
echo [5/7] Staging customer-safe files...
git add catalogue-public.json
git add data\catalogue-public.json
git add index.html
git add aimy-catalogue-site\index.html
git add aimy-catalogue-site\catalogue-public.json

REM Auth layer (safe to re-stage; only commits when changed). The real
REM secrets live in Vercel env, never in these files.
git add package.json middleware.js lib\auth.js api\auth\*.js .env.example
git add vercel.json .vercelignore .gitignore

for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)

echo [6/7] Committing and pushing to GitHub...
git commit -m "Update AiMY customer catalogue from Jira - %mydate% %mytime%" -m "Curated, safety-checked pitch catalogue. Internal Jira evidence kept private."
if errorlevel 1 (
    echo [ERROR] Commit failed!
    pause
    exit /b 1
)

git push origin main
if errorlevel 1 (
    echo [ERROR] Push failed! Check your connection and GitHub authentication.
    pause
    exit /b 1
)

REM --- Deploy the customer-safe site to Vercel production. ---
REM     .vercelignore keeps internal files (evidence, cache, scripts, .env) out.
REM     Targets the aimy-catalogue-internal-617r project explicitly via env vars,
REM     so it does not depend on the local .vercel link.
echo.
echo [7/7] Deploying to Vercel production...
where vercel >nul 2>nul
if errorlevel 1 (
    echo [WARN] Vercel CLI not found. Skipping deploy.
    echo        Install with: npm i -g vercel   then re-run, or deploy manually.
    goto :done
)
set "VERCEL_ORG_ID=team_zau3neWoVzklLuacmBS4FoKF"
set "VERCEL_PROJECT_ID=prj_0St3XYJ6FQ8vyL4u2aSlbIV0ctRD"
call vercel deploy --prod --yes
if errorlevel 1 (
    echo [ERROR] Vercel deploy failed! GitHub push succeeded; deploy did not.
    echo         Check 'vercel login' and project access, then re-run deploy.
    pause
    exit /b 1
)

:done
echo.
echo ========================================
echo   UPDATE COMPLETE - catalogue published
echo   Live: https://aimy-catalogue-internal-617r.vercel.app/
echo ========================================
echo.
pause
