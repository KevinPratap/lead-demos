"""
Google Maps scraper - extracts business data from page JS state.
Uses Playwright to load the page, then extracts from window object.
"""
import json
import time
import re
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\prata\AppData\Local\Programs\Python\Python311\Lib\site-packages")

from playwright.sync_api import sync_playwright

OUTPUT_FILE = Path("/home/prata/leads/data/playwright_leads_v2.json")

SEARCHES = [
    ("dental", "dental clinic in Andheri West Mumbai"),
    ("salon", "beauty salon in Bandra Mumbai"),
    ("gym", "gym in Juhu Mumbai"),
    ("barber", "barber shop in Andheri Mumbai"),
    ("skin", "skin clinic in Bandra Mumbai"),
    ("cafe", "cafe in Bandra Mumbai"),
    ("yoga", "yoga studio in Andheri Mumbai"),
    ("physio", "physiotherapy in Vile Parle Mumbai"),
    ("bakery", "bakery in Bandra Mumbai"),
    ("spa", "spa in Juhu Mumbai"),
]

def extract_phone(text):
    patterns = [
        r'[\+]?91[\s\-]?\d{10}',
        r'\d{3,4}[\s\-]\d{3,4}[\s\-]\d{4}',
        r'\d{5}[\s\-]\d{5}',
    ]
    phones = []
    for p in patterns:
        phones.extend(re.findall(p, text))
    return list(set(phones))

def scrape_niche(niche, query, page):
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
    print(f"\n[{niche}] {query}")
    page.goto(url, wait_until="networkidle", timeout=30000)
    time.sleep(3)
    
    # Try to extract data from the page's JavaScript state
    # Google Maps stores data in window.__INITIAL_STATE__ or similar
    result = page.evaluate("""
        () => {
            // Try multiple possible data locations
            const candidates = [
                window.__INITIAL_STATE__,
                window.__google_map_data__,
                window.APP_INITIALIZATION_STATE,
            ];
            
            for (const c of candidates) {
                if (c) return JSON.stringify(c).substring(0, 5000);
            }
            
            // Try to find data in script tags
            const scripts = document.querySelectorAll('script');
            for (const s of scripts) {
                const text = s.textContent;
                if (text.includes('APP_INITIALIZATION_STATE')) {
                    const match = text.match(/APP_INITIALIZATION_STATE\\s*=\\s*(\\[.+?\\]);/s);
                    if (match) return match[1].substring(0, 5000);
                }
            }
            
            return null;
        }
    """)
    
    if result:
        print(f"  Found JS state data: {len(result)} chars")
        print(f"  Preview: {result[:200]}")
    
    # Alternative: use the aria-label approach
    # Google Maps list items have aria-label with business name
    businesses = page.evaluate("""
        () => {
            const results = [];
            
            // Method 1: Look for result containers with aria labels
            const items = document.querySelectorAll('[aria-label]');
            items.forEach(item => {
                const label = item.getAttribute('aria-label');
                if (label && label.length > 5 && label.length < 200) {
                    // Check if it looks like a business name
                    const text = item.textContent || '';
                    const phoneMatch = text.match(/[\\+]?91[\\s\\-]?\\d{10}|\\d{3,4}[\\s\\-]\\d{3,4}[\\s\\-]\\d{4}/g);
                    results.push({
                        name: label,
                        text: text.substring(0, 300),
                        phones: phoneMatch || []
                    });
                }
            });
            
            return results;
        }
    """)
    
    print(f"  Businesses found: {len(businesses)}")
    
    leads = []
    seen = set()
    
    for biz in businesses:
        name = biz.get('name', '')
        if not name or name in seen or len(name) < 5:
            continue
        seen.add(name)
        
        phones = extract_phone(biz.get('text', ''))
        
        lead = {
            "niche": niche,
            "name": name,
            "phones": phones,
            "source": "google_maps_aria"
        }
        leads.append(lead)
        
        phone_str = ", ".join(phones) if phones else "no phone"
        print(f"  + {name[:60]} | {phone_str}")
    
    return leads


def main():
    all_leads = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
        )
        page = context.new_page()
        
        for niche, query in SEARCHES:
            try:
                leads = scrape_niche(niche, query, page)
                all_leads.extend(leads)
            except Exception as e:
                print(f"  Error: {e}")
            time.sleep(2)
        
        browser.close()
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_leads, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n=== DONE ===")
    print(f"Total leads: {len(all_leads)}")
    print(f"With phones: {sum(1 for l in all_leads if l['phones'])}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
