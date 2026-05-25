# URL Redirects Configuration

## 🔄 Redirect Rules

All one-page-pitch URLs now redirect to the public GitHub Pages deployment.

### Active Redirects

| Old URL | New URL | Status |
|---------|---------|--------|
| `/one-page-pitch` | `https://osahmed.github.io/aimy-pitch-public/` | 301 Permanent |
| `/one-page-pitch.html` | `https://osahmed.github.io/aimy-pitch-public/` | 301 Permanent |
| `./one-page-pitch.html` (internal link) | `https://osahmed.github.io/aimy-pitch-public/` | External link |

### Legacy Support

Old Vercel subdomain patterns are also redirected:
```
https://aimy-catalogue-internal-617r.vercel.app/* 
  → https://osahmed.github.io/aimy-pitch-public/
```

## 📝 Implementation

### 1. Internal Links (`index.html`)
```html
<a href="https://osahmed.github.io/aimy-pitch-public/" 
   target="_blank" 
   style="color: var(--accent-magenta);">
   One-Page Pitch
</a>
```
- Opens in new tab
- Points directly to public GitHub Pages
- Consistent across all deployments

### 2. Vercel Redirects (`vercel.json`)
```json
{
  "redirects": [
    {
      "source": "/one-page-pitch",
      "destination": "https://osahmed.github.io/aimy-pitch-public/",
      "permanent": true
    },
    {
      "source": "/one-page-pitch.html",
      "destination": "https://osahmed.github.io/aimy-pitch-public/",
      "permanent": true
    }
  ]
}
```
- HTTP 301 (permanent redirect)
- SEO-friendly
- Browsers will cache the redirect

### 3. Fallback Redirects (`public/_redirects`)
```
/one-page-pitch https://osahmed.github.io/aimy-pitch-public/ 301
/one-page-pitch.html https://osahmed.github.io/aimy-pitch-public/ 301
https://aimy-catalogue-internal-617r.vercel.app/* https://osahmed.github.io/aimy-pitch-public/:splat 301
```
- Compatible with Netlify/Vercel
- Catches any edge cases
- Legacy URL support

## 🎯 Why These Redirects?

### Single Source of Truth
The one-page pitch is now maintained in **one place**:
- Primary: `https://osahmed.github.io/aimy-pitch-public/`
- Source: `aimy-pitch-public` repository

### Benefits
✅ **No duplicate content** - Better for SEO  
✅ **Single update point** - Change once, live everywhere  
✅ **Consistent URLs** - Same link works across all deployments  
✅ **Clear separation** - Internal vs. public content  

### Previous Setup (Replaced)
❌ Multiple copies of one-page-pitch.html  
❌ Different URLs for same content  
❌ Manual sync required  
❌ Potential version conflicts  

### Current Setup (Improved)
✅ Single pitch repository  
✅ All paths redirect to it  
✅ Automatic deployments  
✅ Single URL to share  

## 🔍 Testing Redirects

### Test Commands
```bash
# Test redirect from Vercel deployment
curl -I https://aimy-catalogue-internal-617r.vercel.app/one-page-pitch

# Should return:
# HTTP/1.1 301 Moved Permanently
# Location: https://osahmed.github.io/aimy-pitch-public/
```

### Manual Testing
1. Visit: `https://aimy-catalogue-internal-617r.vercel.app/one-page-pitch`
2. Should automatically redirect to: `https://osahmed.github.io/aimy-pitch-public/`
3. Browser address bar will show the new URL

## 📊 Redirect Flow

```
User clicks "One-Page Pitch" in catalogue
           ↓
Internal link: https://osahmed.github.io/aimy-pitch-public/
           ↓
Opens in new tab (target="_blank")
           ↓
User sees pitch page (GitHub Pages)
```

Or via old URLs:
```
User visits old URL: /one-page-pitch
           ↓
Vercel redirect (301)
           ↓
Browser redirects to: https://osahmed.github.io/aimy-pitch-public/
           ↓
User sees pitch page (GitHub Pages)
```

## 🔐 Security Notes

- All redirects use HTTPS
- No sensitive data exposed in redirect URLs
- 301 status prevents caching issues
- External links open in new tabs (security best practice)

## 📝 Maintenance

### When to Update
- If GitHub Pages URL changes
- If deploying to a custom domain
- If creating regional deployments

### How to Update
1. Edit `index.html` - Update the href
2. Edit `vercel.json` - Update destination URLs
3. Edit `public/_redirects` - Update target URLs
4. Commit and push changes
5. Vercel auto-deploys within 10 seconds

---

**Last Updated:** 2026-05-25  
**Status:** Active and deployed
