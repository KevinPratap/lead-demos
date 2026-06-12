import json

try:
    with open("/home/prata/leads/data/playwright_leads.json", 'r') as f:
        playwright_leads = json.load(f)
    print(f"Playwright leads count: {len(playwright_leads)}")
    if playwright_leads:
        print("Keys:", list(playwright_leads[0].keys()))
        print("Sample:", playwright_leads[0])
except Exception as e:
    print("Error:", e)
