"""Google Maps Places API (New) client.

Replaces Apify Maps Scraper with direct Places API (New) Text Search.
$200/mo free credit → ~6,250 searches/month → more than enough for daily leads.

API docs: https://developers.google.com/maps/documentation/places/web-service/text-search
"""

from __future__ import annotations
import os
import time
import requests
from pathlib import Path

BASE_URL = "https://places.googleapis.com/v1/places:searchText"

# Fields we want back. Cost: Text Search base + per-field Places Details pricing.
# With $200/mo credit, even advanced fields on 100 results/day is ~$16/mo.
FIELD_MASK = (
    "places.id,places.displayName,places.formattedAddress,"
    "places.nationalPhoneNumber,places.websiteUri,"
    "places.rating,places.userRatingCount,places.googleMapsUri,"
    "places.primaryTypeDisplayName,places.photos,"
    "places.businessStatus,places.priceLevel"
)


def _api_key() -> str:
    """Resolve API key from env or config."""
    key = os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()
    if key:
        return key

    # Try project config
    cfg_path = Path(__file__).resolve().parent.parent / "config.yaml"
    if cfg_path.exists():
        import yaml
        cfg = yaml.safe_load(cfg_path.read_text())
        key = (cfg.get("google") or {}).get("api_key", "").strip()
        if key:
            return key

    raise RuntimeError(
        "GOOGLE_MAPS_API_KEY not set. "
        "Export it or add google.api_key to ~/leads/config.yaml"
    )


def search_places(
    query: str,
    max_results: int = 20,
    api_key: str | None = None,
) -> list[dict]:
    """Run a Text Search and return normalized place dicts.

    Returns up to max_results (API caps at 20 per call).
    Each dict has keys matching the leads table schema.
    """
    key = api_key or _api_key()
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": FIELD_MASK,
    }

    all_places = []
    page_token = None
    pages = 0

    while len(all_places) < max_results:
        pages += 1
        body = {"textQuery": query}
        if page_token:
            body["pageToken"] = page_token

        resp = requests.post(BASE_URL, json=body, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        for place in data.get("places", []):
            all_places.append(_normalize(place))
            if len(all_places) >= max_results:
                break

        page_token = data.get("nextPageToken")
        if not page_token:
            break
        # Google requires a short delay before the next page token is valid
        time.sleep(2)

    return all_places


def get_photo_url(photo_name: str, api_key: str | None = None, max_width: int = 400) -> str | None:
    """Fetch a photo URL from a photo resource name.

    photo_name looks like: 'places/ChIJ.../photos/...'
    Returns the direct image URL, or None on failure.
    """
    key = api_key or _api_key()
    url = f"https://places.googleapis.com/v1/{photo_name}/media"
    params = {"maxWidthPx": max_width, "skipHttpRedirect": "false"}
    headers = {"X-Goog-Api-Key": key}

    try:
        # We just want the redirect URL, not the image bytes
        resp = requests.get(url, params=params, headers=headers, allow_redirects=False, timeout=10)
        if resp.status_code in (302, 301, 307, 308):
            return resp.headers.get("Location")
        # If it returns the image directly, use the request URL as-is
        if resp.status_code == 200:
            return resp.url
    except Exception:
        pass
    return None


def _normalize(place: dict) -> dict:
    """Convert Places API (New) response to our standard flat dict."""
    display = place.get("displayName", {})
    address = place.get("formattedAddress", "")
    phone = place.get("nationalPhoneNumber", "") or ""
    website = place.get("websiteUri", "") or None
    maps_uri = place.get("googleMapsUri", "")

    # Best photo name (for later URL resolution)
    photos = place.get("photos", [])
    photo_name = photos[0]["name"] if photos else None

    # Primary type
    ptype = place.get("primaryTypeDisplayName", {})
    category = ptype.get("text", "") if ptype else ""

    return {
        "place_id": place.get("id", ""),
        "name": display.get("text", "") if display else "",
        "phone": phone,
        "address": address,
        "website": website,
        "google_url": maps_uri,
        "rating": place.get("rating"),
        "reviews": place.get("userRatingCount", 0),
        "category": category,
        "image_url": None,  # resolved lazily if needed
        "photo_name": photo_name,
    }


def run_scrape(query: str, max_results: int = 100) -> list[dict]:
    """Public interface — same signature as apify_client.run_scrape."""
    places = search_places(query, max_results=max_results)

    # Resolve photo URLs (best-effort, non-blocking)
    key = _api_key()
    for p in places:
        if p.get("photo_name"):
            url = get_photo_url(p["photo_name"], api_key=key)
            if url:
                p["image_url"] = url

    # Add scraped_at timestamp
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for p in places:
        p["scraped_at"] = now

    return places


def search_nearby(
    query: str,
    location: str | None = None,
    radius: int = 5000,
    max_results: int = 20,
    api_key: str | None = None,
) -> list[dict]:
    """Nearby Search (alternative to Text Search for geofenced queries).

    Uses the new Places API Nearby Search endpoint.
    """
    key = api_key or _api_key()
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": FIELD_MASK,
    }

    body = {
        "maxResultCount": min(max_results, 20),
        "rankPreference": "DISTANCE",
        "textQuery": query,
    }

    if location:
        body["locationRestriction"] = {
            "circle": {
                "center": {"latitude": 19.0760, "longitude": 72.8777},  # Mumbai default
                "radius": float(radius),
            }
        }

    resp = requests.post(url, json=body, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    places = [_normalize(p) for p in data.get("places", [])]
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for p in places:
        p["scraped_at"] = now

    return places


if __name__ == "__main__":
    import json
    results = search_places("dentist in Mumbai", max_results=5)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nTotal: {len(results)} places")
