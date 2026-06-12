import json
import os

serpapi_path = "/home/prata/leads/data/serpapi_leads.json"
wa_sent_path = "/home/prata/leads/data/wa_sent.json"
pitch_sheet_path = "/home/prata/leads/data/exports/pitch_sheet.md"
demos_dir = "/home/prata/leads/demos/"

with open(serpapi_path, 'r') as f:
    serpapi_leads = json.load(f)

with open(wa_sent_path, 'r') as f:
    wa_sent = json.load(f)

print(f"SerpAPI leads count: {len(serpapi_leads)}")
print(f"WA sent leads count: {len(wa_sent)}")

# Count unique phones in wa_sent
wa_phones = [item.get('phone') for item in wa_sent if item.get('phone')]
print(f"Unique phones in WA sent: {len(set(wa_phones))} out of {len(wa_phones)}")

# Let's see some samples of SerpAPI leads
print("\nSerpAPI leads sample:")
for i, item in enumerate(serpapi_leads[:5]):
    print(f"{i+1}: {item.get('name')} | {item.get('phones')} | {item.get('source')} | {item.get('niche')}")

# Let's see some samples of WA sent
print("\nWA sent sample:")
for i, item in enumerate(wa_sent[:5]):
    print(f"{i+1}: {item.get('lead')} | {item.get('phone')} | {item.get('sent_at')} | {item.get('success')}")

# Demos list
demo_folders = os.listdir(demos_dir)
print(f"\nDemo folders count: {len(demo_folders)}")
