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
import pitch_messages

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
        "---",
        "",
        "## 📋 Quick Overview",
        "",
        "| # | Business | Phone | Rating | Area | AG Folder |",
        "|---|----------|-------|--------|------|-----------|",
    ]
    for i, r in enumerate(rows, 1):
        rating = f"{r['rating']:.1f}⭐" if r.get("rating") else "—"
        area = (r.get("address") or "").split(",")[0].strip() if r.get("address") else "—"
        slug = pitch_messages._slug(r)
        lines.append(
            f"| {i} | {r['name']} | {r['phone'] or '—'} | {rating} | {area} | `leads/{slug}` |"
        )

    lines += [
        "",
        "---",
        "",
        "## 📞 Full Pitch Scripts",
        "",
    ]

    for i, r in enumerate(rows, 1):
        rating = f"{r['rating']:.1f}⭐" if r.get("rating") else "—"
        reviews = f"{r.get('reviews', 0) or 0} reviews"
        address = r.get("address") or "—"
        maps = r.get("google_url") or ""

        lines += [
            f"### {i}. {r['name']}",
            "",
            f"**Phone:** {r['phone'] or '—'} | **Rating:** {rating} ({reviews})",
            f"**Address:** {address}",
            f"**Maps:** {maps}",
            "",
            "#### 💬 WhatsApp (copy-paste)",
            "",
            pitch_messages.whatsapp(r),
            "",
            "#### 📞 Call Script",
            "",
            pitch_messages.call_script(r),
            "",
            "#### 🤖 Antigravity Prompt (copy-paste into AG IDE)",
            "",
            "```",
            pitch_messages.antigravity(r),
            "```",
            "",
            "#### 📤 Auto-Send WhatsApp (terminal)",
            "",
            "```bash",
            f"node scripts/send_whatsapp.js --lead \"{r['name']}\" --url <DEMO_URL>",
            "```",
            "",
        ]
        if i < len(rows):
            lines.append("---")
            lines.append("")

    lines += [
        "",
        "## How to use",
        "1. Pick a lead from the overview table above",
        "2. Copy the 🤖 Antigravity Prompt → paste into Antigravity IDE → site built",
        "3. Deploy to GitHub Pages. Copy the live URL.",
        "4. Run the 📤 send command below the lead (replace <DEMO_URL> with the live URL)",
        "5. First run: scan QR code with WhatsApp. After that: fully automatic.",
        "",
        "### 💡 Pro tip: bulk send all demos",
        "```bash",
        "# After all demo sites are deployed, send them all:",
        "for lead in leads/dr-merchants-dental-clinic leads/care-dental-clinic; do",
        "  node scripts/send_whatsapp.js --lead \"$lead\" --url \"https://kevin.github.io/lead-demos/$lead/\"",
        "  sleep 30  # human-like delay",
        "done",
        "```",
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

    # Auto-copy to Windows Downloads for easy access
    downloads = Path("/mnt/c/Users/prata/Downloads/pitch_sheet.md")
    try:
        downloads.write_bytes(md_p.read_bytes())
        print(f"CP:   {downloads}")
    except Exception as e:
        print(f"CP:   skipped ({e})")

    return csv_p, md_p


if __name__ == "__main__":
    main()
