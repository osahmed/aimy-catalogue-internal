# Cognito SSO Onboarding Runbook (for any new app)

How to stand up a new app gated by AWS Cognito + corporate Azure SSO, the same
way `aimy-catalogue-internal-617r` is gated — **without the back-and-forth.**

Hand the **"Request to IT"** block below to whoever owns AWS Cognito + Azure AD.
It contains everything they need in one shot.

---

## The 3 places things get configured (and who owns each)

This is the mental model. Most loops happen because these get confused.

| # | Where | What lives here | Owner |
|---|-------|-----------------|-------|
| 1 | **Cognito app client** | App's callback URL, sign-out URL, OAuth grant, scopes, **which IdPs are attached** | IT (Cognito) |
| 2 | **Azure AD app registration** | The `…/idpresponse` reply URL so Azure can return to Cognito | IT (Azure) |
| 3 | **Our app (Vercel)** | The 6–7 env vars + the auth code | Us |

> **The two URLs people mix up:**
> - Cognito app client needs **our app's** callback: `https://<app-domain>/api/auth/callback`
> - Azure app registration needs **Cognito's** reply URL: `https://<cognito-domain>/idpresponse`
> These are different URLs in different consoles. Both are required.

---

## ✅ Request to IT (copy/paste this whole block)

> We are launching a new app at **`https://<APP_DOMAIN>`** that should be gated by
> our corporate Azure SSO through Cognito, exactly like the aimyk-dashboard /
> aimy-catalogue apps. Please provide / configure the following on user pool
> **`<USER_POOL_ID>`** (region `us-east-1`):
>
> **A. Create (or reuse) a Cognito app client** and give us:
>  1. App client **ID**
>  2. App client **secret** (we use a confidential client)
>  3. The **Cognito Hosted UI domain** (e.g. `https://<prefix>.auth.us-east-1.amazoncognito.com`)
>  4. The **exact Identity Provider name** of the Azure federation as it appears in
>     Cognito (case-sensitive — the same one the existing dashboards use)
>
> **B. On that app client, set:**
>  - **Allowed callback URL:** `https://<APP_DOMAIN>/api/auth/callback`
>  - **Allowed sign-out URL:** `https://<APP_DOMAIN>/`
>  - **OAuth grant type:** Authorization code grant
>  - **OpenID Connect scopes:** `openid`, `email`, `profile` (add `phone` if needed)
>  - **Identity providers:** ✅ enable the **Azure corporate IdP** on this client
>    (this is what makes "Sign in with corporate account" appear / lets us force it)
>
> **C. On the Azure AD app registration backing the federation**, confirm the
> Cognito reply URL is allowed (usually already there for existing apps):
>  - `https://<cognito-domain>/idpresponse`
>
> **D. If we add a custom domain later** (e.g. `app.aimy.flairstech.com`), we will
> send the new URLs to add to **both** the Cognito callback list **and** wherever
> APP_DOMAIN appears.

Fill in before sending:
- `<APP_DOMAIN>` — the app's public hostname (no trailing slash)
- `<USER_POOL_ID>` — e.g. `us-east-1_3iBxA3reL`

---

## What we configure on our side (Vercel) — no IT needed

Once IT returns the values, set these env vars on the Vercel **Production** env
(`vercel env add <NAME> production`) and deploy. The auth code is reusable as-is:

| Env var | Value |
|---------|-------|
| `COGNITO_DOMAIN` | Hosted UI domain, no trailing slash |
| `COGNITO_ISSUER` | `https://cognito-idp.us-east-1.amazonaws.com/<USER_POOL_ID>` |
| `COGNITO_CLIENT_ID` | from IT |
| `COGNITO_CLIENT_SECRET` | from IT — **set via `vercel env add`, never commit** |
| `APP_BASE_URL` | `https://<APP_DOMAIN>` |
| `SESSION_SECRET` | generate: `node -e "console.log(require('crypto').randomBytes(48).toString('base64url'))"` |
| `COGNITO_IDP_NAME` | the IdP name from IT — set this to **force straight-to-Azure** (skip the Cognito form). Leave unset to show the Cognito page with an SSO button. |

Reusable files to copy into the new app (unchanged):
`middleware.js`, `lib/auth.js`, `api/auth/{login,callback,logout,me}.js`, `package.json` (dep: `jose`).

---

## Verify (one command, tells you instantly which leg is wrong)

```bash
curl -s -o /dev/null -D - \
 "https://<cognito-domain>/oauth2/authorize?response_type=code&client_id=<CLIENT_ID>&redirect_uri=https%3A%2F%2F<APP_DOMAIN>%2Fapi%2Fauth%2Fcallback&scope=openid+email+profile&state=x&nonce=y&code_challenge=zZ&code_challenge_method=S256" \
 | grep -i ^location
```

| Result | Meaning | Fix |
|--------|---------|-----|
| `…/error?error=redirect_mismatch` | Callback URL not on the Cognito app client | IT: add it (step B) |
| `…/login?...` | ✅ Working — reaches the sign-in page | — |
| Login page has **no** "corporate account" button | IdP not attached to this app client | IT: enable IdP (step B) |
| Error **after** Azure login (on return) | Azure `idpresponse` URL or attribute mapping | IT: step C |

---

## The two gotchas that caused loops this time (avoid them)

1. **Azure `idpresponse` ≠ Cognito callback URL.** Adding the reply URL to Azure
   does **not** fix `redirect_mismatch` — that's a Cognito app-client setting.
   Both must be done, in different consoles.
2. **Federation must be attached to *each* app client.** A working SSO on one app
   does not mean a new app client has the IdP enabled. It's a per-client checkbox.
