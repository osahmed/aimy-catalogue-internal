// Shared authentication helpers for the AiMY Cognito SSO flow.
//
// Runs in both the Edge runtime (middleware.js) and the Node runtime
// (api/auth/*). Everything here uses Web Crypto + jose, which are available
// in both, so there is one implementation to maintain.
import { SignJWT, jwtVerify, createRemoteJWKSet } from 'jose';

const SESSION_COOKIE = 'aimy_session';
const TX_COOKIE = 'aimy_auth_tx'; // short-lived: holds state/nonce/pkce/returnTo
const SESSION_TTL_SECONDS = 8 * 60 * 60; // 8 hours
const TX_TTL_SECONDS = 10 * 60; // 10 minutes

export const COOKIE_NAMES = { SESSION: SESSION_COOKIE, TX: TX_COOKIE };

// ---------------------------------------------------------------- config
export function getConfig() {
  const required = [
    'COGNITO_DOMAIN',
    'COGNITO_ISSUER',
    'COGNITO_CLIENT_ID',
    'COGNITO_CLIENT_SECRET',
    'APP_BASE_URL',
    'SESSION_SECRET',
  ];
  const cfg = {};
  for (const key of required) {
    const val = process.env[key];
    if (!val) throw new Error(`Missing required env var: ${key}`);
    cfg[key] = val.trim().replace(/\/+$/, ''); // strip trailing slashes (URLs)
  }
  // SESSION_SECRET must not be slash-trimmed in a way that changes it; re-read raw.
  cfg.SESSION_SECRET = process.env.SESSION_SECRET;
  cfg.COGNITO_IDP_NAME = (process.env.COGNITO_IDP_NAME || '').trim();
  cfg.REDIRECT_URI = `${cfg.APP_BASE_URL}/api/auth/callback`;
  cfg.LOGOUT_REDIRECT = `${cfg.APP_BASE_URL}/`;
  cfg.JWKS_URI = `${cfg.COGNITO_ISSUER}/.well-known/jwks.json`;
  return cfg;
}

function secretKey() {
  return new TextEncoder().encode(process.env.SESSION_SECRET);
}

// ------------------------------------------------------------ session JWT
export async function signSession(claims) {
  return new SignJWT(claims)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime(`${SESSION_TTL_SECONDS}s`)
    .sign(secretKey());
}

export async function verifySession(token) {
  if (!token) return null;
  try {
    const { payload } = await jwtVerify(token, secretKey());
    return payload;
  } catch {
    return null;
  }
}

// Short-lived signed cookie carrying the in-flight OAuth transaction.
export async function signTx(data) {
  return new SignJWT(data)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime(`${TX_TTL_SECONDS}s`)
    .sign(secretKey());
}

export async function verifyTx(token) {
  if (!token) return null;
  try {
    const { payload } = await jwtVerify(token, secretKey());
    return payload;
  } catch {
    return null;
  }
}

// --------------------------------------------------------- id_token verify
let _jwks;
export async function verifyIdToken(idToken, cfg) {
  if (!_jwks) _jwks = createRemoteJWKSet(new URL(cfg.JWKS_URI));
  const { payload } = await jwtVerify(idToken, _jwks, {
    issuer: cfg.COGNITO_ISSUER,
    audience: cfg.COGNITO_CLIENT_ID,
  });
  return payload;
}

// -------------------------------------------------------------- PKCE/state
function b64url(bytes) {
  let str = '';
  const arr = new Uint8Array(bytes);
  for (let i = 0; i < arr.length; i++) str += String.fromCharCode(arr[i]);
  return btoa(str).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export function randomToken(byteLen = 32) {
  return b64url(crypto.getRandomValues(new Uint8Array(byteLen)));
}

export async function pkceChallenge() {
  const verifier = randomToken(48);
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier));
  return { verifier, challenge: b64url(digest) };
}

// ----------------------------------------------------------------- cookies
export function parseCookies(header) {
  const out = {};
  if (!header) return out;
  for (const part of header.split(';')) {
    const idx = part.indexOf('=');
    if (idx === -1) continue;
    const k = part.slice(0, idx).trim();
    const v = part.slice(idx + 1).trim();
    if (k) out[k] = decodeURIComponent(v);
  }
  return out;
}

export function buildCookie(name, value, { maxAge, expires } = {}) {
  const parts = [
    `${name}=${encodeURIComponent(value)}`,
    'Path=/',
    'HttpOnly',
    'Secure',
    'SameSite=Lax',
  ];
  if (typeof maxAge === 'number') parts.push(`Max-Age=${maxAge}`);
  if (expires) parts.push(`Expires=${expires}`);
  return parts.join('; ');
}

export function sessionCookie(token) {
  return buildCookie(SESSION_COOKIE, token, { maxAge: SESSION_TTL_SECONDS });
}
export function txCookie(token) {
  return buildCookie(TX_COOKIE, token, { maxAge: TX_TTL_SECONDS });
}
export function clearCookie(name) {
  return buildCookie(name, '', { maxAge: 0, expires: 'Thu, 01 Jan 1970 00:00:00 GMT' });
}
