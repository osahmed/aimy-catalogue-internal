# Quick Start Guide - AiMY Catalogue Updates

## Easiest Method

On your Desktop, double-click:

```text
update repo.bat
```

This will:

- Fetch latest Jira data through `ATLASSIAN_API_TOKEN`.
- Regenerate the sanitized catalogue.
- Commit and push the catalogue repository.
- Trigger the normal Vercel deployment from GitHub.

## From The Repository Folder

You can also run:

| File | What It Does |
|------|--------------|
| `update-and-deploy.bat` | Main Jira-to-catalogue update workflow |
| `update-all.bat` | Compatibility wrapper for the same workflow |

## Verify Updates

Visit: https://github.com/osahmed/aimy-catalogue-internal/commits/main

Then check the deployed catalogue:

```text
https://aimy-pitch-report.vercel.app
```

## Troubleshooting

### "Python not found"

Install Python from https://www.python.org/downloads/.

### ".env file not found"

Copy `.env.example` to `.env`, add your Jira credentials, and save the file.

### "Failed to fetch Jira data through the API token"

Check the `.env` values for `ATLASSIAN_SITE`, `ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN`, and `JIRA_PROJECT_KEY`.

### "Git push failed"

Check your internet connection and GitHub authentication.

### No changes detected

This is normal when Jira data has not changed since the last update.

## Security

- Credentials stay in `.env`.
- Raw Jira cache stays in `jira_issues_cache.json`, which is git-ignored.
- Only sanitized catalogue files are staged for deployment.
