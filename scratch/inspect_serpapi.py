import json

serpapi_path = "/home/prata/leads/data/serpapi_leads.json"
with open(serpapi_path, 'r') as f:
    serpapi_leads = json.load(f)

local_count = 0
organic_count = 0
has_phone = 0
for l in serpapi_leads:
    source = l.get('source')
    if source == 'local':
        local_count += 1
    elif source == 'organic':
        organic_count += 1
    
    if l.get('phones'):
        has_phone += 1

print(f"Total leads: {len(serpapi_leads)}")
print(f"Local leads: {local_count}")
print(f"Organic leads: {organic_count}")
print(f"Leads with phones: {has_phone}")
