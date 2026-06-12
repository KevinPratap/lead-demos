import sqlite3
import json

db_path = "/home/prata/leads/data/leads.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT * FROM leads LIMIT 5;")
rows = cursor.fetchall()

# Let's get column names
cursor.execute("PRAGMA table_info(leads);")
cols = [col[1] for col in cursor.fetchall()]

print("Sample rows from 'leads' table:")
for row in rows:
    row_dict = dict(zip(cols, row))
    print(f"Name: {row_dict['name']} | Category: {row_dict['category']} | Phone: {row_dict['phone']} | Rating: {row_dict['rating']}")

# Let's see if we can match serpapi_leads and wa_sent to leads in database
# We'll load the JSON files first
with open("/home/prata/leads/data/serpapi_leads.json", 'r') as f:
    serpapi_leads = json.load(f)

with open("/home/prata/leads/data/wa_sent.json", 'r') as f:
    wa_sent = json.load(f)

# Count matches by name or phone in db
cursor.execute("SELECT name, phone FROM leads;")
db_leads = cursor.fetchall()
db_names_set = {n.lower().strip() for n, p in db_leads if n}
db_phones_set = {p.replace(" ", "").replace("-", "").replace("+", "") for n, p in db_leads if p}

serpapi_matched_name = 0
serpapi_matched_phone = 0
for l in serpapi_leads:
    name = l.get('name', '').lower().strip()
    if name in db_names_set:
        serpapi_matched_name += 1
    # Check phone
    for p in l.get('phones', []):
        cp = p.replace(" ", "").replace("-", "").replace("+", "")
        if cp in db_phones_set:
            serpapi_matched_phone += 1
            break

wa_matched_name = 0
wa_matched_phone = 0
for l in wa_sent:
    name = l.get('lead', '').lower().strip()
    if name in db_names_set:
        wa_matched_name += 1
    phone = l.get('phone', '')
    cp = phone.replace(" ", "").replace("-", "").replace("+", "")
    if cp in db_phones_set:
        wa_matched_phone += 1

print(f"\nSerpAPI matches in DB by name: {serpapi_matched_name} / {len(serpapi_leads)}")
print(f"SerpAPI matches in DB by phone: {serpapi_matched_phone} / {len(serpapi_leads)}")
print(f"WA sent matches in DB by name: {wa_matched_name} / {len(wa_sent)}")
print(f"WA sent matches in DB by phone: {wa_matched_phone} / {len(wa_sent)}")

conn.close()
