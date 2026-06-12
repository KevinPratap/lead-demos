#!/usr/bin/env python3
import json
import time
import re
import requests
from datetime import datetime
from pathlib import Path

API_KEY = "7e8fbacc1bfa5d0a1b162f596e734999342199bb11a1c0472771adf210e500e6"
OUTPUT_PATH = Path("/home/prata/leads/data/serpapi_leads.json")

SEARCH_QUERIES = [
    ("dental", "dental clinic in Andheri West Mumbai"),
    ("dental", "dentist in Vile Parle Mumbai"),
    ("salon", "beauty salon in Bandra Mumbai"),
    ("salon", "hair salon in Juhu Mumbai"),
    ("gym", "gym in Juhu Mumbai"),
    ("gym", "fitness center in Andheri Mumbai"),
    ("barber", "barber shop in Andheri Mumbai"),
    ("barber", "mens salon in Bandra Mumbai"),
    ("skin", "skin clinic in Bandra Mumbai"),
    ("skin", "dermatologist in Andheri Mumbai"),
    ("cafe", "cafe in Bandra Mumbai"),
    ("cafe", "coffee shop in Andheri Mumbai"),
    ("yoga", "yoga studio in Andheri Mumbai"),
    ("physio", "physiotherapy in Vile Parle Mumbai"),
    ("bakery", "bakery in Bandra Mumbai"),
    ("spa", "spa in Juhu Mumbai"),
    ("spa", "massage in Andheri Mumbai"),
    ("eyelash", "eyelash extension in Bandra Mumbai"),
]

AGGREGATORS = [
    "justdial", "asklaila", "practo", "lybrate", "magicpin",
    "5bestincity", "cybo", "yelp", "tripadvisor", "wikipedia",
    "facebook", "instagram", "linkedin", "youtube", "reddit",
    "quora", "indiamart", "tradeindia", "exportersindia"
]

def clean_phone(phone_str):
    if not phone_str:
        return None
    cleaned = re.sub(r'[^\d+]', '', phone_str)
    if len(cleaned) == 12 and cleaned.startswith('91'):
        cleaned = '+' + cleaned
    return cleaned

def extract_phones(text):
    if not text:
        return []
    raw_matches = re.findall(r'\+?[0-9][0-9\-\s]{7,14}[0-9]', text)
    phones = set()
    for m in raw_matches:
        cleaned = clean_phone(m)
        if not cleaned:
            continue
        if len(cleaned) == 10 and cleaned[0] in '6789':
            phones.add(cleaned)
        elif len(cleaned) == 11 and cleaned.startswith('0') and cleaned[1] in '6789':
            phones.add(cleaned)
        elif len(cleaned) == 13 and cleaned.startswith('+91') and cleaned[3] in '6789':
            phones.add(cleaned)
        elif len(cleaned) == 11 and cleaned.startswith('022'):
            phones.add(cleaned)
        elif len(cleaned) == 10 and cleaned.startswith('22'):
            phones.add(cleaned)
            
    patterns = [
        r'[\+]?91[\s\-]?\d{10}',
        r'\d{3,4}[\s\-]\d{3,4}[\s\-]\d{4}',
        r'\d{5}[\s\-]\d{5}',
    ]
    for p in patterns:
        for m in re.findall(p, text):
            cleaned = clean_phone(m)
            if cleaned and len(cleaned) >= 8:
                phones.add(cleaned)
                
    return list(phones)

def deduplicate_phones(phones):
    if not phones:
        return []
    unique_phones = {}
    for p in phones:
        digits_only = re.sub(r'\D', '', p)
        if len(digits_only) >= 10:
            key = digits_only[-10:]
            if key not in unique_phones:
                unique_phones[key] = p
            else:
                existing = unique_phones[key]
                if not existing.startswith('+') and p.startswith('+'):
                    unique_phones[key] = p
                elif len(existing) < len(p):
                    unique_phones[key] = p
        else:
            unique_phones[p] = p
    return list(unique_phones.values())

def is_aggregator(url, name):
    url_lower = (url or "").lower()
    name_lower = (name or "").lower()
    for s in AGGREGATORS:
        if s in url_lower or s in name_lower:
            return True
    return False

def query_serpapi(query):
    params = {
        "q": query,
        "api_key": API_KEY,
        "engine": "google",
        "num": 10,
        "gl": "in",
        "hl": "en"
    }
    r = requests.get("https://serpapi.com/search", params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def merge_leads(existing, lead):
    # Merge phones
    existing_phones = existing.get("phones") or []
    lead_phones = lead.get("phones") or []
    existing["phones"] = deduplicate_phones(list(set(existing_phones + lead_phones)))
    
    # Merge fields if they are missing/empty in existing
    for field in ["address", "website", "rating"]:
        if not existing.get(field) and lead.get(field):
            existing[field] = lead[field]
            
    # Upgrade source to local if lead is local
    if existing.get("source") == "organic" and lead.get("source") == "local":
        existing["source"] = "local"
        for field in ["address", "website", "rating"]:
            if lead.get(field):
                existing[field] = lead[field]
                
    return existing

def process_organic_results(organic_results, niche):
    leads = []
    timestamp = datetime.utcnow().isoformat() + "Z"
    for r in organic_results:
        title = r.get("title", "")
        link = r.get("link", "")
        snippet = r.get("snippet", "")
        
        if not title:
            continue
            
        # Clean title to get business name
        name = title.split(" - ")[0].split(" | ")[0].strip()
        
        if is_aggregator(link, name):
            continue
            
        phones = extract_phones(snippet + " " + title)
        
        leads.append({
            "name": name,
            "phones": deduplicate_phones(phones),
            "address": None,
            "website": link,
            "rating": None,
            "source": "organic",
            "niche": niche,
            "timestamp": timestamp
        })
    return leads

def process_local_results(local_results, niche):
    leads = []
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    if isinstance(local_results, dict):
        places = local_results.get("places", [])
    elif isinstance(local_results, list):
        places = local_results
    else:
        places = []
        
    for p in places:
        name = p.get("title", p.get("name", ""))
        if not name:
            continue
            
        phones = []
        if p.get("phone"):
            cleaned = clean_phone(p["phone"])
            if cleaned:
                phones.append(cleaned)
                
        # Also extract phones from description or snippet
        desc = p.get("description", p.get("snippet", ""))
        phones.extend(extract_phones(desc))
        
        address = p.get("address")
        website = p.get("website") or p.get("links", {}).get("website")
        rating = p.get("rating")
        
        leads.append({
            "name": name,
            "phones": deduplicate_phones(phones),
            "address": address if address else None,
            "website": website if website else None,
            "rating": rating if rating else None,
            "source": "local",
            "niche": niche,
            "timestamp": timestamp
        })
    return leads

def main():
    print("Starting SerpAPI Lead Scraper v2...")
    all_leads = []
    
    for idx, (niche, query) in enumerate(SEARCH_QUERIES, 1):
        print(f"[{idx}/{len(SEARCH_QUERIES)}] Querying '{query}' ({niche})...")
        try:
            data = query_serpapi(query)
            
            # Process organic results
            organic_leads = process_organic_results(data.get("organic_results", []), niche)
            
            # Process local results
            local_leads = process_local_results(data.get("local_results", []), niche)
            
            query_leads = organic_leads + local_leads
            print(f"  -> Found {len(query_leads)} raw leads ({len(local_leads)} local, {len(organic_leads)} organic)")
            all_leads.extend(query_leads)
            
        except Exception as e:
            print(f"  -> Error scraping '{query}': {e}")
            
        time.sleep(1.5)
        
    # Deduplicate and merge leads
    print("\nDeduplicating leads...")
    deduped_leads = {}
    for lead in all_leads:
        name = lead.get("name", "")
        if not name:
            continue
        key = name.strip().lower()[:40]
        if key not in deduped_leads:
            deduped_leads[key] = lead
        else:
            deduped_leads[key] = merge_leads(deduped_leads[key], lead)
            
    final_leads = list(deduped_leads.values())
    
    # Save output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(final_leads, f, indent=2, ensure_ascii=False)
        
    # Stats
    with_phone = [l for l in final_leads if l.get("phones")]
    
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"Total Unique Leads: {len(final_leads)}")
    print(f"Leads with Phone Numbers: {len(with_phone)}")
    print(f"Leads without Phone Numbers: {len(final_leads) - len(with_phone)}")
    print("\nBreakdown by Niche:")
    
    niche_counts = {}
    for l in final_leads:
        n = l["niche"]
        niche_counts[n] = niche_counts.get(n, 0) + 1
        
    niche_phone_counts = {}
    for l in with_phone:
        n = l["niche"]
        niche_phone_counts[n] = niche_phone_counts.get(n, 0) + 1
        
    for niche in sorted(niche_counts.keys()):
        total = niche_counts[niche]
        with_p = niche_phone_counts.get(niche, 0)
        print(f"  - {niche}: {total} leads ({with_p} with phone)")
        
    print(f"\nSaved results to: {OUTPUT_PATH}")
    print("=" * 60)

if __name__ == "__main__":
    main()
