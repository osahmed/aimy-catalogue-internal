#!/bin/bash
# Pre-commit security scanner for Jira Replication project
# Prevents accidental commits of secrets, credentials, and sensitive data

echo "🔍 Running security check..."

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track if any issues found
ISSUES_FOUND=0

# 1. Check for .env files
echo "Checking for .env files..."
if git diff --cached --name-only | grep -E "^\.env$|^\.env\.local$|\.env\..*$" | grep -v ".env.example"; then
    echo -e "${RED}❌ ERROR: .env file(s) detected in commit${NC}"
    echo "   These files contain secrets and must never be committed."
    ISSUES_FOUND=1
fi

# 2. Check for sensitive JSON files
echo "Checking for sensitive data files..."
if git diff --cached --name-only | grep -E "jira_issues_cache\.json|catalogue-data\.json|internal-review-notes\.md"; then
    echo -e "${RED}❌ ERROR: Sensitive data file detected in commit${NC}"
    echo "   These files contain internal information (emails, account IDs, internal notes)."
    ISSUES_FOUND=1
fi

# 3. Scan staged content for API tokens
echo "Scanning staged content for secrets..."
if git diff --cached | grep -iE "ATATT[a-zA-Z0-9_-]{80,}|api_token.*=.*ATATT"; then
    echo -e "${RED}❌ ERROR: Atlassian API token detected in commit${NC}"
    echo "   API tokens must never be committed to git."
    ISSUES_FOUND=1
fi

# 4. Check for email addresses
if git diff --cached | grep -iE "@flairstech\.com|@.*\.com" | grep -v "example\|template\|README"; then
    echo -e "${YELLOW}⚠️  WARNING: Email address detected in commit${NC}"
    echo "   Verify this is intentional (e.g., documentation) and not from Jira data."
    # Don't fail on this, just warn
fi

# 5. Check for Atlassian account IDs
if git diff --cached | grep -E "accountId.*[a-f0-9]{24}|712020:[a-f0-9-]{36}"; then
    echo -e "${RED}❌ ERROR: Atlassian account ID detected in commit${NC}"
    echo "   Account IDs are internal identifiers and should not be committed."
    ISSUES_FOUND=1
fi

# 6. Check for private Jira URLs
if git diff --cached | grep -E "flairstechdev\.atlassian\.net"; then
    echo -e "${YELLOW}⚠️  WARNING: Internal Jira URL detected${NC}"
    echo "   Verify this is safe for external visibility."
    # Don't fail, but warn
fi

# 7. Verify .gitignore exists and contains required entries
echo "Verifying .gitignore configuration..."
if [ ! -f .gitignore ]; then
    echo -e "${RED}❌ ERROR: .gitignore file missing${NC}"
    ISSUES_FOUND=1
elif ! grep -q "^\.env$" .gitignore || ! grep -q "jira_issues_cache\.json" .gitignore; then
    echo -e "${RED}❌ ERROR: .gitignore incomplete${NC}"
    echo "   Required entries: .env, jira_issues_cache.json, catalogue-data.json"
    ISSUES_FOUND=1
fi

# 8. Check for hardcoded credentials in Python files
if git diff --cached -- "*.py" | grep -iE "password.*=|token.*=.*['\"][^'\"]{20,}|api_key.*="; then
    echo -e "${YELLOW}⚠️  WARNING: Possible hardcoded credentials in Python files${NC}"
    echo "   Verify credentials are loaded from .env, not hardcoded."
fi

# Final result
echo ""
if [ $ISSUES_FOUND -eq 1 ]; then
    echo -e "${RED}❌ COMMIT BLOCKED: Security issues detected${NC}"
    echo ""
    echo "To fix:"
    echo "  1. Remove sensitive files: git reset HEAD <file>"
    echo "  2. Check .gitignore includes all sensitive files"
    echo "  3. Run: git status"
    echo ""
    exit 1
else
    echo -e "${GREEN}✅ Security check passed${NC}"
    echo ""
    exit 0
fi
