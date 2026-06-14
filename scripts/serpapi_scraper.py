import sys, time, yaml, requests
from pathlib import Path

# Add scripts dir to path to import lead_cache
sys.path.append(str(Path(__file__).resolve().parent))
import lead_cache

def main():
    cfg_p = Path(__file__).resolve().parent.parent / "config.yaml"
    with open(cfg_p) as f:
        cfg = yaml.safe_load(f)
    
    api_key = cfg["serpapi"]["api_key"]
    queries = cfg["queries"]
    all_leads = []
    
    for idx, q in enumerate(queries, 1):
        print(f"[{idx}/{len(queries)}] Querying: {q}")
        params = {"engine": "google_maps", "q": q, "api_key": api_key, "type": "search"}
        try:
            r = requests.get("https://serpapi.com/search", params=params, timeout=20)
            r.raise_for_status()
            for lr in r.json().get("local_results", []):
                all_leads.append({
                    "title": lr.get("title"),
                    "rating": lr.get("rating"),
                    "reviews": lr.get("reviews"),
                    "phone": lr.get("phone"),
                    "address": lr.get("address"),
                    "website": lr.get("website"),
                    "gps_coordinates": lr.get("gps_coordinates"),
                    "place_id": lr.get("place_id")
                })
        except Exception as e:
            print(f"Error querying {q}: {e}")
        time.sleep(1.5)

    if all_leads:
        inserted, skipped = lead_cache.ingest(all_leads)
        print(f"\nIngested {inserted} leads ({skipped} skipped).")
    else:
        print("No leads found to ingest.")

if __name__ == "__main__":
    main()
