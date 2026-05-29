# URL Redirects

The standalone one-page pitch has been removed from the website.

Legacy paths now return visitors to the main catalogue homepage:

| Old URL | Current Destination |
|---------|---------------------|
| `/one-page-pitch` | `/` |
| `/one-page-pitch.html` | `/` |

The old generated Vercel subdomain redirects to the current catalogue deployment:

```text
https://aimy-catalogue-internal-617r.vercel.app/*
  -> https://aimy-pitch-report.vercel.app/:splat
```

The active catalogue URL is:

```text
https://aimy-pitch-report.vercel.app
```
