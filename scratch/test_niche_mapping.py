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
cursor.execute("SELECT name, phone, category FROM leads;")
db_rows = cursor.fetchall()

def last_10_digits(phone):
    if not phone:
        return ""
    digits = re.sub(r'\D', '', str(phone))
    return digits[-10:] if len(digits) >= 10 else digits

db_by_phone10 = {}
for name, phone, category in db_rows:
    p10 = last_10_digits(phone)
    if p10:
        db_by_phone10[p10] = {
            "name": name,
            "category": category
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
        pitch_by_phone10[p10] = {
            "name": biz_name
        }

def get_niche_from_category(category, name):
    if not category:
        category = ""
    cat = category.lower()
    nm = name.lower()
    
    if "dent" in cat or "prosthodontist" in cat or "dent" in nm:
        return "dental"
    if "eyelash" in cat or "eyelash" in nm:
        return "eyelash"
    if "salon" in cat or "hair" in cat or "beauty" in cat or "makeup" in cat or "salon" in nm or "beauty" in nm:
        return "salon"
    if "barber" in cat or "barber" in nm:
        return "barber"
    if "cafe" in cat or "coffee" in cat or "cafe" in nm or "coffee" in nm:
        return "cafe"
    if "gym" in cat or "fitness" in cat or "gym" in nm or "fitness" in nm:
        return "gym"
    if "yoga" in cat or "pilates" in cat or "yoga" in nm or "pilates" in nm:
        return "yoga"
    if "skin" in cat or "dermat" in cat or "skin" in nm:
        return "skin"
    if "spa" in cat or "massage" in cat or "sauna" in cat or "spa" in nm:
        return "spa"
    if "physio" in cat or "therapy" in cat or "rehab" in cat or "physio" in nm:
        return "physio"
    if "bakery" in cat or "bake" in cat or "bakery" in nm or "bake" in nm:
        return "bakery"
        
    return "other"

print("Mapping wa_sent leads to niches:")
unmapped = 0
for idx, l in enumerate(wa_sent):
    name = l.get('lead')
    phone = l.get('phone')
    p10 = last_10_digits(phone)
    
    db_name = ""
    category = ""
    if p10 in db_by_phone10:
        db_name = db_by_phone10[p10]['name']
        category = db_by_phone10[p10]['category']
    elif p10 in pitch_by_phone10:
        db_name = pitch_by_phone10[p10]['name']
        
    actual_name = db_name if db_name else name
    niche = get_niche_from_category(category, actual_name)
    if niche == "other":
        unmapped += 1
        print(f"UNMAPPED: Name: {actual_name} | Category: {category} | Phone: {phone}")
    # else:
    #     print(f"MAPPED: Name: {actual_name} | Category: {category} -> Niche: {niche}")

print(f"Total unmapped: {unmapped} / {len(wa_sent)}")

conn.close()
