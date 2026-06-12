"""
Lead scraper using SerpAPI - free tier (100 searches/month).
Extracts business names, phones, addresses from Google local search.
"""
import json
import time
import re
import urllib.request
import urllib.parse
import yaml
from pathlib import Path
from datetime import datetime

# Read API key from config
_cfg_path = Path(__file__).parent / "config.yaml"
with open(_cfg_path) as _f:
    API_KEY = yaml.safe_load(_f)["serpapi"]["api_key"]
OUTPUT_FILE = Path("/home/prata/leads/data/serpapi_leads.json")

SEARCHES = [
    ("dental", "dental clinic in Andheri West Mumbai", "Mumbai"),
    ("dental", "dentist in Vile Parle Mumbai", "Mumbai"),
    ("salon", "beauty salon in Bandra Mumbai", "Mumbai"),
    ("salon", "hair salon in Juhu Mumbai", "Mumbai"),
    ("gym", "gym in Juhu Mumbai", "Mumbai"),
    ("gym", "fitness center in Andheri Mumbai", "Mumbai"),
    ("barber", "barber shop in Andheri Mumbai", "Mumbai"),
    ("barber", "mens salon in Bandra Mumbai", "Mumbai"),
    ("skin", "skin clinic in Bandra Mumbai", "Mumbai"),
    ("skin", "dermatologist in Andheri Mumbai", "Mumbai"),
    ("cafe", "cafe in Bandra Mumbai", "Mumbai"),
    ("cafe", "coffee shop in Andheri Mumbai", "Mumbai"),
    ("yoga", "yoga studio in Andheri Mumbai", "Mumbai"),
    ("physio", "physiotherapy in Vile Parle Mumbai", "Mumbai"),
    ("bakery", "bakery in Bandra Mumbai", "Mumbai"),
    ("spa", "spa in Juhu Mumbai", "Mumbai"),
    ("spa", "massage in Andheri Mumbai", "Mumbai"),
    ("eyelash", "eyelash extension in Bandra Mumbai", "Mumbai"),
]

def extract_phones(text):
    """Extract Indian phone numbers from text."""
    if not text:
        return []
    patterns = [
        r'[\+]?91[\s\-]?\d{10}',
        r'\d{3,4}[\s\-]\d{3,4}[\s\-]\d{4}',
        r'\d{5}[\s\-]\d{5}',
    ]
    phones = set()
    for p in patterns:
        for m in re.findall(p, text):
            # Clean up
            clean = re.sub(r'[\s\-]', '', m)
            if len(clean) >= 10:
                phones.add(m.strip())
    return list(phones)

def search_serpapi(query, num=10):
    """Search via SerpAPI Google engine."""
    params = {
        "q": query,
        "api_key": API_KEY,
        "engine": "google",
        "num": num,
        "gl": "in",
        "hl": "en",
    }
    url = f"https://serpapi.com/search?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Hermes/1.0"})
    
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())

def scrape_niche(niche, query, city):
    """Scrape leads for one niche query."""
    print(f"\n[{niche}] {query}")
    
    data = search_serpapi(query, 10)
    leads = []
    
    # Extract from organic results (business websites)
    for r in data.get("organic_results", []):
        title = r.get("title", "")
        link = r.get("link", "")
        snippet = r.get("snippet", "")
        
        # Skip aggregator sites
        skip = ["justdial", "asklaila", "practo", "lybrate", "magicpin",
                "5bestincity", "cybo", "yelp", "tripadvisor", "wikipedia",
                "facebook", "instagram", "linkedin", "youtube", "reddit",
                "quora", "indiamart", "tradeindia", "exportersindia"]
        
        link_lower = link.lower()
        title_lower = title.lower()
        if any(s in link_lower or s in title_lower for s in skip):
            continue
        
        # Extract phones from snippet and title
        phones = extract_phones(snippet + " " + title)
        
        if title and len(title) > 5:
            leads.append({
                "name": title.split(" - ")[0].split(" | ")[0].strip(),
                "phones": phones,
                "url": link,
                "snippet": snippet[:200],
                "source": "organic"
            })
    
    # Extract from local results (Google Maps listings)
    local_results = data.get("local_results", [])
    if isinstance(local_results, list):
        for lr in local_results:
            name = lr.get("title", lr.get("name", ""))
            phones = []
            
            # Phone might be in different fields
            if "phone" in lr and lr["phone"]:
                phones.append(lr["phone"])
            
            # Also extract from description/snippet
            desc = lr.get("description", lr.get("snippet", ""))
            phones.extend(extract_phones(desc))
            
            address = lr.get("address", "")
            rating = lr.get("rating", "")
            reviews = lr.get("reviews", "")
            
            # Thumbnail / image
            thumbnail = lr.get("thumbnail", "")
            
            if name:
                leads.append({
                    "name": name,
                    "phones": list(set(phones)),
                    "address": address,
                    "rating": rating,
                    "reviews": reviews,
                    "source": "local"
                })
    
    # Deduplicate by name
    seen = set()
    unique_leads = []
    for l in leads:
        key = l["name"].lower()[:30]
        if key not in seen:
            seen.add(key)
            unique_leads.append(l)
    
    print(f"  Found: {len(unique_leads)} unique leads")
    for l in unique_leads[:5]:
        phone_str = ", ".join(l["phones"][:2]) if l["phones"] else "no phone"
        print(f"  + {l['name'][:60]} | {phone_str}")
    
    return unique_leads

def main():
    all_leads = []
    total_searches = 0
    
    for niche, query, city in SEARCHES:
        try:
            leads = scrape_niche(niche, query, city)
            for l in leads:
                l["niche"] = niche
                l["city"] = city
                l["query"] = query
                l["scraped_at"] = datetime.now().isoformat()
            all_leads.extend(leads)
            total_searches += 1
        except Exception as e:
            print(f"  Error: {e}")
        
        time.sleep(1.5)  # Rate limit
    
    # Deduplicate across all searches
    seen = set()
    final_leads = []
    for l in all_leads:
        key = l["name"].lower()[:40]
        if key not in seen:
            seen.add(key)
            final_leads.append(l)
    
    # Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(final_leads, f, indent=2, ensure_ascii=False)
    
    # Stats
    with_phone = [l for l in final_leads if l.get("phones")]
    
    print(f"\n{'='*60}")
    print(f"DONE — {total_searches} searches used")
    print(f"Total unique leads: {len(final_leads)}")
    print(f"With phone numbers: {len(with_phone)}")
    print(f"Without phone: {len(final_leads) - len(with_phone)}")
    print(f"\nBy niche:")
    niches = set(l["niche"] for l in final_leads)
    for n in sorted(niches):
        count = sum(1 for l in final_leads if l["niche"] == n)
        with_p = sum(1 for l in final_leads if l["niche"] == n and l.get("phones"))
        print(f"  {n}: {count} ({with_p} with phone)")
    print(f"\nSaved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
