import json
from collections import defaultdict
import re

with open("/home/prata/leads/data/wa_sent.json", 'r') as f:
    wa_sent = json.load(f)

def last_10_digits(phone):
    if not phone:
        return ""
    digits = re.sub(r'\D', '', str(phone))
    return digits[-10:] if len(digits) >= 10 else digits

by_phone = defaultdict(list)
for l in wa_sent:
    p10 = last_10_digits(l.get('phone'))
    by_phone[p10].append(l)

print(f"Total entries in wa_sent.json: {len(wa_sent)}")
print(f"Unique phone numbers in wa_sent.json: {len(by_phone)}")

duplicates = {k: v for k, v in by_phone.items() if len(v) > 1}
print(f"Number of phone numbers with multiple messages: {len(duplicates)}")

print("\nSample duplicates:")
for p10, list_leads in list(duplicates.items())[:3]:
    print(f"\nPhone: {p10}")
    for idx, l in enumerate(list_leads):
        print(f"  {idx+1}: Date: {l.get('sent_at')} | Success: {l.get('success')} | Lead: {l.get('lead')} | Msg: {l.get('message')[:60]}")
