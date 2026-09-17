import crypto from 'node:crypto';
import { supa } from './supabase-server.js';

const ROW_ID = 'atm_gate';
function secret() {
  const v = process.env.ATM_HASH_SECRET || process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!v) throw new Error('ATM hash secret ausente');
  return v;
}
export function newAtm() { return 'ohmi_' + crypto.randomBytes(24).toString('base64url'); }
export function hashAtm(value) { return crypto.createHmac('sha256', secret()).update(String(value)).digest('hex'); }
function safeEq(a,b) {
  if (!a || !b) return false;
  try { const aa=Buffer.from(a,'hex'), bb=Buffer.from(b,'hex'); return aa.length===bb.length && crypto.timingSafeEqual(aa,bb); } catch { return false; }
}
export async function getConfig() {
  const { data } = await supa(`/rest/v1/site_config?id=eq.${ROW_ID}&select=*`);
  return Array.isArray(data) && data[0] ? data[0] : null;
}
export async function validateAtm(atm) {
  if (!atm || typeof atm !== 'string' || atm.length > 180) return { valid:false, source:null };
  const row = await getConfig();
  if (!row) return { valid:false, source:null };
  const h = hashAtm(atm);
  if (safeEq(h,row.current_hash)) return { valid:true, source:'current' };
  if (row.previous_hash && row.previous_expires_at && new Date(row.previous_expires_at).getTime() > Date.now() && safeEq(h,row.previous_hash)) return { valid:true, source:'previous' };
  return { valid:false, source:null };
}
export async function rotateAtm(graceHours=24) {
  const old = await getConfig();
  const hours = Math.max(0,Math.min(168,Number(graceHours)||0));
  const plain = newAtm();
  const now = new Date();
  const previousHash = old?.current_hash && hours > 0 ? old.current_hash : null;
  const previousExpires = previousHash ? new Date(now.getTime()+hours*3600000).toISOString() : null;
  const payload = {
    id: ROW_ID,
    current_hash: hashAtm(plain),
    previous_hash: previousHash,
    previous_expires_at: previousExpires,
    version: Number(old?.version||0)+1,
    updated_at: now.toISOString()
  };
  await supa('/rest/v1/site_config?on_conflict=id', {
    method:'POST', headers:{Prefer:'resolution=merge-duplicates,return=minimal'}, body:JSON.stringify(payload)
  });
  return { atm:plain, version:payload.version, previousExpiresAt:previousExpires, updatedAt:payload.updated_at };
}
export async function revokePrevious() {
  await supa(`/rest/v1/site_config?id=eq.${ROW_ID}`, {method:'PATCH', headers:{Prefer:'return=minimal'}, body:JSON.stringify({previous_hash:null,previous_expires_at:null,updated_at:new Date().toISOString()})});
}
