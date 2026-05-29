# AiMY Catalogue - Deployment Map

## Architecture

```text
Jira (source data)
  |
  | scripts/refresh-catalogue.py
  | uses ATLASSIAN_EMAIL + ATLASSIAN_API_TOKEN from .env
  v
Private repository: aimy-catalogue-internal
  |
  | Git push from update-and-deploy.bat / update repo.bat
  v
Vercel deployment
  |
  v
https://aimy-pitch-report.vercel.app
```

## Live URL

Use this URL for catalogue sharing:

```text
https://aimy-pitch-report.vercel.app
```

The standalone one-page pitch and GitHub Pages backup workflow have been retired.

## Update Flow

```text
Jira update
  -> run update repo.bat
  -> fetch current Jira issues through the API token
  -> regenerate sanitized catalogue JSON
  -> commit and push repository changes
  -> Vercel auto-deploys from GitHub
```

## Access Control

| Resource | Visibility | Who Can Access |
|----------|------------|----------------|
| Private repo | Private | Authorized collaborators |
| Vercel catalogue | Public URL | Anyone with the URL |
| Jira data | Private | FlairsTech team only |
| `.env` credentials | Local only | Current machine only |

## Update Checklist

- [ ] `.env` contains valid Atlassian credentials.
- [ ] `update repo.bat` completes without Jira API errors.
- [ ] Git commit is pushed to `main`.
- [ ] Vercel deployment reflects the latest catalogue.

## Scripts

```bat
update-and-deploy.bat
```

Main update workflow.

```bat
update-all.bat
```

Compatibility wrapper for the same workflow.

```bat
update repo.bat
```

Desktop launcher for the main workflow.
