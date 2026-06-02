demandimport

# Lead Pipeline — local lead-gen engine

- Apify Maps scrape → SQLite dedup/cache → CSV+MD export
- See `prompts/antigravity_prompt.md` for the demo-site build workflow
- See `config.yaml` for niche / city / cadence

## Daily run
```
source .venv/bin/activate
python scripts/daily_run.py
```

## Cost model
Apify free tier = $5 monthly credit. One scrape of 100 results ≈ $0.10.
Default cadence is weekly. We default to 100 results / scrape.

## Adding a new niche
Edit `config.yaml` `niche`, `city`, and `queries`. Done.

## Demo site workflow
1. Read `data/exports/pitch_sheet.md` — pick a lead
2. Use `prompts/antigravity_prompt.md` in Google Antigravity to build
3. Push to your `lead-demos` GitHub Pages repo
4. Pitch via the included phone script
