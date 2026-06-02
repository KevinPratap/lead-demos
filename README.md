# Hermes Lead-Pipeline

Automated local lead generation + demo website builder.
Stack: Apify (Maps scrape) → SQLite (dedup/cache) → Google Sheets (pitch sheet) → Antigravity + GitHub Pages (demo sites).

## Setup
1. `source .venv/bin/activate`
2. Make sure `~/.config/hermes/leads/.env` has your `APIFY_TOKEN` (already done).
3. First run: `python scripts/daily_run.py` — this will:
   - Hit Apify Google Maps Scraper (~$0.10 of free credit)
   - Filter to businesses with no website
   - Dedup against `data/leads.db`
   - Push the 5 newest to a Google Sheet
4. (One-time) Authenticate Google: `python scripts/sheets_auth.py`

## Files
- `config.yaml` — niche, city, lead count, scrape cadence
- `scripts/apify_client.py` — wrapper around Apify REST API
- `scripts/filter_dedup.py` — SQLite-backed no-website filter + dedup
- `scripts/sheets_sync.py` — pushes leads to Google Sheet
- `scripts/sheets_auth.py` — one-time OAuth setup
- `scripts/daily_run.py` — orchestrator (this is what the cron job calls)
- `prompts/antigravity_prompt.md` — copy-paste prompt for Antigravity
- `data/leads.db` — local cache (gitignored)

## Cost model
- Apify free tier = $5 credit
- One scrape of 100 results ≈ $0.10
- Weekly cadence ≈ $0.40/month → $5 lasts ~12 months
- If we go daily: $0.70/week → $5 lasts ~7 weeks
- We default to weekly. Change `rescrape_cadence` in config.yaml.

## Demo sites
Built freestyle with Google Antigravity, hosted on GitHub Pages (one repo, subfolders per lead).
See `prompts/antigravity_prompt.md` for the exact prompt to use.
