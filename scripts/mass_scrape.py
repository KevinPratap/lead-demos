#!/usr/bin/env python3
"""Mass lead scrape — area × niche rotation to hit 1000+ leads."""
import sys, time, yaml
sys.path.insert(0, 'scripts')
import google_maps_client as gmc
import lead_cache as lc

cfg = yaml.safe_load(open('config.yaml'))

# 16 Mumbai areas × 10 niches = 160 queries × 20 results = up to 3200 raw hits
areas = [
    "Bandra West", "Juhu", "Powai", "Andheri West", "Chembur",
    "Thane", "Navi Mumbai", "Colaba", "Worli", "Lower Parel",
    "Malad West", "Goregaon West", "Borivali West", "Dadar",
    "Kurla", "Ghatkopar", "Mulund", "Kandivali West",
    "Marine Lines", "Vile Parle East", "Mahim", "Sion",
    "Vasai West", "Mira Road", "Kalyan West", "Dombivli",
]

niches = [
    "dental clinic",
    "dentist",
    "hair salon",
    "beauty salon",
    "gym",
    "fitness center",
    "spa",
    "skin clinic",
    "physiotherapy clinic",
    "yoga studio",
    "diagnostic center",
    "pathology lab",
    "cafe",
    "bakery",
    "optical store",
    "dermatologist",
    "pharmacy",
    "restaurant",
]

total_new = 0
total_seen = 0

for i, area in enumerate(areas):
    for j, niche in enumerate(niches):
        query = f"{niche} in {area} Mumbai"
        print(f"\n[{i*len(niches)+j+1}/{len(areas)*len(niches)}] {query}")
        try:
            results = gmc.run_scrape(query, max_results=20)
            new, seen = lc.ingest(results)
            total_new += new
            total_seen += seen
            print(f"  → {new} new, {seen} seen | running: {total_new} new / {total_new+total_seen} total")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        
        # Be gentle to Google's API — 1.5s between queries
        time.sleep(1.5)
    
    # Slightly longer pause between areas
    time.sleep(2)

# Final count
import sqlite3
db = sqlite3.connect('data/leads.db')
final = db.execute('SELECT COUNT(*) FROM leads').fetchone()[0]
db.close()

print(f"\n=== DONE ===")
print(f"This run: {total_new} new, {total_seen} duplicates")
print(f"Total leads in DB: {final}")
