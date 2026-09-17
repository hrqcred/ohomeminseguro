import { adminOk } from '../_auth.js';
import { rotateAtm } from '../../lib/atm-server.js';
export default async function handler(req,res){
  if(req.method!=='POST') return res.status(405).json({error:'Method not allowed'});
  if(!adminOk(req)) return res.status(401).json({error:'Token ATM inválido'});
  try{
    const result=await rotateAtm(req.body?.graceHours??24);
    const base='https://www.ohomeminseguro.store/';
    const params=new URLSearchParams();
    params.set('atm',result.atm);
    params.set('utm_source','{{site_source_name}}');
    params.set('utm_medium','paid_social');
    params.set('utm_campaign','{{campaign.name}}');
    params.set('utm_content','{{ad.name}}');
    params.set('utm_term','{{adset.name}}');
    params.set('utm_id','{{campaign.id}}');
    params.set('campaign_id','{{campaign.id}}');
    params.set('adset_id','{{adset.id}}');
    params.set('ad_id','{{ad.id}}');
    params.set('creative_id','{{ad.id}}');
    params.set('placement','{{placement}}');
    params.set('site_source_name','{{site_source_name}}');
    return res.status(200).json({ok:true,...result,campaignUrl:base+'?'+params.toString()});
  }catch(e){console.error(e);return res.status(500).json({error:'Não foi possível gerar a nova chave ATM.'});}
}
