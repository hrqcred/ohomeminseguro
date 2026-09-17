const DEFAULT_URL = 'https://zfljisjwrnkhfsmwdace.supabase.co';

export function supaConfig() {
  const url = (process.env.SUPABASE_URL || DEFAULT_URL).replace(/\/+$/, '');
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!key) throw new Error('SUPABASE_SERVICE_ROLE_KEY ausente');
  return { url, key };
}

export async function supa(path, options = {}) {
  const { url, key } = supaConfig();
  const headers = {
    apikey: key,
    Authorization: `Bearer ${key}`,
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };
  const res = await fetch(url + path, { ...options, headers });
  const text = await res.text();
  if (!res.ok) throw new Error(`Supabase ${res.status}: ${text}`);
  if (!text) return { data: null, headers: res.headers };
  try { return { data: JSON.parse(text), headers: res.headers }; }
  catch { return { data: text, headers: res.headers }; }
}
