// Completes the OIDC flow: validates state, exchanges the code for tokens,
// verifies the id_token (signature + iss + aud + nonce), then issues a signed
// session cookie and returns the user to where they started.
import {
  getConfig,
  verifyTx,
  verifyIdToken,
  signSession,
  sessionCookie,
  clearCookie,
  parseCookies,
  COOKIE_NAMES,
} from '../../lib/auth.js';

function bounceToLogin(res) {
  res.setHeader('Set-Cookie', clearCookie(COOKIE_NAMES.TX));
  res.writeHead(302, { Location: '/api/auth/login' });
  res.end();
}

export default async function handler(req, res) {
  let cfg;
  try {
    cfg = getConfig();
  } catch {
    res.status(500).send('Auth not configured');
    return;
  }

  const { code, state, error } = req.query;
  if (error || !code || !state) return bounceToLogin(res);

  const cookies = parseCookies(req.headers.get ? req.headers.get('cookie') : req.headers.cookie);
  const tx = await verifyTx(cookies[COOKIE_NAMES.TX]);
  if (!tx || tx.state !== state) return bounceToLogin(res);

  // Exchange authorization code for tokens (confidential client → Basic auth).
  const basic = Buffer.from(`${cfg.COGNITO_CLIENT_ID}:${cfg.COGNITO_CLIENT_SECRET}`).toString('base64');
  const body = new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: cfg.COGNITO_CLIENT_ID,
    code: String(code),
    redirect_uri: cfg.REDIRECT_URI,
    code_verifier: tx.verifier,
  });

  let tokens;
  try {
    const tokenRes = await fetch(`${cfg.COGNITO_DOMAIN}/oauth2/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        Authorization: `Basic ${basic}`,
      },
      body,
    });
    if (!tokenRes.ok) return bounceToLogin(res);
    tokens = await tokenRes.json();
  } catch {
    return bounceToLogin(res);
  }

  if (!tokens.id_token) return bounceToLogin(res);

  let claims;
  try {
    claims = await verifyIdToken(tokens.id_token, cfg);
    if (claims.nonce !== tx.nonce) return bounceToLogin(res);
  } catch {
    return bounceToLogin(res);
  }

  const session = await signSession({
    sub: claims.sub,
    email: claims.email || claims['cognito:username'] || '',
  });

  let returnTo = typeof tx.returnTo === 'string' && tx.returnTo.startsWith('/') && !tx.returnTo.startsWith('//')
    ? tx.returnTo
    : '/';

  res.setHeader('Set-Cookie', [sessionCookie(session), clearCookie(COOKIE_NAMES.TX)]);
  res.writeHead(302, { Location: returnTo });
  res.end();
}
