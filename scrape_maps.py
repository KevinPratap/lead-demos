"""
Free lead scraper using Playwright to scrape Google Maps.
No API key needed - uses browser automation.
"""
import json
import time
import re
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\prata\AppData\Local\Programs\Python\Python311\Lib\site-packages")

from playwright.sync_api import sync_playwright

OUTPUT_FILE = Path("/home/prata/leads/data/playwright_leads.json")

# Search queries for different niches
SEARCHES = [
    ("dental", "dental clinic in Andheri West Mumbai"),
    ("salon", "beauty salon in Bandra Mumbai"),
    ("gym", "gym in Juhu Mumbai"),
    ("barber", "barber shop in Andheri Mumbai"),
    ("skin", "skin clinic in Mumbai"),
    ("cafe", "cafe in Bandra Mumbai"),
    ("yoga", "yoga studio in Andheri Mumbai"),
    ("physio", "physiotherapy in Vile Parle Mumbai"),
    ("bakery", "bakery in Bandra Mumbai"),
    ("spa", "spa in Juhu Mumbai"),
]

def scrape_google_maps(search_query, niche, page):
    """Scrape business listings from Google Maps search results."""
    url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
    print(f"  Navigating to: {url}")
    
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)  # Wait for results to load
    
    # Scroll down to load more results
    for _ in range(3):
        page.evaluate("window.scrollBy(0, 500)")
        time.sleep(1)
    
    # Extract business data from the page
    # Google Maps renders business cards with name, phone, address
    businesses = page.evaluate("""
        () => {
            const results = [];
            // Business cards in search results
            const cards = document.querySelectorAll('div[class*="V0h1Ob"], div[class*="Nv2PK"], a[href*="maps/place"]');
            
            cards.forEach(card => {
                const nameEl = card.querySelector('div[class*="qBF1Pd"], div[class*="fontHeadlineSmall"], span[class*="fontHeadline"]');
                const name = nameEl ? nameEl.textContent.trim() : '';
                
                // Phone - look for phone patterns in all text
                const allText = card.textContent || '';
                const phoneMatch = allText.match(/[\+]?91[\s\-]?\d{10}|\d{3,4}[\s\-]\d{3,4}[\s\-]\d{4}/g);
                const phones = phoneMatch ? [...new Set(phoneMatch)] : [];
                
                // Address
                const addrEl = card.querySelector('div[class*="W4Efsd"], div[class*="fontBodyMedium"]');
                const address = addrEl ? addrEl.textContent.trim() : '';
                
                // Rating
                const ratingEl = card.querySelector('span[class*="MW4etd"], span[class*="fontDisplayLarge"]');
                const rating = ratingEl ? ratingEl.textContent.trim() : '';
                
                if (name && name.length > 3) {
                    results.push({name, phones, address, rating});
                }
            });
            
            return results;
        }
    """)
    
    return businesses


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
            print(f"\n[{niche}] {query}")
            try:
                businesses = scrape_google_maps(query, niche, page)
                print(f"  Found: {len(businesses)} businesses")
                
                for biz in businesses:
                    lead = {
                        "niche": niche,
                        "name": biz["name"],
                        "phones": biz["phones"],
                        "address": biz["address"],
                        "rating": biz["rating"],
                        "source": "google_maps_scrape"
                    }
                    all_leads.append(lead)
                    phone_str = ", ".join(biz["phones"]) if biz["phones"] else "no phone"
                    print(f"  + {biz['name'][:60]} | {phone_str}")
                    
            except Exception as e:
                print(f"  Error: {e}")
            
            time.sleep(3)  # Rate limit between searches
        
        browser.close()
    
    # Save results
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_leads, f, indent=2)
    
    print(f"\n\n=== DONE ===")
    print(f"Total leads: {len(all_leads)}")
    print(f"With phones: {sum(1 for l in all_leads if l['phones'])}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
