import sqlite3
import json
import re

db_path = "/home/prata/leads/data/leads.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Load serpapi_leads.json
with open("/home/prata/leads/data/serpapi_leads.json", 'r') as f:
    serpapi_leads = json.load(f)

cursor.execute("SELECT name, phone, rating, reviews FROM leads;")
db_rows = cursor.fetchall()

def last_10_digits(phone):
    if not phone:
        return ""
    digits = re.sub(r'\D', '', str(phone))
    return digits[-10:] if len(digits) >= 10 else digits

def clean_name(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

db_by_name = {}
db_by_phone10 = {}
for name, phone, rating, reviews in db_rows:
    cname = clean_name(name)
    if cname:
        db_by_name[cname] = {"rating": rating, "reviews": reviews}
    p10 = last_10_digits(phone)
    if p10:
        db_by_phone10[p10] = {"rating": rating, "reviews": reviews}

matched_db = 0
has_phone = 0
for l in serpapi_leads:
    name = l.get('name')
    phones = l.get('phones', [])
    
    # Try match by phone
    matched = False
    for p in phones:
        p10 = last_10_digits(p)
        if p10 in db_by_phone10:
            matched = True
            matched_db += 1
            break
            
    if not matched:
        cname = clean_name(name)
        if cname in db_by_name:
            matched_db += 1
            matched = True

print(f"SerpAPI leads matched in DB: {matched_db} / {len(serpapi_leads)}")
conn.close()
