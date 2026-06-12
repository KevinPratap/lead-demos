"""Scrape Google Maps for 3 niches: beauty, gyms, diagnostics.
Target: 20+ leads per niche = 60+ total after filtering.
Filter: no existing website, has phone number, rating >= 4.0
"""
from __future__ import annotations
import sys, json, time
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import apify_client as ac
import lead_cache as lc

NICHES = {
    "beauty_salon": {
        "label": "Beauty Parlors & Salons",
        "queries": [
            "beauty parlour in Mumbai",
            "salon in Mumbai",
            "hair salon Mumbai",
            "unisex salon Mumbai",
        ],
    },
    "gym_fitness": {
        "label": "Gyms & Fitness Centers",
        "queries": [
            "gym in Mumbai",
            "fitness center Mumbai",
            "health club Mumbai",
            "crossfit gym Mumbai",
        ],
    },
    "diagnostic_lab": {
        "label": "Diagnostic Labs & Pathology Centers",
        "queries": [
            "diagnostic lab in Mumbai",
            "pathology lab Mumbai",
            "blood test center Mumbai",
            "medical testing lab Mumbai",
        ],
    },
}

MAX_RESULTS_PER_QUERY = 100  # Apify max per search
MIN_RATING = 4.0

def filter_leads(items: list[dict]) -> list[dict]:
    """Filter: no website, has phone, rating >= MIN_RATING."""
    good = []
    for it in items:
        website = (it.get("website") or "").strip()
        phone = (it.get("phone") or it.get("phoneUnformatted") or "").strip()
        rating = it.get("totalScore") or 0
        
        # Skip if has website
        if website:
            continue
        # Skip if no phone
        if not phone:
            continue
        # Skip if rating too low
        try:
            rating = float(rating)
        except (TypeError, ValueError):
            rating = 0
        if rating < MIN_RATING:
            continue
        
        good.append(it)
    return good


def scrape_niche(niche_key: str, niche_info: dict, max_per_query: int = 100) -> dict:
    """Scrape one niche across all its queries. Returns stats."""
    label = niche_info["label"]
    queries = niche_info["queries"]
    all_items = []
    
    print(f"\n{'='*60}")
    print(f"  NICHE: {label}")
    print(f"{'='*60}")
    
    for q in queries:
        print(f"\n--- Query: {q!r} ---")
        try:
            items = ac.run_scrape(q, max_results=max_per_query)
            print(f"  Raw results: {len(items)}")
            all_items.extend(items)
        except Exception as e:
            print(f"  ! FAILED: {e}", file=sys.stderr)
            continue
    
    if not all_items:
        print(f"\n  No results at all for {label}")
        return {"niche": niche_key, "label": label, "raw": 0, "ingested": 0, "filtered": []}
    
    # Deduplicate by placeId
    seen = set()
    unique = []
    for it in all_items:
        pid = it.get("placeId")
        if pid and pid not in seen:
            seen.add(pid)
            unique.append(it)
    
    print(f"\n  Unique (deduped): {len(unique)}")
    
    # Filter for our criteria
    filtered = filter_leads(unique)
    print(f"  After filter (no website, has phone, >= {MIN_RATING}★): {len(filtered)}")
    
    # Ingest all unique into DB (the filter is for reporting; we store all)
    ingested, _ = lc.ingest(unique)
    print(f"  Ingested into DB: {ingested}")
    
    # Show filtered leads
    if filtered:
        print(f"\n  Top filtered leads:")
        for i, ld in enumerate(filtered[:5]):
            print(f"    {i+1}. {ld.get('title','?')[:50]}")
            print(f"       ★{ld.get('totalScore','?')} | {ld.get('reviewsCount','?')} reviews")
            print(f"       📞 {ld.get('phone') or ld.get('phoneUnformatted') or '—'}")
            print(f"       📍 {ld.get('address','?')[:60]}")
    
    return {
        "niche": niche_key,
        "label": label,
        "raw": len(all_items),
        "unique": len(unique),
        "filtered": len(filtered),
        "ingested": ingested,
        "top_filtered": [
            {
                "name": ld.get("title"),
                "rating": ld.get("totalScore"),
                "reviews": ld.get("reviewsCount"),
                "phone": ld.get("phone") or ld.get("phoneUnformatted"),
                "address": ld.get("address"),
                "placeId": ld.get("placeId"),
            }
            for ld in filtered[:20]
        ],
    }


def main():
    results = {}
    total_filtered = 0
    
    for niche_key, niche_info in NICHES.items():
        res = scrape_niche(niche_key, niche_info, max_per_query=MAX_RESULTS_PER_QUERY)
        results[niche_key] = res
        total_filtered += res.get("filtered", 0)
    
    # Summary
    print(f"\n\n{'='*60}")
    print(f"  FINAL SUMMARY")
    print(f"{'='*60}")
    for nk, r in results.items():
        print(f"  {r['label']:40s} | raw: {r.get('raw',0):4d} | unique: {r.get('unique',0):4d} | filtered: {r.get('filtered',0):4d}")
    print(f"\n  TOTAL FILTERED LEADS: {total_filtered}")
    print(f"  Target: 60+ | {'✅ MET' if total_filtered >= 60 else '❌ SHORT by ' + str(60 - total_filtered)}")
    
    # DB stats
    s = lc.stats()
    print(f"\n  DB Stats: total={s['total']} no_website={s['no_website']} pending={s['pending']}")
    
    # Save results JSON
    out_path = Path("/home/prata/leads/data/multiniche_results.json")
    out_path.write_text(json.dumps(results, indent=2, default=str))
    print(f"\n  Full results saved to: {out_path}")
    
    return results


if __name__ == "__main__":
    main()
