import yaml
import requests
from pathlib import Path

cfg_path = Path(__file__).resolve().parent.parent / "config.yaml"
with open(cfg_path) as f:
    cfg = yaml.safe_load(f)

api_key = cfg["serpapi"]["api_key"]
print("Using API key:", api_key[:10] + "...")

# Query using engine=google
print("--- TESTING ENGINE=google ---")
params_google = {
    "q": "dental clinic in Mumbai",
    "api_key": api_key,
    "engine": "google",
    "num": 5,
    "gl": "in",
    "hl": "en"
}
try:
    r = requests.get("https://serpapi.com/search", params=params_google, timeout=20)
    data = r.json()
    print("Top level keys in google engine:", list(data.keys()))
    local_results = data.get("local_results", [])
    print(f"Found {len(local_results)} local results in google engine.")
    if local_results:
        print("First local result keys:", list(local_results[0].keys()))
        print("First local result sample:", {k: local_results[0][k] for k in ["title", "phone", "address", "website", "rating"] if k in local_results[0]})
except Exception as e:
    print("Google engine failed:", e)

# Query using engine=google_maps
print("\n--- TESTING ENGINE=google_maps ---")
params_maps = {
    "q": "dental clinic in Mumbai",
    "api_key": api_key,
    "engine": "google_maps",
    "type": "search",
    "num": 5,
}
try:
    r = requests.get("https://serpapi.com/search", params=params_maps, timeout=20)
    data = r.json()
    print("Top level keys in google_maps engine:", list(data.keys()))
    local_results = data.get("local_results", [])
    print(f"Found {len(local_results)} local results in google_maps engine.")
    if local_results:
        print("First local result keys in maps:", list(local_results[0].keys()))
        sample_keys = ["title", "phone", "address", "website", "rating", "place_id", "gps_coordinates", "thumbnail"]
        print("First local result sample in maps:", {k: local_results[0][k] for k in sample_keys if k in local_results[0]})
except Exception as e:
    print("Google maps engine failed:", e)
