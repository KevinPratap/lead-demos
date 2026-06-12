import json
import re

with open("/home/prata/leads/data/wa_sent.json", 'r') as f:
    wa_sent = json.load(f)

extracted_count = 0
not_extracted = []
for idx, l in enumerate(wa_sent):
    msg = l.get('message', '')
    # Search for the pattern
    match = re.search(r'kevinpratap\.github\.io/lead-demos/([a-z0-9\-]+)/?', msg)
    if match:
        folder = match.group(1)
        extracted_count += 1
        # print(f"{idx+1}: Extracted {folder}")
    else:
        not_extracted.append((l.get('lead'), msg))

print(f"\nExtracted folder from message: {extracted_count} / {len(wa_sent)}")
print(f"Not extracted: {len(not_extracted)}")
for lead, msg in not_extracted:
    print(f"- Lead: {lead} | Msg snippet: {msg[:100]}")
