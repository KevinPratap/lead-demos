import json

with open("/home/prata/leads/data/serpapi_leads.json", 'r') as f:
    leads = json.load(f)

keys = set()
for l in leads:
    keys.update(l.keys())

print(f"All keys in serpapi_leads.json: {list(keys)}")

# Print a few that are of source 'local'
locals = [l for l in leads if l.get('source') == 'local']
print("\nSample local lead keys and values:")
for l in locals[:3]:
    print(l)
