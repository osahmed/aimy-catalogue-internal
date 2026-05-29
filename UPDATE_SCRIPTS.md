# Update Scripts Documentation

## Overview

The update workflow is now a single catalogue update path:

| Script | Purpose | What It Does |
|--------|---------|--------------|
| `update-and-deploy.bat` | Main repo update | Fetches Jira data through `ATLASSIAN_API_TOKEN`, regenerates catalogue files, commits, and pushes |
| `update-all.bat` | Compatibility wrapper | Calls `update-and-deploy.bat` |
| `update repo.bat` | Desktop launcher | Opens the project and runs the repo update workflow |

## Quick Start

Double-click `update repo.bat` from the Desktop.

This will:

1. Fetch latest Jira issues using the credentials in `.env`.
2. Regenerate sanitized catalogue JSON.
3. Stage the catalogue website and data outputs.
4. Commit and push changes to GitHub.

## Requirements

- `.env` file with Jira credentials:
  - `ATLASSIAN_SITE`
  - `ATLASSIAN_EMAIL`
  - `ATLASSIAN_API_TOKEN`
  - `JIRA_PROJECT_KEY`
- Python 3 installed and available in PATH.
- Git authentication configured.

## Troubleshooting

### "Python not found"

Install Python 3 from https://www.python.org/downloads/ or ensure Python is in PATH.

### ".env file not found"

Copy `.env.example` to `.env` and add your Jira credentials:

```bat
copy .env.example .env
notepad .env
```

### "Failed to fetch Jira data through the API token"

Check `ATLASSIAN_SITE`, `ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN`, and `JIRA_PROJECT_KEY` in `.env`.

### "Git push failed"

Check your internet connection and GitHub authentication:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## What Gets Updated

- `catalogue-public.json`
- `data/catalogue-public.json`
- `data/catalogue-internal-evidence.json`
- `aimy-catalogue-site/catalogue-public.json`
- `index.html`
- `aimy-catalogue-site/index.html`

## Notes

- Credentials stay in `.env` and are never committed.
- `jira_issues_cache.json` is refreshed locally from Jira and remains git-ignored.
- The standalone one-page pitch deployment has been removed from the update workflow.
