import json
import os
import sqlite3
import re

db_path = "/home/prata/leads/data/leads.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Load wa_sent.json
with open("/home/prata/leads/data/wa_sent.json", 'r') as f:
    wa_sent = json.load(f)

# Load database leads
cursor.execute("SELECT name, phone FROM leads;")
db_rows = cursor.fetchall()

def last_10_digits(phone):
    if not phone:
        return ""
    digits = re.sub(r'\D', '', str(phone))
    return digits[-10:] if len(digits) >= 10 else digits

db_by_phone10 = {}
for name, phone in db_rows:
    p10 = last_10_digits(phone)
    if p10:
        db_by_phone10[p10] = name

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
    
    # Extract phone
    phone_rating_line = ""
    for line in lines[1:]:
        if "**Phone:**" in line:
            phone_rating_line = line
            break
            
    phone = ""
    if phone_rating_line:
        p_match = re.search(r'\*\*Phone:\*\*\s*(.*?)\s*\|', phone_rating_line)
        if p_match:
            phone = p_match.group(1).strip()
            
    p10 = last_10_digits(phone)
    if p10:
        pitch_by_phone10[p10] = biz_name

demos_dir = "/home/prata/leads/demos/"
demo_folders = os.listdir(demos_dir)

def clean_name(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

folder_map = {clean_name(folder): folder for folder in demo_folders}

matched_count = 0
unmatched_leads = []

for idx, l in enumerate(wa_sent):
    name = l.get('lead')
    phone = l.get('phone')
    p10 = last_10_digits(phone)
    
    # Resolve actual name
    db_name = ""
    if p10 in db_by_phone10:
        db_name = db_by_phone10[p10]
    elif p10 in pitch_by_phone10:
        db_name = pitch_by_phone10[p10]
        
    actual_name = db_name if db_name else name
    cname = clean_name(actual_name)
    
    if cname in folder_map:
        matched_count += 1
    else:
        # Check if we can find a folder that contains the cleaned name, or vice versa
        closest = []
        for fk, fv in folder_map.items():
            if cname and (cname in fk or fk in cname):
                closest.append(fv)
        unmatched_leads.append((actual_name, phone, closest))

print(f"Total matched folders after name resolution: {matched_count} / {len(wa_sent)}")
print(f"Total unmatched: {len(unmatched_leads)}")
for name, phone, closest in unmatched_leads[:15]:
    print(f"- {name} | Phone: {phone} | Closest folders: {closest}")

conn.close()
