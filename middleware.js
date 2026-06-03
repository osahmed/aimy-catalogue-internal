// Edge middleware — the PRIMARY authentication gate.
//
// Runs before the cache on every matched request. If there is no valid signed
// session cookie, the request is redirected to the Cognito login flow. This is
// what makes auth a backend guarantee: a logged-out client never receives the
// HTML, the logos, or catalogue-public.json — only a 302 to /api/auth/login.
import { parseCookies, verifySession, COOKIE_NAMES } from './lib/auth.js';

export const config = {
  // Gate everything EXCEPT the auth endpoints themselves and favicon.
  // (Static assets under the catalogue are intentionally gated too.)
  matcher: ['/((?!api/auth/|favicon\\.ico|favicon).*)'],
};

export default async function middleware(request) {
  const url = new URL(request.url);
  const cookies = parseCookies(request.headers.get('cookie'));
  const session = await verifySession(cookies[COOKIE_NAMES.SESSION]);

  if (session) {
    return; // authenticated → continue to the requested resource
  }

  const returnTo = url.pathname + url.search;
  const loginUrl = new URL('/api/auth/login', url.origin);
  loginUrl.searchParams.set('returnTo', returnTo);
  return Response.redirect(loginUrl.toString(), 302);
}
