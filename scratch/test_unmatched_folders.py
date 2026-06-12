import json
import os
import re

serpapi_path = "/home/prata/leads/data/serpapi_leads.json"
wa_sent_path = "/home/prata/leads/data/wa_sent.json"
demos_dir = "/home/prata/leads/demos/"

with open(wa_sent_path, 'r') as f:
    wa_sent = json.load(f)

demo_folders = os.listdir(demos_dir)

# Helper function to get clean text for matching
def clean_name(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

folder_map = {clean_name(folder): folder for folder in demo_folders}

print("Unmatched WA sent leads:")
unmatched = 0
for idx, lead in enumerate(wa_sent):
    name = lead['lead']
    cname = clean_name(name)
    if cname not in folder_map:
        unmatched += 1
        # Let's print the name and search if there's a close folder name
        # E.g. let's find any folder name that contains a substantial part of the name
        matches = [f for f in demo_folders if clean_name(name)[:10] in clean_name(f) or clean_name(f)[:10] in clean_name(name)]
        print(f"{unmatched}: {name} | Phone: {lead.get('phone')} | Close Folders: {matches}")
