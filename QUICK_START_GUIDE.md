# 🚀 Quick Start Guide - AiMY Catalogue Updates

## 🎯 Easiest Method (Recommended)

### On Your Desktop

Find and double-click:

```
🔄 Update AiMY Catalogue.bat
```

**That's it!** This will:
- ✅ Fetch latest Jira data
- ✅ Update private repository
- ✅ Update public pitch page
- ✅ Push everything to GitHub

---

## 📂 Alternative Methods

### From Repository Folder

Navigate to: `C:\Users\osama.ramadan\Documents\aimy-catalogue-internal\`

Then double-click one of these:

| File | What It Does |
|------|--------------|
| **`update-all.bat`** | **Everything** - Complete update workflow |
| `update-and-deploy.bat` | Only private catalogue (Jira → GitHub) |
| `update-public-pitch.bat` | Only public pitch page |

---

## ⏱️ How Long Does It Take?

| Step | Time |
|------|------|
| Fetch Jira data | 5-10 seconds |
| Commit & push | 2-5 seconds |
| GitHub Pages deploy | 1-2 minutes |
| **Total** | **~2 minutes** |

---

## ✅ What You'll See

The script will show:

```
========================================
 AiMY COMPLETE UPDATE - ALL REPOS
========================================

[1/5] Changed to repository directory
[2/5] Fetching latest Jira data...
[SUCCESS] Jira data fetched successfully

[3/5] Changes detected
[4/5] Staging changes...
[5/5] Committing and pushing to GitHub...

========================================
 ALL UPDATES COMPLETE!
========================================

Private Catalogue: https://github.com/osahmed/aimy-catalogue-internal
Public Pitch Page: https://osahmed.github.io/aimy-pitch-public/
```

---

## 🔍 Verify Updates

### Private Repository
Visit: https://github.com/osahmed/aimy-catalogue-internal/commits/main
- You should see a new commit with today's date

### Public Pitch Page
Visit: https://osahmed.github.io/aimy-pitch-public/
- Wait 1-2 minutes after script completes
- Refresh the page (Ctrl+F5 for hard refresh)

---

## ❌ Troubleshooting

### "Python not found"
**Solution**: Install Python from https://www.python.org/downloads/

### ".env file not found"
**Solution**: 
1. Copy `.env.example` to `.env`
2. Add your Jira credentials
3. Save the file

### "Git push failed"
**Solution**: Check your internet connection and GitHub authentication

### No changes detected
**Solution**: This is normal! It means Jira data hasn't changed since last update

---

## 📝 When to Run This

Run the update script:
- ✅ After making changes to Jira tickets
- ✅ Before sharing the pitch page with clients
- ✅ Weekly to keep catalogue fresh
- ✅ Anytime you want latest data

---

## 🔐 Security

- ✅ All credentials stay in `.env` (never committed)
- ✅ Only sanitized data goes to GitHub
- ✅ Private repository stays private
- ✅ Public pitch page has no sensitive data

---

## 💡 Pro Tips

1. **Run it regularly** - Keep data fresh
2. **Check the output** - Watch for errors
3. **Wait for deployment** - GitHub Pages takes 1-2 minutes
4. **Hard refresh browser** - Press Ctrl+F5 to see changes

---

## 📞 Need Help?

See full documentation: `UPDATE_SCRIPTS.md`

Or check:
- Repository structure: `README.md`
- Security guidelines: `SECURITY_AUDIT_REPORT.md`

---

**Last Updated**: 2026-05-25
