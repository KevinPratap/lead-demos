"""One-command daily run.

Steps:
  1. Decide if we need a fresh Apify scrape (weekly/daily based on config)
  2. If yes: run scrape, ingest into SQLite
  3. Pick the N new no-website leads
  4. Export to CSV + Markdown
  5. Print a summary
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
import yaml

# Allow running from any working directory
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import apify_client
import lead_cache as lc
import export_local


CFG_PATH = Path(__file__).resolve().parent.parent / "config.yaml"


def load_cfg() -> dict:
    return yaml.safe_load(CFG_PATH.read_text())


def should_rescrape(cfg: dict) -> bool:
    cadence = cfg.get("rescrape_cadence", "weekly")
    if cadence == "manual":
        return False
    # If we have zero leads, always scrape
    s = lc.stats()
    if s["total"] == 0:
        return True
    # Check age of most recent scrape
    import sqlite3
    with sqlite3.connect(lc.DB_PATH) as c:
        row = c.execute("SELECT MAX(scraped_at) FROM leads").fetchone()
    last = row[0] if row else None
    if not last:
        return True
    # crude day-diff
    from datetime import datetime, timezone
    try:
        last_dt = datetime.strptime(last[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    except Exception:
        return True
    age_days = (datetime.now(timezone.utc) - last_dt).days
    if cadence == "daily":
        return age_days >= 1
    if cadence == "weekly":
        return age_days >= 7
    return False


def run():
    cfg = load_cfg()
    n = cfg.get("leads_per_day", 5)
    max_results = cfg.get("apify_max_results", 100)  # renamed: max_results_per_query

    print(f"=== Hermes daily run · {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    print(f"Niche: {cfg['niche']} in {cfg['city']}")
    print(f"Targets/day: {n} | Rescrape cadence: {cfg.get('rescrape_cadence','weekly')}")
    print(f"Provider: Google Maps Places API (New)\n")

    # 1) Scrape if needed
    if should_rescrape(cfg):
        for q in cfg.get("queries", []):
            try:
                items = apify_client.run_scrape(q, max_results=max_results)
                lc.ingest(items)
                print(f"  + {q!r}: {len(items)} results")
            except Exception as e:
                print(f"  ! scrape failed for {q!r}: {e}", file=sys.stderr)
    else:
        print("(skipping scrape — cache is fresh enough)")

    s = lc.stats()
    print(f"Cache: total={s['total']}  no_website={s['no_website']}  pending_to_pitch={s['pending']}\n")

    # 2) Pick N new
    new = lc.pick_new(n)
    if not new:
        print("No new leads to push. Run a manual scrape or change niche.")
        return 0

    print(f"Picked {len(new)} new leads:")
    for r in new:
        print(f"  · {r['name']:45s} | {r['phone'] or '—':15s} | ⭐{r['rating'] or 0:.1f}")

    # 3) Mark pushed + export
    lc.mark_pushed([r["place_id"] for r in new])
    csv_p, md_p = export_local.main()
    print(f"\n✓ Wrote {csv_p}")
    print(f"✓ Wrote {md_p}")
    print(f"\nNext: open the markdown file and pick your top 1 to pitch. Build a demo site via Antigravity.")
    return len(new)


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
