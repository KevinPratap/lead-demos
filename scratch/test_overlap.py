import json
import os
import re

serpapi_path = "/home/prata/leads/data/serpapi_leads.json"
wa_sent_path = "/home/prata/leads/data/wa_sent.json"
pitch_sheet_path = "/home/prata/leads/data/exports/pitch_sheet.md"

with open(serpapi_path, 'r') as f:
    serpapi_leads = json.load(f)

with open(wa_sent_path, 'r') as f:
    wa_sent = json.load(f)

# Parse pitch_sheet.md for businesses and their scripts
with open(pitch_sheet_path, 'r') as f:
    pitch_content = f.read()

# Let's find sections starting with ### <num>. <name>
# and extract their WhatsApp and Call Script content
# We will split by "---" or by the next "###"
sections = re.split(r'\n---\n', pitch_content)
print(f"Number of sections split by '---': {len(sections)}")

parsed_pitch_leads = {}
# The business pitch scripts start after "## 📞 Full Pitch Scripts"
# Let's find it.
full_scripts_part = pitch_content.split("## 📞 Full Pitch Scripts")[-1]
individual_sections = re.split(r'\n###\s+', full_scripts_part)
print(f"Number of individual sections in Full Pitch Scripts: {len(individual_sections)}")

for sec in individual_sections[1:]:
    lines = sec.strip().split('\n')
    header = lines[0] # e.g. "1. Dental Clinic" or "10. Advance Fitness"
    match = re.match(r'^\d+\.\s+(.+)$', header)
    if not match:
        continue
    biz_name = match.group(1).strip()
    
    # Let's extract WhatsApp message
    wa_msg = ""
    call_script = ""
    
    # We can search for #### 💬 WhatsApp (copy-paste) and #### 📞 Call Script
    parts_wa = sec.split("#### 💬 WhatsApp (copy-paste)")
    if len(parts_wa) > 1:
        wa_part = parts_wa[1].split("####")[0].strip()
        wa_msg = wa_part
    
    parts_call = sec.split("#### 📞 Call Script")
    if len(parts_call) > 1:
        call_part = parts_call[1].split("####")[0].strip()
        call_script = call_part
        
    parsed_pitch_leads[biz_name] = {
        "whatsapp": wa_msg,
        "call": call_script
    }

print(f"Successfully parsed {len(parsed_pitch_leads)} business scripts from pitch_sheet.md")

# Check matches between serpapi_leads and parsed_pitch_leads
serp_names = [l['name'] for l in serpapi_leads]
wa_names = [l['lead'] for l in wa_sent]

print("\nOverlap check:")
print(f"SerpAPI leads matched with pitch_sheet.md: {len([n for n in serp_names if n in parsed_pitch_leads])} / {len(serp_names)}")
print(f"WA sent leads matched with pitch_sheet.md: {len([n for n in wa_names if n in parsed_pitch_leads])} / {len(wa_names)}")

# Let's check normalized name matching
def normalize(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

norm_pitch_leads = {normalize(k): (k, v) for k, v in parsed_pitch_leads.items()}
serp_norm_matches = []
for l in serpapi_leads:
    nl = normalize(l['name'])
    if nl in norm_pitch_leads:
        serp_norm_matches.append(l['name'])

wa_norm_matches = []
for l in wa_sent:
    nl = normalize(l['lead'])
    if nl in norm_pitch_leads:
        wa_norm_matches.append(l['lead'])

print(f"Normalized SerpAPI leads matched with pitch_sheet.md: {len(serp_norm_matches)} / {len(serp_names)}")
print(f"Normalized WA sent leads matched with pitch_sheet.md: {len(wa_norm_matches)} / {len(wa_names)}")
print(f"Unique SerpAPI names: {len(set(serp_names))}")
print(f"Unique WA sent names: {len(set(wa_names))}")
