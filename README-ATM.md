# Alterações ATM + Blog

## O que já foi alterado

- `/` agora passa por `api/gate.js`.
- Sem `atm`, com `atm` inválido ou expirado: o usuário recebe o blog.
- Com `atm` válido: recebe o funil original, na mesma URL raiz.
- Não existe `funil.html` público. O funil original está empacotado em `lib/funnel-content.js`.
- O painel `admin.html` ganhou a aba **ATM**.
- A nova URL de campanha inclui UTMs e IDs dinâmicos.
- O funil preserva mais parâmetros no checkout.
- Tracking ganhou `utm_term`, `campaign_id`, `adset_id`, `ad_id` e `placement`.

## 2 passos antes do deploy

### 1. Supabase
Abra o SQL Editor do projeto Supabase já usado pelo site e execute todo o arquivo:

`supabase-atm.sql`

### 2. Vercel
Em **Settings > Environment Variables**, adicione:

- `SUPABASE_URL` = `https://zfljisjwrnkhfsmwdace.supabase.co`
- `SUPABASE_SERVICE_ROLE_KEY` = chave **service_role** do mesmo projeto Supabase
- `ATM_ADMIN_TOKEN` = um token administrativo longo

Um token aleatório já foi gerado em `.env.example`. Você pode usar aquele valor ou criar outro.

Depois faça um novo deploy.

## Uso

1. Abra `https://www.ohomeminseguro.store/admin.html`.
2. Entre com o PIN atual.
3. Abra a aba **ATM**.
4. Cole o mesmo `ATM_ADMIN_TOKEN` configurado na Vercel.
5. Clique **Verificar conexão**.
6. Clique **Gerar nova ATM**.
7. Copie a URL pronta para a campanha.

Exemplo de formato:

`https://www.ohomeminseguro.store/?atm=ohmi_...&utm_source={site_source_name}&utm_medium=paid_social&utm_campaign={campaign.name}&utm_content={ad.name}&utm_term={adset.name}&utm_id={campaign.id}&campaign_id={campaign.id}&adset_id={adset.id}&ad_id={ad.id}&creative_id={ad.id}&placement={placement}&site_source_name={site_source_name}`

## Regra final

- domínio puro -> blog
- URL com ATM válida -> funil original
- ATM inválida -> blog
- ATM antiga dentro da tolerância -> funil
- ATM antiga expirada/revogada -> blog

## Observação

A Service Role fica somente no backend/Vercel e nunca é colocada no HTML público. Não comite uma `.env` real com segredos.
