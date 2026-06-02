# Hermes Lead-Pipeline

Automated local lead generation + demo website builder.
Stack: Apify (Maps scrape) → SQLite (dedup/cache) → CSV+MD export → Antigravity (build) → GitHub Pages (host).

## ✅ What's working (verified)
- **Apify Maps scrape**: $0 spent, async + polling, 20 results per run
- **SQLite dedup**: 20 leads in cache, 6 no-website, dedup invariant verified
- **Local export**: data/exports/pitch_sheet.md + all_leads.csv
- **Daily run orchestrator**: `python scripts/daily_run.py` — one command, smart about cache freshness
- **Antigravity prompt template**: prompts/antigravity_prompt.md with full pitch script

## ⏳ What's deferred (blocked, not failed)
- **GitHub Pages deployment** — token redaction issue in our environment blocked gh auth. Sites can still be built in Antigravity and viewed locally.
- **Google Sheets sync** — chose CSV/MD export instead (works fine, just less live).
- **Cron job for daily 8am** — easy to add via Hermes cronjob tool once GitHub auth is sorted.

## Run it
```bash
cd ~/leads
source .venv/bin/activate
python scripts/daily_run.py
# → updates pitch_sheet.md with the next batch of new leads
```

## Currently in your pitch sheet (6 ready-to-call leads)
1. Saifee Dental Clinic · +91 98701 32176 · 4.9⭐
2. Dr Abbas Unwala's Saifee Smiles Multispeciality · +91 98208 54665 · 4.9⭐
3. Specialist Dental Centre (SINCE 1983) · +91 99204 07651 · 5.0⭐
4. Dr Merchant's Dental Clinic · +91 90812 32785 · 5.0⭐
5. CARE DENTAL CLINIC · +91 91676 66796 · 5.0⭐
6. Dr.Bera's dental clinic Mumbai Dentist · +91 97025 82286 · 5.0⭐

## Next step
1. Open `data/exports/pitch_sheet.md`
2. Pick #6 (highest rating, 5.0⭐)
3. Open `prompts/antigravity_prompt.md`, copy the prompt, fill in {NAME} and {MAPS_URL}
4. Run in Google Antigravity
5. Use the pitch script in the same file to call the clinic

## Cost model
- Apify free tier = $5/month credit
- One scrape of 100 results ≈ $0.10
- Default cadence is weekly. Change `rescrape_cadence` in `config.yaml` to `daily` if you want fresh leads every day (~$0.40/month).

## File tree
```
~/leads/
├── README.md
├── config.yaml                  ← niche, city, cadence, leads_per_day
├── data/
│   ├── leads.db                 ← SQLite cache (gitignored)
│   └── exports/
│       ├── pitch_sheet.md       ← ← READ THIS, this is your lead list
│       └── all_leads.csv        ← raw data, for spreadsheets
├── prompts/
│   └── antigravity_prompt.md    ← copy-paste prompt for Antigravity + pitch script
└── scripts/
    ├── apify_client.py          ← Apify Maps Scraper client
    ├── lead_cache.py            ← SQLite dedup + filter
    ├── export_local.py          ← CSV + Markdown export
    ├── daily_run.py             ← orchestrator: scrape → dedup → export
    ├── check_token.py           ← verify Apify auth
    └── sheets_sync.py           ← stub, deferred
```

## When you want GitHub Pages
1. Open a WSL terminal directly (not Windows PowerShell) and run:
   ```bash
   cat > ~/.gh_pat << 'EOF'
   <paste your github_pat_... token here>
   EOF
   chmod 600 ~/.gh_pat
   ```
2. Tell Hermes "auth gh with ~/.gh_pat" and we'll create KevinPratap/lead-demos, enable Pages, and finish cron setup.
