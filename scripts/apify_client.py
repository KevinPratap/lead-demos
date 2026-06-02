"""Apify client: runs the Google Maps Scraper actor and returns the dataset.

Actor: compass/crawler-google-places (the YouTube video used this one — most popular,
most results, free-tier friendly).

Usage:
    from apify_client import run_scrape
    items = run_scrape(query="dental clinic in Mumbai", max_results=100)

Each item is a dict with at least: title, phone, website, url (Google Maps link),
address, rating, reviewsCount, categoryName, location, placeId.
"""
from __future__ import annotations
import os, sys, time, json
from typing import Any
import requests
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/hermes/leads/.env"))

APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "")
BASE = "https://api.apify.com/v2"
# Public, well-maintained Google Maps scraper. 3.6M users, 0.004 USD per result approx.
ACTOR_ID = "compass~crawler-google-places"


def _auth() -> dict:
    return {"Authorization": f"Bearer {APIFY_TOKEN}"}


def run_scrape(query: str, max_results: int = 100, language: str = "en",
               wait_timeout: int = 600) -> list[dict]:
    """Start the actor, wait for it to finish, return all dataset items.

    Uses async start + polling (more reliable than run-sync-get-dataset-items,
    which can return HTTP 201 with a partial dataset before the run finishes).
    """
    if not APIFY_TOKEN or APIFY_TOKEN == "apify_...":
        raise RuntimeError("APIFY_TOKEN missing in ~/.config/hermes/leads/.env")

    actor_input = {
        "searchStringsArray": [query],
        "maxCrawledPlacesPerSearch": max_results,
        "language": language,
        "maxImages": 1,
        "maxReviews": 0,
        "scrapeReviewerName": False,
        "includePeopleAlsoSearch": False,
        "oneReviewPerPlace": True,
    }

    # 1) Start the actor run ASYNCHRONOUSLY
    print(f"[apify] starting actor for: {query!r} (max {max_results})", file=sys.stderr)
    r = requests.post(
        f"{BASE}/acts/{ACTOR_ID}/runs",
        params={"token": APIFY_TOKEN, "memory": 512},
        headers=_auth(),
        json=actor_input,
        timeout=60,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Apify run start failed: HTTP {r.status_code}\n{r.text[:500]}")
    run = r.json()["data"]
    run_id = run["id"]
    dataset_id = run["defaultDatasetId"]
    print(f"[apify] run_id={run_id} status={run.get('status')}", file=sys.stderr)

    # 2) Poll until terminal state
    deadline = time.time() + wait_timeout
    terminal = {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}
    while time.time() < deadline:
        rr = requests.get(
            f"{BASE}/acts/{ACTOR_ID}/runs/{run_id}",
            params={"token": APIFY_TOKEN},
            headers=_auth(),
            timeout=30,
        )
        if rr.status_code != 200:
            raise RuntimeError(f"Poll failed: HTTP {rr.status_code}")
        st = rr.json()["data"]["status"]
        if st in terminal:
            break
        time.sleep(5)
    else:
        raise RuntimeError(f"Apify run {run_id} did not finish within {wait_timeout}s (last status: {st})")

    if st != "SUCCEEDED":
        raise RuntimeError(f"Apify run {run_id} ended with status {st}")

    # 3) Fetch the dataset
    items = requests.get(
        f"{BASE}/datasets/{dataset_id}/items",
        params={"token": APIFY_TOKEN, "clean": "true", "limit": 1000},
        headers=_auth(),
        timeout=60,
    ).json()
    if not isinstance(items, list):
        raise RuntimeError(f"Unexpected dataset shape: {type(items)}")

    print(f"[apify] got {len(items)} items for {query!r} (status={st})", file=sys.stderr)
    return items


def cost_estimate(items: list[dict]) -> float:
    """Rough USD estimate. compass charges ~$0.004/result on free tier."""
    return round(len(items) * 0.004, 4)


if __name__ == "__main__":
    # CLI: python apify_client.py "dental clinic in Mumbai" 100
    q = sys.argv[1] if len(sys.argv) > 1 else "dental clinic in Mumbai"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    data = run_scrape(q, n)
    print(f"\nResults: {len(data)} | est cost: ${cost_estimate(data)}")
    if data:
        print("\nSample item keys:", list(data[0].keys())[:15])
        print("\nFirst item:")
        print(json.dumps(data[0], indent=2)[:800])
