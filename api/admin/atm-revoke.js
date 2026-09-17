import { adminOk } from '../_auth.js';
import { revokePrevious } from '../../lib/atm-server.js';
export default async function handler(req,res){
  if(req.method!=='POST') return res.status(405).json({error:'Method not allowed'});
  if(!adminOk(req)) return res.status(401).json({error:'Token ATM inválido'});
  try{await revokePrevious();return res.status(200).json({ok:true});}catch(e){console.error(e);return res.status(500).json({error:'Não foi possível revogar a chave anterior.'});}
}
