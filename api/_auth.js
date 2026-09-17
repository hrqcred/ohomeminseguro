export function adminOk(req) {
  const expected = process.env.ATM_ADMIN_TOKEN || '';
  const got = String(req.headers['x-atm-admin-token'] || '');
  if (!expected || !got) return false;
  let diff = expected.length ^ got.length;
  const n = Math.max(expected.length, got.length);
  for (let i=0;i<n;i++) diff |= (expected.charCodeAt(i%expected.length)||0) ^ (got.charCodeAt(i%got.length)||0);
  return diff === 0;
}
