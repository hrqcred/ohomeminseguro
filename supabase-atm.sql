-- Execute UMA VEZ no SQL Editor do mesmo projeto Supabase já usado pelo site.

create table if not exists public.site_config (
  id text primary key,
  current_hash text,
  previous_hash text,
  previous_expires_at timestamptz,
  version integer not null default 0,
  updated_at timestamptz not null default now()
);

-- O gate usa Service Role no servidor. Nenhuma policy pública é necessária.
alter table public.site_config enable row level security;

-- Amplia o tracking existente sem remover nenhuma coluna atual.
alter table public.events add column if not exists utm_term text default '';
alter table public.events add column if not exists campaign_id text default '';
alter table public.events add column if not exists adset_id text default '';
alter table public.events add column if not exists ad_id text default '';
alter table public.events add column if not exists placement text default '';

create index if not exists events_type_created_idx on public.events(type, created_at desc);
