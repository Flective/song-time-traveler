# Supabase Setup — Fiat Musica feedback + future play counts

**Goal:** one free database to store listener feedback now, and play counts / favoriting later.
**Cost:** $0 (free tier). No monthly bill for this usage.
**Your time:** ~10 minutes, all in the browser.

---

## STEP 1 — Create the project
1. Go to **supabase.com** → Sign up (GitHub or email).
2. Click **New project**.
3. Name it anything (e.g. `fiatmusica`). Choose a region near you (US East is fine).
4. It asks for a **database password** — make one up, save it somewhere (you won't need it for the website, but keep it).
5. Click **Create**. Wait ~2 minutes while it provisions.

---

## STEP 2 — Create the tables
1. In the left sidebar, click **SQL Editor**.
2. Click **+ New query**, paste ALL of the SQL below, click **Run**.

```sql
-- Feedback from the listen-page questionnaire
create table feedback (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  song_id text,
  first_impression text,
  hook_rating int,
  sounds_like text,
  lyrics text,
  would_listen_full text,
  comment text
);
alter table feedback enable row level security;
create policy "anyone can submit feedback"
  on feedback for insert to anon with check (true);

-- Play counts (one row per song, incremented as people play)
create table plays (
  song_id text primary key,
  count int default 0
);
alter table plays enable row level security;
create policy "anyone can read plays"
  on plays for select to anon using (true);
-- increment function (safe, atomic)
create or replace function increment_play(p_song_id text)
returns void language plpgsql security definer as $$
begin
  insert into plays (song_id, count) values (p_song_id, 1)
  on conflict (song_id) do update set count = plays.count + 1;
end; $$;
grant execute on function increment_play(text) to anon;
```

3. You should see "Success. No rows returned." That's correct.

---

## STEP 3 — Get the two values for the website
1. Left sidebar → **Project Settings** (gear icon) → **API**.
2. Copy these two, paste them back to me (or into the file as marked):
   - **Project URL** — looks like `https://abcdefgh.supabase.co`
   - **anon / public key** — a long string starting with `eyJ...`
   (The anon key is SAFE to put in a public website. It's designed for that. Do NOT share the `service_role` key — that one's secret. We don't use it.)

---

## STEP 4 — Hand off
Give me the Project URL + anon key. I paste them into:
- `feedback.html` (listen page) — already wired, just needs the two values.
Then feedback saves to your `feedback` table. View responses anytime in Supabase → **Table Editor → feedback**, or export to CSV.

---

## Notes
- **Free-tier sleep:** if a full week passes with zero activity, the project pauses (data kept). Tap **Resume** in the dashboard to wake it. Any traffic keeps it awake.
- **No auto-backups on free tier** — fine for feedback; export occasionally if you want a copy.
- **Play counts / favoriting** use the same project — tables already created above, wired when we build that feature.
