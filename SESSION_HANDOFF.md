# Session Handoff — AiMY Catalogue + Cognito SSO

> Saved 2026-06-03 so work can resume after restarting the app.
> Read this top-to-bottom; the **"Resume here"** section at the end is the
> single open action.

---

## 1. What this project is

A customer-facing **AiMY pitch catalogue** website. Jira is the internal source
of truth (evidence); the website is the polished pitch. Do **not** expose raw
Jira data publicly. Two index.html files (root + `aimy-catalogue-site/`) render
from `catalogue-public.json`.

- Live site: **https://aimy-catalogue-internal-617r.vercel.app/**
- Vercel project: `aimy-catalogue-internal-617r`
  - org = `team_zau3neWoVzklLuacmBS4FoKF`
  - project = `prj_0St3XYJ6FQ8vyL4u2aSlbIV0ctRD`
  - (deploy with these as `VERCEL_ORG_ID` / `VERCEL_PROJECT_ID` env vars; the
    local `.vercel` link points at a *different* project, `aimy-pitch-report`)
- GitHub remote: `https://github.com/osahmed/aimy-catalogue-internal.git` (branch `main`)

---

## 2. Work completed this session

### A. Catalogue pipeline rebuild (DONE, deployed)
The old pipeline was a **Jira mirror** — it dumped all ~4,300 raw issues (bugs,
subtasks, `[Dynamic System]`, `Failed:` test titles) into the public site, and
the curated mappings used dead Jira keys (project is now `AIMYIMP`, 4,633 issues).

Rebuilt into a **curated, Epic-grounded pipeline**:
- `scripts/catalogue_map.py` — hand-written `CURATED_FEATURES` (24 features),
  each bound to live `AIMYIMP` epics by title substring (`epic_match`).
- `scripts/refresh-catalogue.py` — fetches Jira (incl. dates/fixVersions),
  binds curated features to live evidence, resolves display dates
  (fixVersion → resolution → updated), writes 3 files, runs a **real** safety
  check that hard-fails on any leak, regenerates `internal-review-notes.md`,
  prints a summary. LLM-draft scaffold (`maybe_draft_with_llm`) is a no-op
  unless `ANTHROPIC_API_KEY` is set.
- Outputs: `data/catalogue-public.json` (+ root + `aimy-catalogue-site/` copies),
  `data/catalogue-internal-evidence.json` (private), `data/catalogue-review-needed.json` (private).
- Both `index.html` renderers extended to show module badge, customer problem,
  what-changed, and display date.
- `.vercelignore` blocks all internal files from deploy (verified: evidence,
  cache, scripts, `.env`, notes all return **404** live).
- Run offline test anytime: `python scripts/refresh-catalogue.py --cache-only`
  (last run: 24 public features, 8 modules, 3,361 excluded, 886 review, safety PASSED).

### B. AWS Cognito SSO authentication (DONE on our side; ONE AWS step pending)
Static site → gated by Cognito SSO, enforced on **backend** (edge middleware),
not just the browser. OIDC Authorization Code + PKCE flow (ported from the
user's Flask/authlib snippet to Vercel serverless).

Files (all reusable, syntax-checked, 7/7 unit tests passed):
- `middleware.js` — edge gate; verifies signed `aimy_session` cookie on every
  route; no session → 302 to `/api/auth/login`. Matcher excludes `api/auth/` + favicon.
- `lib/auth.js` — jose HS256 session sign/verify, PKCE, id_token verify (JWKS),
  secure cookies (HttpOnly/Secure/SameSite=Lax). 8h session.
- `api/auth/login.js` — state+nonce+PKCE → redirect to Cognito; appends
  `identity_provider=<COGNITO_IDP_NAME>` if that env var is set.
- `api/auth/callback.js` — validate state → exchange code → verify id_token → set cookie.
- `api/auth/logout.js` — clear cookie → Cognito `/logout`.
- `api/auth/me.js` — returns `{email}` for the header UI.
- both `index.html` — header shows signed-in email + Log out; `fetch('/api/auth/me')`.
- `package.json` — dep `jose`.

Cognito facts:
- User pool `us-east-1_3iBxA3reL`, client `7qqsvrc3h0molhts9g0djemsvb`
  (confidential, has secret), region `us-east-1`.
- Hosted UI domain `https://us-east-13ibxa3rel.auth.us-east-1.amazoncognito.com`.
- SSO = federated **Azure AD** behind Cognito.

Env vars SET on Vercel Production (all 6, verified):
`COGNITO_DOMAIN`, `COGNITO_ISSUER`, `COGNITO_CLIENT_ID`, `COGNITO_CLIENT_SECRET`,
`APP_BASE_URL`, `SESSION_SECRET`. (`COGNITO_IDP_NAME` NOT yet set — see resume.)
> Note: never paste the real client secret into `.env.example` (git-tracked).
> Set it only via `vercel env add COGNITO_CLIENT_SECRET production`.

Verified live:
- Logged-out `/`, `/catalogue-public.json`, `/aimy-catalogue-site/catalogue-public.json`
  all → **302 to login** (backend gating works — bytes never served).
- `/api/auth/login` → 302 to Cognito with full code+PKCE params.
- `/api/auth/me` (no cookie) → 401.
- Callback URL `…/api/auth/callback` IS registered in Cognito (fixed mid-session;
  `redirect_mismatch` is resolved — authorize now reaches the `/login` page).

### C. Docs written
- `SSO_ONBOARDING_RUNBOOK.md` — how to stand up any future SSO-gated app.
- (Email to IT was drafted in chat — not yet saved to a file; can save as
  `IT_SSO_REQUEST_EMAIL.md` if wanted.)
- `update-and-deploy.bat` — full pipeline + confirm-before-push + Vercel deploy;
  header documents the Cognito env vars; stages auth files too.

---

## 3. The blocker history (so we don't loop)

Three consoles, three jobs — keep them separate:
| Console | Needs | Status |
|---|---|---|
| **Cognito app client** | our `/api/auth/callback` URL **+ Azure IdP attached** | callback ✅ · **IdP attach ❌ pending** |
| **Azure app registration** | Cognito's `/idpresponse` reply URL | ✅ IT did this |
| **Vercel (us)** | env vars + auth code | ✅ done |

Two traps that caused loops:
1. Azure `idpresponse` ≠ Cognito callback URL — different URLs, different
   consoles, both required. Azure change did NOT fix `redirect_mismatch`.
2. Federation is **per-app-client**. Working SSO on the dashboard app does not
   mean our app client has the IdP enabled — it's a per-client checkbox. This is
   why our login currently shows username/password instead of the corporate
   "Sign in with corporate account" button.

I (Claude) cannot make AWS changes: the `AIMY_Analytics` IAM user gets
`AccessDeniedException` on all `cognito-idp:*` actions.

---

## 4. ▶ RESUME HERE — the one open action

**Goal:** make our app log in via the corporate Azure SSO (not the Cognito
username/password form), forced straight to Azure.

**Step 1 — Ask IT (Cognito console):**
> On user pool `us-east-1_3iBxA3reL`, app client `7qqsvrc3h0molhts9g0djemsvb`:
> enable / attach the **Azure corporate Identity Provider** (the same federation
> the aimyk-dashboard app uses), and tell me its **exact IdP name** (case-sensitive).

**Step 2 — Once IT confirms + gives the name, set it and redeploy:**
```bash
cd "<project root>"
export VERCEL_ORG_ID=team_zau3neWoVzklLuacmBS4FoKF
export VERCEL_PROJECT_ID=prj_0St3XYJ6FQ8vyL4u2aSlbIV0ctRD
printf '%s' "<EXACT_IDP_NAME>" | vercel env add COGNITO_IDP_NAME production
vercel deploy --prod --yes
```
(`api/auth/login.js` already appends `identity_provider=<name>` when the env var
is set — no code change needed.)

**Step 3 — Verify the live redirect goes straight to Azure:**
```bash
curl -s -o /dev/null -D - "https://aimy-catalogue-internal-617r.vercel.app/api/auth/login" | grep -i ^location
# then follow that Cognito URL; it should redirect to login.microsoftonline.com / Azure,
# NOT show the Cognito username form.
```

**Step 4 — Browser test (incognito):** visit the site → should bounce straight
to Azure corporate login → back to the catalogue with your email + Log out in
the header.

### Also still open (optional, lower priority):
- [ ] **Commit + push to GitHub.** The auth code, pipeline rebuild, runbook, and
      this handoff are deployed to Vercel but NOT yet committed to git. To do:
      `git add` the auth files + docs + catalogue files, commit, `git push origin main`.
      (The `update-and-deploy.bat` already stages the auth files; or do it manually.)
- [ ] Optionally save the IT email as `IT_SSO_REQUEST_EMAIL.md`.

---

## 5. Quick reference — useful commands

```bash
# Refresh catalogue offline (no Jira creds needed):
python scripts/refresh-catalogue.py --cache-only

# Leak audit of public JSON (must all be 0):
python -c "import re; s=open('catalogue-public.json',encoding='utf-8').read(); print('keys',len(re.findall(r'[A-Z]{2,}-[0-9]+',s)),'dynsys',s.count('[Dynamic System]'))"

# List Vercel prod env vars:
VERCEL_ORG_ID=team_zau3neWoVzklLuacmBS4FoKF VERCEL_PROJECT_ID=prj_0St3XYJ6FQ8vyL4u2aSlbIV0ctRD vercel env ls production

# Generate a session secret:
node -e "console.log(require('crypto').randomBytes(48).toString('base64url'))"

# Diagnose the Cognito leg (mismatch vs login page):
curl -s -o /dev/null -D - "https://us-east-13ibxa3rel.auth.us-east-1.amazoncognito.com/oauth2/authorize?response_type=code&client_id=7qqsvrc3h0molhts9g0djemsvb&redirect_uri=https%3A%2F%2Faimy-catalogue-internal-617r.vercel.app%2Fapi%2Fauth%2Fcallback&scope=openid+email+phone&state=x&nonce=y&code_challenge=zZ&code_challenge_method=S256" | grep -i ^location
```

See also: `SSO_ONBOARDING_RUNBOOK.md` (future apps), `AGENTS.md` / `README.md`
(project background).
