# 🚀 GitHub Push Guide — Jira Replication Project

## ✅ Pre-Push Security Checklist

**All security requirements have been satisfied:**

- ✅ `.env` and `.env.*` files are in `.gitignore`
- ✅ `.env.example` template created (safe to commit)
- ✅ `jira_issues_cache.json` excluded (contains emails, account IDs)
- ✅ `aimy-catalogue-site/catalogue-data.json` excluded (raw Jira data)
- ✅ `aimy-catalogue-site/internal-review-notes.md` excluded (internal notes)
- ✅ Security scanner script created (`security-check.sh`)
- ✅ No API tokens in committed files (verified)
- ✅ No email addresses in committed code (verified)
- ✅ No Atlassian account IDs in committed files (verified)
- ✅ Git repository initialized with clean commit
- ✅ README with security documentation added

**Committed files (sanitized):**
```
✅ .env.example                          # Safe template
✅ .gitignore                            # Security rules
✅ README.md                             # Documentation
✅ security-check.sh                     # Pre-commit scanner
✅ check_jira_endpoints.py               # API testing (no secrets)
✅ test_jira_search.py                   # Search testing (no secrets)
✅ aimy-catalogue-site/index.html        # Customer-safe catalogue
✅ aimy-catalogue-site/catalogue-content.md
✅ aimy-catalogue-site/site-map.md
✅ atlassian-creator/SKILL.md            # Skill definitions
✅ atlassian-creator/references/*.md     # Reference docs
```

**Excluded files (sensitive - NOT in repo):**
```
🔒 .env                                  # Contains API tokens
🔒 jira_issues_cache.json                # Contains emails, account IDs
🔒 aimy-catalogue-site/catalogue-data.json
🔒 aimy-catalogue-site/internal-review-notes.md
```

---

## 📋 Step-by-Step: Push to Private GitHub Repo

### Option 1: Create New Private Repo (Recommended)

1. **Create the private repository on GitHub:**

   Go to: https://github.com/new

   - **Repository name**: `jira-replication` (or `aimy-catalogue-internal`)
   - **Description**: "Internal Jira replication tools and AiMY catalogue generation (PRIVATE)"
   - **Visibility**: 🔒 **Private** (CRITICAL - DO NOT make public)
   - **Initialize**: Do NOT add README, .gitignore, or license (we already have them)
   
   Click **"Create repository"**

2. **Add GitHub remote:**

   ```bash
   cd "/c/Users/osama.ramadan/OneDrive - FlairsTech for Software Development/Projects/Jira replication"
   
   # Replace YOUR_ORG with your GitHub org or username
   git remote add origin https://github.com/YOUR_ORG/jira-replication.git
   ```

3. **Push to GitHub:**

   ```bash
   git branch -M main
   git push -u origin main
   ```

4. **Verify repository settings:**

   - Go to repo **Settings** → **General**
   - Confirm **"Private"** badge is visible
   - Under **Danger Zone**, verify repository is private

---

### Option 2: Push to Existing Private Repo

If you already have a private FlairsTech organization repo:

```bash
cd "/c/Users/osama.ramadan/OneDrive - FlairsTech for Software Development/Projects/Jira replication"

# Add your existing repo URL
git remote add origin https://github.com/flairstech/jira-replication.git

# Push
git branch -M main
git push -u origin main
```

---

## 🛡️ Post-Push Verification

After pushing, run these checks:

### 1. Verify Repository Privacy

```bash
# Check if repo is private via GitHub API
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/YOUR_ORG/jira-replication | grep '"private"'

# Should return: "private": true
```

Or manually check: `https://github.com/YOUR_ORG/jira-replication/settings`

### 2. Scan for Accidentally Committed Secrets

```bash
# Clone fresh copy and scan
cd /tmp
git clone https://github.com/YOUR_ORG/jira-replication.git test-scan
cd test-scan

# Check for secrets in git history
git log -p | grep -iE "ATATT[a-zA-Z0-9_-]{80,}"
git log -p | grep -iE "accountId.*[a-f0-9]{24}"
git log -p | grep -E "@flairstech\.com"

# Should return NO results
```

### 3. Verify .gitignore is Working

```bash
cd "/c/Users/osama.ramadan/OneDrive - FlairsTech for Software Development/Projects/Jira replication"

# These commands should return empty (files ignored)
git status --ignored | grep "\.env$"
git status --ignored | grep "jira_issues_cache.json"
git status --ignored | grep "catalogue-data.json"
```

### 4. Test Security Scanner Locally

```bash
cd "/c/Users/osama.ramadan/OneDrive - FlairsTech for Software Development/Projects/Jira replication"

# Run security check
./security-check.sh

# Should output: "✅ Security check passed"
```

---

## 🚨 If Secrets Were Accidentally Committed

If you discover secrets in git history after pushing:

### Nuclear Option (Small Repo):

```bash
# WARNING: This rewrites history and requires force push

# Remove sensitive file from all history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (DANGEROUS - coordinate with team)
git push origin --force --all

# Rotate compromised credentials immediately
# Go to: https://id.atlassian.com/manage-profile/security/api-tokens
# Revoke the exposed token and generate a new one
```

### Better Option:

1. **Delete the repository entirely** on GitHub
2. **Rotate all exposed credentials** immediately
3. **Re-create the repository** following this guide
4. **Push clean history** without the sensitive commits

---

## 📊 Repository Access Control

### Recommended Team Access

- **Admin**: Engineering leadership only
- **Write**: AiMY platform team members
- **Read**: Product managers with NDA (if needed)

### Setting Collaborator Access

```
Repository Settings → Collaborators and teams → Add people
```

Only grant access to:
- Team members with signed NDAs
- Internal FlairsTech personnel
- Never make public or share with external parties

---

## 🔄 Future Updates

When adding new files in future commits:

1. **Before staging any files:**
   ```bash
   # Review what will be committed
   git status
   
   # Check for sensitive content
   grep -r "ATATT\|accountId\|@flairstech" <new-file>
   ```

2. **Run security check:**
   ```bash
   git add <files>
   ./security-check.sh  # Run manually before committing
   ```

3. **Commit and push safely:**
   ```bash
   git commit -m "Your commit message"
   git push origin main
   ```

---

## 📞 Emergency Contacts

**If secrets are leaked:**
1. **Immediately revoke** Atlassian API tokens: https://id.atlassian.com/manage-profile/security/api-tokens
2. **Notify** security team or engineering leadership
3. **Delete** the compromised repository
4. **Rotate** all related credentials

**Questions about repository access?**
- Contact: FlairsTech Engineering Leadership
- Security concerns: Follow internal security incident protocol

---

## ✨ Summary

**You are ready to push!**

Your repository is:
- ✅ Properly sanitized
- ✅ Security-reviewed
- ✅ Git-ignored correctly
- ✅ Documentation complete
- ✅ Safe for private GitHub hosting

**Next command:**

```bash
# Create repo on GitHub (set to Private), then run:
cd "/c/Users/osama.ramadan/OneDrive - FlairsTech for Software Development/Projects/Jira replication"
git remote add origin https://github.com/YOUR_ORG/jira-replication.git
git branch -M main
git push -u origin main
```

**⚠️ CRITICAL REMINDER: Repository must be PRIVATE — never public!**
