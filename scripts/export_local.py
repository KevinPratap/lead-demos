"""Export the leads in our SQLite cache to a local CSV and a pretty Markdown file.

We do this instead of pushing to Google Sheets for v1 — same data, just a file on disk
that you can copy-paste into a Sheet, or use as-is for daily review.
"""
from __future__ import annotations
import csv
import sqlite3
from contextlib import closing
from pathlib import Path
import yaml

import lead_cache as lc

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "exports"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _all_leads() -> list[dict]:
    with closing(lc.connect()) as c:
        rows = c.execute(
            """
            SELECT place_id, name, phone, address, google_url, rating, reviews,
                   category, website, first_seen_at, pushed_to_sheet
            FROM leads
            ORDER BY first_seen_at DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


def _new_leads() -> list[dict]:
    with closing(lc.connect()) as c:
        rows = c.execute(
            """
            SELECT place_id, name, phone, address, google_url, rating, reviews,
                   category, website, first_seen_at
            FROM leads
            WHERE (website IS NULL OR website = '')
              AND pushed_to_sheet = 1
            ORDER BY first_seen_at DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]


def export_csv() -> Path:
    rows = _all_leads()
    p = OUT_DIR / "all_leads.csv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [
            "place_id", "name", "phone", "address", "google_url", "rating",
            "reviews", "category", "website", "first_seen_at", "pushed_to_sheet"
        ])
        w.writeheader()
        w.writerows(rows)
    return p


def export_markdown() -> Path:
    rows = _new_leads()
    p = OUT_DIR / "pitch_sheet.md"
    cfg = yaml.safe_load((Path(__file__).resolve().parent.parent / "config.yaml").read_text())
    lines = [
        f"# {cfg['niche'].title()} in {cfg['city']} — Daily Pitch Sheet",
        "",
        f"_Generated from local Apify cache. {len(rows)} leads ready to pitch._",
        "",
        "| # | Business | Phone | Address | Rating | Google Maps |",
        "|---|----------|-------|---------|--------|-------------|",
    ]
    for i, r in enumerate(rows, 1):
        rating = f"{r['rating']:.1f}⭐" if r.get("rating") else "—"
        lines.append(
            f"| {i} | {r['name']} | {r['phone'] or '—'} | {r['address'] or '—'} | {rating} | [Maps]({r['google_url']}) |"
        )
    lines += [
        "",
        "## How to use",
        "1. Pick the highest-rating / most-reviewed clinic from this list",
        "2. Build a demo site for them (Antigravity prompt → GitHub Pages)",
        "3. Call them, open the demo, pitch website services",
        "",
        f"_Database: data/leads.db · Total in cache: {len(_all_leads())}_",
    ]
    p.write_text("\n".join(lines), encoding="utf-8")
    return p


def main():
    csv_p = export_csv()
    md_p = export_markdown()
    print(f"CSV:  {csv_p} ({csv_p.stat().st_size} bytes)")
    print(f"MD:   {md_p} ({md_p.stat().st_size} bytes)")
    return csv_p, md_p


if __name__ == "__main__":
    main()
