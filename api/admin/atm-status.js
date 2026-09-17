import { adminOk } from '../_auth.js';
import { getConfig } from '../../lib/atm-server.js';
import { supa } from '../../lib/supabase-server.js';
async function countType(type){
  const since=new Date(); since.setHours(0,0,0,0);
  const path=`/rest/v1/events?select=type&type=eq.${encodeURIComponent(type)}&created_at=gte.${encodeURIComponent(since.toISOString())}&limit=1`;
  const { headers }=await supa(path,{headers:{Prefer:'count=exact',Range:'0-0'}});
  const cr=headers.get('content-range')||'';
  const m=cr.match(/\/(\d+|\*)$/);
  return m && m[1] !== '*' ? Number(m[1]) : 0;
}
export default async function handler(req,res){
  if(!adminOk(req)) return res.status(401).json({error:'Token ATM inválido'});
  try{
    const row=await getConfig();
    const [valid,invalid,missing]=await Promise.all([countType('atm_valid'),countType('atm_invalid'),countType('atm_missing')]);
    return res.status(200).json({ok:true,configured:!!row?.current_hash,version:row?.version||0,updatedAt:row?.updated_at||null,previousExpiresAt:row?.previous_expires_at||null,stats:{valid,invalid,missing}});
  }catch(e){console.error(e);return res.status(500).json({error:'ATM ainda não configurado. Confira as variáveis e execute supabase-atm.sql.'});}
}
