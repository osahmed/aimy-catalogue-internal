// Begins the OIDC Authorization Code + PKCE flow.
// Stashes state/nonce/verifier/returnTo in a short-lived signed cookie, then
// redirects the browser to the Cognito Hosted UI (which federates to the
// corporate IdP).
import { getConfig, signTx, txCookie, randomToken, pkceChallenge } from '../../lib/auth.js';

export default async function handler(req, res) {
  let cfg;
  try {
    cfg = getConfig();
  } catch (err) {
    res.status(500).send('Auth not configured');
    return;
  }

  const state = randomToken(32);
  const nonce = randomToken(32);
  const { verifier, challenge } = await pkceChallenge();

  let returnTo = req.query.returnTo || '/';
  // Only allow same-site relative paths as returnTo (open-redirect guard).
  if (typeof returnTo !== 'string' || !returnTo.startsWith('/') || returnTo.startsWith('//')) {
    returnTo = '/';
  }

  const tx = await signTx({ state, nonce, verifier, returnTo });

  const authUrl = new URL(`${cfg.COGNITO_DOMAIN}/oauth2/authorize`);
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('client_id', cfg.COGNITO_CLIENT_ID);
  authUrl.searchParams.set('redirect_uri', cfg.REDIRECT_URI);
  authUrl.searchParams.set('scope', 'openid email phone');
  authUrl.searchParams.set('state', state);
  authUrl.searchParams.set('nonce', nonce);
  authUrl.searchParams.set('code_challenge', challenge);
  authUrl.searchParams.set('code_challenge_method', 'S256');
  if (cfg.COGNITO_IDP_NAME) {
    authUrl.searchParams.set('identity_provider', cfg.COGNITO_IDP_NAME);
  }

  res.setHeader('Set-Cookie', txCookie(tx));
  res.writeHead(302, { Location: authUrl.toString() });
  res.end();
}
