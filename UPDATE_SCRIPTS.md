# Update Scripts Documentation

## 📋 Overview

Three automated .bat files to manage Jira updates and GitHub deployments:

| Script | Purpose | What It Does |
|--------|---------|--------------|
| **`update-and-deploy.bat`** | Update private catalogue only | Fetches Jira data → Commits → Pushes to private repo |
| **`update-public-pitch.bat`** | Update public pitch page only | Copies pitch → Commits → Pushes to public repo |
| **`update-all.bat`** | **Complete update** (Recommended) | Runs both scripts above in sequence |

## 🚀 Quick Start

### Option 1: Update Everything (Recommended)
Double-click: **`update-all.bat`**

This will:
1. ✅ Fetch latest Jira data
2. ✅ Update private catalogue repository
3. ✅ Update public pitch page
4. ✅ Push all changes to GitHub

### Option 2: Update Private Catalogue Only
Double-click: **`update-and-deploy.bat`**

Use this when you want to update internal data without changing the public pitch page.

### Option 3: Update Public Pitch Page Only
Double-click: **`update-public-pitch.bat`**

Use this when you've manually edited `one-page-pitch.html` and want to deploy it.

## 📂 Requirements

### For Private Catalogue Updates
- `.env` file with Jira credentials (see `.env.example`)
- Python 3 installed
- Git authentication configured

### For Public Pitch Updates
- Public repository cloned at: `C:\Users\{YOUR_USERNAME}\Documents\aimy-pitch-public`
- Git authentication configured

## 🔐 Security Notes

- These scripts only push to repositories you have access to
- `.env` file is git-ignored and never committed
- All commits include timestamp and automation signature
- No credentials are exposed in commit messages

## 🛠️ Troubleshooting

### "Python not found"
Install Python 3: https://www.python.org/downloads/
Or ensure Python is in your PATH environment variable.

### "Git push failed"
Check your GitHub authentication:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### ".env file not found"
Copy `.env.example` to `.env` and add your Jira credentials:
```bash
copy .env.example .env
notepad .env
```

### "Public repository not found"
Clone the public repository:
```bash
cd %USERPROFILE%\Documents
git clone https://github.com/osahmed/aimy-pitch-public.git
```

## 📝 What Gets Updated

### Private Repository (`aimy-catalogue-internal`)
- `catalogue-public.json` - Latest Jira data (sanitized)
- `index.html` - Main catalogue page
- `data/` - Internal data files

### Public Repository (`aimy-pitch-public`)
- `index.html` - One-page pitch (copied from `one-page-pitch.html`)

## 🕒 Deployment Timeline

1. **Immediate**: Changes committed and pushed to GitHub
2. **1-2 minutes**: GitHub Pages deployment completes
3. **5-10 minutes**: CDN cache updates globally

## 🔄 Automation Schedule (Optional)

To run updates automatically, you can:
1. Use Windows Task Scheduler
2. Set `update-all.bat` to run daily/weekly
3. Or manually run whenever Jira is updated

## 💡 Tips

- Run `update-all.bat` after major Jira updates
- Check the terminal output for errors
- Git will only push if there are actual changes
- Public pitch page is cached - may take a few minutes to refresh

## 📞 Support

For issues with:
- **Scripts**: Check this documentation
- **Jira data**: Verify `.env` credentials
- **GitHub**: Check repository permissions
- **Python**: Ensure dependencies installed

---

**Last Updated**: 2026-05-25
