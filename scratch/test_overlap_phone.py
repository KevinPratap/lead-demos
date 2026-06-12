import json
import re

serpapi_path = "/home/prata/leads/data/serpapi_leads.json"
wa_sent_path = "/home/prata/leads/data/wa_sent.json"

with open(serpapi_path, 'r') as f:
    serpapi_leads = json.load(f)

with open(wa_sent_path, 'r') as f:
    wa_sent = json.load(f)

def clean_phone(phone):
    if not phone:
        return ""
    # Remove all non-digits
    digits = re.sub(r'\D', '', str(phone))
    # If it starts with 91 and has 12 digits, or starts with 0 and has 11, let's normalize
    if len(digits) == 12 and digits.startswith('91'):
        return digits[2:]
    if len(digits) == 11 and digits.startswith('0'):
        return digits[1:]
    return digits

serpapi_phones = set()
for l in serpapi_leads:
    for p in l.get('phones', []):
        cp = clean_phone(p)
        if cp:
            serpapi_phones.add(cp)

wa_phones = set()
for l in wa_sent:
    cp = clean_phone(l.get('phone'))
    if cp:
        wa_phones.add(cp)

print(f"Number of clean SerpAPI phones: {len(serpapi_phones)}")
print(f"Number of clean WA sent phones: {len(wa_phones)}")
print(f"Overlap of phones between SerpAPI and WA sent: {len(serpapi_phones.intersection(wa_phones))}")

# Check names as well
serpapi_names = {l['name'].strip().lower() for l in serpapi_leads}
wa_names = {l['lead'].strip().lower() for l in wa_sent}
print(f"Number of SerpAPI names: {len(serpapi_names)}")
print(f"Number of WA sent names: {len(wa_names)}")
print(f"Overlap of names: {len(serpapi_names.intersection(wa_names))}")
