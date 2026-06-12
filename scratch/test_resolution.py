import sqlite3
import json
import re

db_path = "/home/prata/leads/data/leads.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Load wa_sent.json
with open("/home/prata/leads/data/wa_sent.json", 'r') as f:
    wa_sent = json.load(f)

# Load database leads
cursor.execute("SELECT name, phone, address, rating, website, category FROM leads;")
db_rows = cursor.fetchall()
# Map database leads by clean name and clean phone
def clean_phone(phone):
    if not phone:
        return ""
    return re.sub(r'\D', '', str(phone))

def clean_name(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

db_by_name = {}
db_by_phone = {}
for name, phone, address, rating, website, category in db_rows:
    cname = clean_name(name) if name else ""
    cphone = clean_phone(phone) if phone else ""
    info = {
        "name": name,
        "phone": phone,
        "address": address,
        "rating": rating,
        "website": website,
        "category": category
    }
    if cname:
        db_by_name[cname] = info
    if cphone:
        db_by_phone[cphone] = info

# Parse pitch_sheet.md for details
pitch_sheet_path = "/home/prata/leads/data/exports/pitch_sheet.md"
with open(pitch_sheet_path, 'r') as f:
    pitch_content = f.read()

# We can parse the individual sections
full_scripts_part = pitch_content.split("## 📞 Full Pitch Scripts")[-1]
individual_sections = re.split(r'\n###\s+', full_scripts_part)
pitch_by_name = {}
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
    # E.g., **Phone:** 072080 84400 | **Rating:** 4.9⭐ (227 reviews)
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
            
    pitch_by_name[clean_name(biz_name)] = {
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
    
    cname = clean_name(name)
    cphone = clean_phone(phone)
    
    # Try to resolve details
    details = None
    if cphone in db_by_phone:
        details = db_by_phone[cphone]
        method = "db_phone"
    elif cname in db_by_name:
        details = db_by_name[cname]
        method = "db_name"
    elif cname in pitch_by_name:
        details = pitch_by_name[cname]
        method = "pitch_name"
    elif cphone in db_by_phone: # try with partial phone?
        pass
        
    if details:
        resolved_count += 1
    else:
        not_resolved.append((name, phone))

print(f"Resolved WA sent leads: {resolved_count} / {len(wa_sent)}")
print("\nUnresolved WA sent leads:")
for name, phone in not_resolved[:15]:
    print(f"- {name} | {phone}")

conn.close()
