# 🗺️ AiMY Catalogue - Deployment Map

## 📊 Complete Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    JIRA (Source Data)                            │
│                  FlairsTech Internal                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ refresh-catalogue.py
                         │ (update-and-deploy.bat)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         Private Repository (aimy-catalogue-internal)             │
│              https://github.com/osahmed/aimy-catalogue-internal  │
│                                                                   │
│  Contains:                                                        │
│  ✓ Full catalogue data (catalogue-public.json)                  │
│  ✓ Main index.html (full catalogue interface)                   │
│  ✓ one-page-pitch.html                                          │
│  ✓ Jira integration scripts                                     │
│  ✓ Automation .bat files                                        │
│  ✓ Internal documentation                                       │
│                                                                   │
│  Status: PRIVATE ✅                                              │
└────────┬────────────────────────────┬───────────────────────────┘
         │                            │
         │ Auto-deploy                │ Manual sync
         │ (Vercel)                   │ (update-public-pitch.bat)
         │                            │
         ▼                            ▼
┌──────────────────────┐    ┌──────────────────────────────────┐
│  Vercel Deployment   │    │   Public GitHub Repository       │
│  (PRIMARY)           │    │   (BACKUP)                       │
│                      │    │                                  │
│  🌐 aimy-pitch-      │    │   aimy-pitch-public              │
│     report.vercel    │    │   github.com/osahmed/            │
│     .app             │    │   aimy-pitch-public              │
│                      │    │                                  │
│  ✓ Auto-deploys      │    │   ✓ Manual updates               │
│  ✓ Instant updates   │    │   ✓ GitHub Actions               │
│  ✓ Global CDN        │    │   ✓ 1-2 min deploy time          │
│  ✓ Production-ready  │    │                                  │
│                      │    │   Status: PUBLIC ✅              │
│  Status: PUBLIC ✅   │    │                                  │
└──────────────────────┘    └──────────┬───────────────────────┘
                                       │
                                       │ GitHub Pages
                                       ▼
                            ┌──────────────────────────────────┐
                            │   GitHub Pages Deployment        │
                            │                                  │
                            │   🌐 osahmed.github.io/          │
                            │      aimy-pitch-public           │
                            │                                  │
                            │   Status: PUBLIC ✅              │
                            └──────────────────────────────────┘
```

## 🌐 Live URLs

### For Public Sharing (Recommended Priority)

1. **Primary:** https://aimy-pitch-report.vercel.app ⚡
   - Use this for clients and stakeholders
   - Fastest performance
   - Auto-updates from private repo
   - Production-grade hosting

2. **Backup:** https://osahmed.github.io/aimy-pitch-public/
   - Alternative if Vercel is down
   - GitHub's infrastructure
   - Requires manual sync

### Internal Only

- **Private Repository:** https://github.com/osahmed/aimy-catalogue-internal 🔒
  - Full catalogue system
  - Jira integration
  - Source of truth

## 🔄 Update Flow

### Automatic (Vercel)
```
Jira Update → Run update-and-deploy.bat → Push to GitHub → Vercel auto-deploys
                                                            (instant, ~10 seconds)
```

### Manual (GitHub Pages)
```
Jira Update → Run update-all.bat → Push to both repos → GitHub Pages deploys
                                                         (1-2 minutes)
```

## 🔐 Access Control

| Resource | Visibility | Who Can Access |
|----------|-----------|----------------|
| Private Repo | Private | You + authorized collaborators |
| Public Repo | Public | Anyone (read-only) |
| Vercel Site | Public | Anyone via URL |
| GitHub Pages | Public | Anyone via URL |
| Jira Data | Private | FlairsTech team only |

## 📝 Update Checklist

When you run the update scripts:

- [ ] Jira data fetched successfully
- [ ] Private repo updated and pushed
- [ ] Vercel auto-deploys (check in ~10 seconds)
- [ ] GitHub Pages synced (if using update-all.bat)
- [ ] Both public URLs showing latest version

## 🚀 Deployment Methods

### Method 1: Complete Update (Recommended)
```batch
update-all.bat
```
Updates everything: Private repo → Vercel → GitHub Pages

### Method 2: Private Only
```batch
update-and-deploy.bat
```
Updates only private repo (Vercel auto-syncs)

### Method 3: Public Pitch Only
```batch
update-public-pitch.bat
```
Syncs pitch to GitHub Pages backup only

## 🔗 Cross-References

All repositories and deployments are cross-linked in their READMEs:
- Private repo README → Links to both public deployments
- Public repo README → Links to both live sites
- Update scripts → Show all URLs after completion

## 📊 Performance Comparison

| Feature | Vercel | GitHub Pages |
|---------|--------|--------------|
| Deploy Speed | ~10 seconds | 1-2 minutes |
| Update Method | Auto (on push) | Manual sync required |
| CDN | Global | Global |
| Custom Domain | ✅ Yes (free) | ✅ Yes (free) |
| SSL/HTTPS | ✅ Auto | ✅ Auto |
| Best For | Production | Backup/fallback |

## 💡 Best Practices

1. **Always use Vercel URL** for client presentations
2. **Keep GitHub Pages as backup** in case Vercel has issues
3. **Run updates regularly** to keep data fresh
4. **Verify both URLs** after major updates
5. **Monitor Vercel dashboard** for deployment status

---

**Last Updated:** 2026-05-25  
**Maintained By:** Automated update scripts
