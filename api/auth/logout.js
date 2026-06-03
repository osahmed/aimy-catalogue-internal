// Clears the local session and ends the Cognito session via its logout endpoint.
import { getConfig, clearCookie, COOKIE_NAMES } from '../../lib/auth.js';

export default async function handler(req, res) {
  let cfg;
  try {
    cfg = getConfig();
  } catch {
    res.status(500).send('Auth not configured');
    return;
  }

  const logoutUrl = new URL(`${cfg.COGNITO_DOMAIN}/logout`);
  logoutUrl.searchParams.set('client_id', cfg.COGNITO_CLIENT_ID);
  logoutUrl.searchParams.set('logout_uri', cfg.LOGOUT_REDIRECT);

  res.setHeader('Set-Cookie', [
    clearCookie(COOKIE_NAMES.SESSION),
    clearCookie(COOKIE_NAMES.TX),
  ]);
  res.writeHead(302, { Location: logoutUrl.toString() });
  res.end();
}
