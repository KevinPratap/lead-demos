"""
Free lead scraper - Google Maps with phone extraction.
Clicks into each business to get phone numbers.
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
    """Extract Indian phone numbers from text."""
    patterns = [
        r'[\+]?91[\s\-]?\d{10}',
        r'\d{3,4}[\s\-]\d{3,4}[\s\-]\d{4}',
        r'\d{5}[\s\-]\d{5}',
    ]
    phones = []
    for p in patterns:
        matches = re.findall(p, text)
        phones.extend(matches)
    return list(set(phones))

def scrape_niche(niche, query, page):
    """Scrape businesses for one niche, clicking each for phone."""
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
    print(f"\n[{niche}] {query}")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    time.sleep(5)
    
    # Scroll to load more results
    for _ in range(3):
        page.evaluate("window.scrollBy(0, 400)")
        time.sleep(1.5)
    
    # Get all business card links
    cards = page.query_selector_all('a[href*="maps/place"]')
    print(f"  Found {len(cards)} business cards")
    
    leads = []
    seen_names = set()
    
    for i, card in enumerate(cards[:8]):  # Top 8 per niche
        try:
            # Click the card to open details
            card.click()
            time.sleep(3)
            
            # Extract details from the detail panel
            detail_text = page.evaluate("""
                () => {
                    // The detail panel is usually on the right side
                    const panel = document.querySelector('div[class*="m6QErb"]') 
                               || document.querySelector('div[role="main"]')
                               || document.body;
                    return panel ? panel.textContent : document.body.textContent;
                }
            """)
            
            # Get business name from the detail panel
            name = page.evaluate("""
                () => {
                    const h1 = document.querySelector('h1');
                    return h1 ? h1.textContent.trim() : '';
                }
            """)
            
            if not name or name in seen_names:
                # Go back to results
                page.keyboard.press("Escape")
                time.sleep(1)
                continue
            
            seen_names.add(name)
            
            # Extract phone from detail text
            phones = extract_phone(detail_text)
            
            # Get address
            address = page.evaluate("""
                () => {
                    const addrBtn = document.querySelector('button[data-item-id="address"]');
                    if (addrBtn) return addrBtn.textContent.trim();
                    // Try alternative
                    const allText = document.body.innerText;
                    const lines = allText.split('\\n');
                    for (const line of lines) {
                        if (line.match(/\d{6}/) && line.length < 200) return line.trim();
                    }
                    return '';
                }
            """)
            
            # Get website
            website = page.evaluate("""
                () => {
                    const webBtn = document.querySelector('a[data-item-id="authority"]')
                                || document.querySelector('button[data-item-id="authority"]');
                    if (webBtn) return webBtn.href || webBtn.textContent.trim();
                    return '';
                }
            """)
            
            lead = {
                "niche": niche,
                "name": name,
                "phones": phones,
                "address": address[:200] if address else "",
                "website": website,
                "source": "google_maps_detail"
            }
            leads.append(lead)
            
            phone_str = ", ".join(phones) if phones else "no phone"
            print(f"  {i+1}. {name[:60]} | {phone_str}")
            
            # Close detail panel
            page.keyboard.press("Escape")
            time.sleep(1.5)
            
        except Exception as e:
            print(f"  Card {i+1} error: {e}")
            page.keyboard.press("Escape")
            time.sleep(1)
            continue
    
    return leads


def main():
    all_leads = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 900},
            locale="en-IN",
        )
        page = context.new_page()
        
        for niche, query in SEARCHES:
            try:
                leads = scrape_niche(niche, query, page)
                all_leads.extend(leads)
            except Exception as e:
                print(f"  Niche error: {e}")
            
            time.sleep(3)
        
        browser.close()
    
    # Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_leads, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n=== DONE ===")
    print(f"Total leads: {len(all_leads)}")
    print(f"With phones: {sum(1 for l in all_leads if l['phones'])}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
