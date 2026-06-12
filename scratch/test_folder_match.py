import json
import os
import re

serpapi_path = "/home/prata/leads/data/serpapi_leads.json"
wa_sent_path = "/home/prata/leads/data/wa_sent.json"
demos_dir = "/home/prata/leads/demos/"

with open(serpapi_path, 'r') as f:
    serpapi_leads = json.load(f)

with open(wa_sent_path, 'r') as f:
    wa_sent = json.load(f)

demo_folders = os.listdir(demos_dir)

# Helper function to get clean text for matching
def clean_name(name):
    # keep only a-z and 0-9
    return re.sub(r'[^a-z0-9]', '', name.lower())

folder_map = {clean_name(folder): folder for folder in demo_folders}

print("Matching serpapi leads:")
serpapi_matched = 0
for idx, lead in enumerate(serpapi_leads):
    name = lead['name']
    cname = clean_name(name)
    if cname in folder_map:
        serpapi_matched += 1
        # print(f"  SerpAPI Match: {name} -> {folder_map[cname]}")

print(f"Total SerpAPI matched: {serpapi_matched} / {len(serpapi_leads)}")

print("\nMatching WA sent leads:")
wa_matched = 0
for idx, lead in enumerate(wa_sent):
    name = lead['lead']
    cname = clean_name(name)
    if cname in folder_map:
        wa_matched += 1
        # print(f"  WA Match: {name} -> {folder_map[cname]}")

print(f"Total WA sent matched: {wa_matched} / {len(wa_sent)}")
