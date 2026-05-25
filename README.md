# Jira Replication & AiMY Catalogue Site

A private repository for managing Jira data replication and generating customer-facing catalogue websites from Atlassian/Jira project data.

## 🌐 Public Pitch Page
**Live Site:** [https://osahmed.github.io/aimy-pitch-public/](https://osahmed.github.io/aimy-pitch-public/)  
**Repository:** [aimy-pitch-public](https://github.com/osahmed/aimy-pitch-public)

This is the internal repository. For the public-facing one-page pitch, visit the link above.

## 🔒 Security Notice

This is a **private repository** containing tools for internal use only. The generated catalogue site is sanitized for customer viewing, but the source data and scripts contain FlairsTech internal workflows.

**Do not:**
- Make this repository public
- Share API tokens or credentials
- Deploy the raw Jira data publicly
- Include `.env` files in commits

## 📁 Project Structure

```
.
├── aimy-catalogue-site/        # Generated customer-facing catalogue website
│   ├── index.html              # Main catalogue interface
│   ├── catalogue-content.md    # Sanitized markdown content
│   ├── site-map.md            # Site structure overview
│   └── [excluded from git]
│       ├── catalogue-data.json      # Raw Jira data (contains internal info)
│       └── internal-review-notes.md # Internal team notes
│
├── atlassian-creator/          # Atlassian integration utilities
│   ├── SKILL.md               # Skill definition for automation
│   └── references/            # Reference documentation
│
├── check_jira_endpoints.py     # Jira API endpoint testing utility
├── test_jira_search.py         # Jira search functionality tests
├── .env.example               # Template for environment configuration
└── [excluded from git]
    ├── .env                   # Your actual credentials (NEVER commit)
    └── jira_issues_cache.json # Cached Jira responses (contains emails, IDs)
```

## 🚀 Setup

### Prerequisites

- Python 3.7+
- Atlassian/Jira API access
- Valid API token with appropriate permissions

### Installation

1. Clone this repository (private access only):
   ```bash
   git clone <private-repo-url>
   cd jira-replication
   ```

2. Create your `.env` file from the template:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` with your Atlassian credentials:
   - `ATLASSIAN_SITE`: Your Atlassian site (e.g., `yourcompany.atlassian.net`)
   - `ATLASSIAN_EMAIL`: Your Atlassian account email
   - `ATLASSIAN_API_TOKEN`: Your API token ([generate here](https://id.atlassian.com/manage-profile/security/api-tokens))
   - `JIRA_PROJECT_KEY`: The Jira project key to replicate

## 🔧 Usage

### Testing Jira Endpoints

Verify your Jira API connection:

```bash
python check_jira_endpoints.py
```

### Running Jira Search Tests

Test search functionality across API versions:

```bash
python test_jira_search.py
```

### Generating the Catalogue Site

The `aimy-catalogue-site/` directory contains a static HTML catalogue generated from Jira data. The site is designed for customer-facing use and excludes:

- Internal comments and notes
- Email addresses and account IDs
- Reporter/assignee personal information
- Private Jira URLs and internal links

**To view the catalogue:**

Open `aimy-catalogue-site/index.html` in a web browser.

## 🛡️ Security Best Practices

### Before Committing

1. **Never commit:**
   - `.env` or any environment files with credentials
   - `jira_issues_cache.json` (contains raw Jira API responses with emails, account IDs)
   - `aimy-catalogue-site/catalogue-data.json` (contains internal metadata)
   - `aimy-catalogue-site/internal-review-notes.md` (internal team notes)

2. **Always verify:**
   ```bash
   git status
   # Check that no sensitive files are staged
   
   grep -r "ATATT\|accountId\|@flairstech" .
   # Should return no results in tracked files
   ```

3. **Secret scanning:**
   ```bash
   # Check for accidentally committed secrets
   git log -p | grep -i "token\|password\|secret\|api_key"
   ```

### Data Sanitization

The catalogue generation process automatically:
- Removes email addresses from assignee/reporter fields
- Strips Atlassian account IDs
- Excludes internal comments
- Redacts private Jira instance URLs
- Separates internal review notes from customer content

### Repository Access

This repository should only be accessible to:
- FlairsTech engineering team members
- Authorized personnel with NDA agreements
- Team members working on AiMY product development

## 📊 Generated Outputs

### Customer-Safe Content

These files are safe for customer viewing:
- ✅ `aimy-catalogue-site/index.html` - Interactive catalogue interface
- ✅ `aimy-catalogue-site/catalogue-content.md` - Sanitized markdown
- ✅ `aimy-catalogue-site/site-map.md` - Navigation structure

### Internal-Only Content (Git-Ignored)

These files contain sensitive internal data:
- 🔒 `aimy-catalogue-site/catalogue-data.json` - Raw Jira data with emails/IDs
- 🔒 `aimy-catalogue-site/internal-review-notes.md` - Internal team notes
- 🔒 `jira_issues_cache.json` - Complete Jira API responses
- 🔒 `.env` - API credentials and configuration

## 🤝 Contributing

1. **Never push secrets** - Always check `git status` before committing
2. **Test locally** - Verify scripts work with your `.env` configuration
3. **Keep data fresh** - Periodically regenerate the catalogue from latest Jira data
4. **Document changes** - Update this README when adding new features

## 📝 License

Private/Internal Use Only - FlairsTech Proprietary

---

**Questions or Issues?**  
Contact the AiMY Platform team or Engineering Leadership.
