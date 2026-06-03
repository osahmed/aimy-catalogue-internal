// Returns the current signed-in user (for the header UI). The edge middleware
// already guarantees a valid session for page loads; this endpoint is excluded
// from the gate so the page can read who is logged in.
import { verifySession, parseCookies, COOKIE_NAMES } from '../../lib/auth.js';

export default async function handler(req, res) {
  const cookieHeader = req.headers.get ? req.headers.get('cookie') : req.headers.cookie;
  const cookies = parseCookies(cookieHeader);
  const session = await verifySession(cookies[COOKIE_NAMES.SESSION]);

  res.setHeader('Cache-Control', 'no-store');
  if (!session) {
    res.status(401).json({ authenticated: false });
    return;
  }
  res.status(200).json({ authenticated: true, email: session.email || '' });
}
