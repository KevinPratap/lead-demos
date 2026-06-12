import sqlite3
import json
import re

db_path = "/home/prata/leads/data/leads.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Load wa_sent.json
with open("/home/prata/leads/data/wa_sent.json", 'r') as f:
    wa_sent = json.load(f)

cursor.execute("SELECT name, phone, address, rating, website, category, reviews FROM leads;")
db_rows = cursor.fetchall()

def last_10_digits(phone):
    if not phone:
        return ""
    digits = re.sub(r'\D', '', str(phone))
    return digits[-10:] if len(digits) >= 10 else digits

db_by_phone10 = {}
for name, phone, address, rating, website, category, reviews in db_rows:
    p10 = last_10_digits(phone)
    if p10:
        db_by_phone10[p10] = {
            "name": name,
            "phone": phone,
            "address": address,
            "rating": rating,
            "website": website,
            "category": category,
            "reviews": reviews
        }

# Parse pitch_sheet.md for details
pitch_sheet_path = "/home/prata/leads/data/exports/pitch_sheet.md"
with open(pitch_sheet_path, 'r') as f:
    pitch_content = f.read()

# We can parse the individual sections
full_scripts_part = pitch_content.split("## 📞 Full Pitch Scripts")[-1]
individual_sections = re.split(r'\n###\s+', full_scripts_part)
pitch_by_phone10 = {}
for sec in individual_sections[1:]:
    lines = sec.strip().split('\n')
    if not lines:
        continue
    header = lines[0]
    match = re.match(r'^\d+\.\s+(.+)$', header)
    if not match:
        continue
    biz_name = match.group(1).strip()
    
    # Extract phone, rating, address, maps
    phone_rating_line = ""
    address_line = ""
    for line in lines[1:]:
        if "**Phone:**" in line:
            phone_rating_line = line
        elif "**Address:**" in line:
            address_line = line
            
    phone = ""
    rating = None
    if phone_rating_line:
        p_match = re.search(r'\*\*Phone:\*\*\s*(.*?)\s*\|', phone_rating_line)
        if p_match:
            phone = p_match.group(1).strip()
        r_match = re.search(r'\*\*Rating:\*\*\s*([\d\.]+)⭐', phone_rating_line)
        if r_match:
            rating = float(r_match.group(1))
            
    address = ""
    if address_line:
        a_match = re.search(r'\*\*Address:\*\*\s*(.*)$', address_line)
        if a_match:
            address = a_match.group(1).strip()
            
    p10 = last_10_digits(phone)
    if p10:
        pitch_by_phone10[p10] = {
            "name": biz_name,
            "phone": phone,
            "rating": rating,
            "address": address
        }

resolved_count = 0
not_resolved = []
for idx, l in enumerate(wa_sent):
    name = l.get('lead')
    phone = l.get('phone')
    
    p10 = last_10_digits(phone)
    
    details = None
    if p10 in db_by_phone10:
        details = db_by_phone10[p10]
    elif p10 in pitch_by_phone10:
        details = pitch_by_phone10[p10]
        
    if details:
        resolved_count += 1
    else:
        not_resolved.append((name, phone))

print(f"Resolved WA sent leads (by last 10 digits): {resolved_count} / {len(wa_sent)}")
print("\nUnresolved WA sent leads:")
for name, phone in not_resolved:
    print(f"- {name} | {phone}")

conn.close()
