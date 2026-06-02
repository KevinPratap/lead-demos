"""SQLite-backed lead cache.

Schema:
    leads(place_id PRIMARY KEY, name, phone, address, website, google_url,
          rating, reviews, category, scraped_at, first_seen_at, pushed_to_sheet)

Workflow:
    ingest()  — insert/update a batch of Apify results (no dedup, just upsert)
    pick_new() — return the N oldest unseen, no-website leads that haven't been
                 pushed to the sheet yet
    mark_pushed() — mark a batch as pushed
"""
from __future__ import annotations
import os, sqlite3, time
from contextlib import closing
from pathlib import Path

DB_PATH = Path(os.environ.get("LEADS_DB", str(Path.home() / "leads" / "data" / "leads.db")))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    place_id       TEXT PRIMARY KEY,
    name           TEXT,
    phone          TEXT,
    address        TEXT,
    website        TEXT,
    google_url     TEXT,
    rating         REAL,
    reviews        INTEGER,
    category       TEXT,
    image_url      TEXT,
    image_urls     TEXT,           -- JSON list
    scraped_at     TEXT,
    first_seen_at  TEXT NOT NULL,
    pushed_to_sheet INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_leads_no_web_unpushed
    ON leads(website, pushed_to_sheet, first_seen_at)
    WHERE website IS NULL OR website = '';
"""


def connect() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    return c


def ingest(items: list[dict]) -> tuple[int, int]:
    """Upsert a batch. Returns (inserted_or_updated, skipped)."""
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    n = 0
    with closing(connect()) as c:
        for it in items:
            pid = it.get("placeId")
            if not pid:
                continue
            c.execute(
                """
                INSERT INTO leads
                    (place_id, name, phone, address, website, google_url,
                     rating, reviews, category, image_url, image_urls,
                     scraped_at, first_seen_at, pushed_to_sheet)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,0)
                ON CONFLICT(place_id) DO UPDATE SET
                    name=excluded.name,
                    phone=excluded.phone,
                    address=excluded.address,
                    website=excluded.website,
                    google_url=excluded.google_url,
                    rating=excluded.rating,
                    reviews=excluded.reviews,
                    category=excluded.category,
                    image_url=excluded.image_url,
                    image_urls=excluded.image_urls,
                    scraped_at=excluded.scraped_at
                """,
                (
                    pid,
                    it.get("title"),
                    it.get("phone") or it.get("phoneUnformatted"),
                    it.get("address"),
                    (it.get("website") or None) or None,  # normalize '' to NULL
                    it.get("url"),
                    it.get("totalScore"),
                    it.get("reviewsCount"),
                    it.get("categoryName"),
                    it.get("imageUrl"),
                    ",".join(it.get("imageUrls") or []),
                    it.get("scrapedAt"),
                    now,
                ),
            )
            n += 1
        c.commit()
    return n, 0


def pick_new(n: int = 5) -> list[dict]:
    """Return the N oldest unseen no-website leads."""
    with closing(connect()) as c:
        rows = c.execute(
            """
            SELECT place_id, name, phone, address, google_url, rating, reviews,
                   category, image_url, image_urls, first_seen_at
            FROM leads
            WHERE (website IS NULL OR website = '')
              AND pushed_to_sheet = 0
            ORDER BY first_seen_at ASC
            LIMIT ?
            """,
            (n,),
        ).fetchall()
        return [dict(r) for r in rows]


def mark_pushed(place_ids: list[str]) -> int:
    if not place_ids:
        return 0
    with closing(connect()) as c:
        cur = c.execute(
            f"UPDATE leads SET pushed_to_sheet = 1 WHERE place_id IN ({','.join('?'*len(place_ids))})",
            place_ids,
        )
        c.commit()
        return cur.rowcount


def stats() -> dict:
    with closing(connect()) as c:
        total = c.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
        no_web = c.execute("SELECT COUNT(*) FROM leads WHERE website IS NULL OR website = ''").fetchone()[0]
        pushed = c.execute("SELECT COUNT(*) FROM leads WHERE pushed_to_sheet = 1").fetchone()[0]
        pending = c.execute("SELECT COUNT(*) FROM leads WHERE (website IS NULL OR website = '') AND pushed_to_sheet = 0").fetchone()[0]
    return {"total": total, "no_website": no_web, "pushed": pushed, "pending": pending}


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 1 and sys.argv[1] == "stats":
        print(json.dumps(stats(), indent=2))
    else:
        print(json.dumps(stats(), indent=2))
