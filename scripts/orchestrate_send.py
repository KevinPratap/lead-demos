#!/usr/bin/env python3
import json
import os
import re
import subprocess
import time
import random
from datetime import datetime

# Paths
DATA_DIR = '/home/prata/leads/data'
LEADS_FILE = os.path.join(DATA_DIR, 'serpapi_leads.json')
SENT_FILE = os.path.join(DATA_DIR, 'wa_sent.json')
FINAL_SEND_FILE = os.path.join(DATA_DIR, 'wa_final_send.json')
RESULTS_FILE = os.path.join(DATA_DIR, 'wa_sent_results.json')
DEMOS_DIR = '/home/prata/leads/demos/'
SENDER_SCRIPT = '/home/prata/leads/scripts/send_whatsapp.js'

def clean_phone(phone):
    if not phone:
        return ""
    digits = re.sub(r'[^0-9]', '', phone)
    if digits.startswith('0'):
        digits = digits[1:]
    if digits.startswith('91') and len(digits) > 10:
        return digits
    elif len(digits) == 10:
        return '91' + digits
    return digits

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def clean_business_name(name):
    original_name = name
    name = name.replace('—', '-')
    
    for sep in ['|', '~', ':', ';']:
        if sep in name:
            name = name.split(sep)[0]
            
    if ' - ' in name:
        name = name.split(' - ')[0]
        
    if '-' in name and len(original_name) > 30:
        parts = name.split('-')
        if parts[0].strip().lower() not in ['physio', 'dent', 'o']:
            name = parts[0]
            
    if ',' in name and len(name) > 30:
        name = name.split(',')[0]
        
    return name.strip()

def main():
    print("🚀 Starting WhatsApp outreach orchestration...")
    
    # ── Load Data ──
    if not os.path.exists(LEADS_FILE):
        print(f"❌ Leads file not found at {LEADS_FILE}")
        return
        
    with open(LEADS_FILE, 'r') as f:
        serpapi_leads = json.load(f)
        
    wa_sent = []
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, 'r') as f:
            try:
                wa_sent = json.load(f)
            except Exception:
                wa_sent = []
                
    demos = os.listdir(DEMOS_DIR) if os.path.exists(DEMOS_DIR) else []
    demo_slugs = set(demos)
    
    # Create a set of already sent phone numbers (normalized)
    sent_phones = set()
    for s in wa_sent:
        p = clean_phone(s.get('phone', ''))
        if p:
            sent_phones.add(p)
            
    print(f"Loaded {len(serpapi_leads)} leads from SerpAPI.")
    print(f"Loaded {len(wa_sent)} sent logs. Found {len(sent_phones)} unique sent phones.")
    print(f"Found {len(demos)} generated demo sites.")
    
    # ── Step 1 & 2: Build send list and write wa_final_send.json ──
    niche_types = {
        'yoga': 'yoga studio',
        'physio': 'physio clinic',
        'spa': 'spa',
        'eyelash': 'lash studio',
        'salon': 'salon',
        'dental': 'dental clinic',
        'fitness': 'gym'
    }

    templates = [
        "hey, im kevin. i build websites. saw your [business type] on google and made a quick mockup. no pressure, check it out: [link]",
        "hey, quick question - does [business name] have a website? made a rough version for you, check it out: [link]",
        "hey, your [business type] looks solid on google. noticed you dont have a site. made a quick one for you, check it out: [link]",
        "hey kevin here. i make websites. saw your [business type] on google, made you a quick demo. have a look: [link]",
        "yo, im kevin. i build sites in mumbai. came across [business name] and whipped up a quick version, see what you think: [link]"
    ]
    
    final_send = []
    skipped_no_phone = 0
    skipped_already_sent = 0
    
    # We will iterate through all serpapi leads
    # Note: we need to rotate templates across the unsent ones to vary the structure
    unsent_count = 0
    
    for lead in serpapi_leads:
        phones = lead.get('phones', [])
        if not phones:
            skipped_no_phone += 1
            continue
            
        # Get first phone
        raw_phone = phones[0]
        phone = clean_phone(raw_phone)
        if not phone:
            skipped_no_phone += 1
            continue
            
        if phone in sent_phones:
            skipped_already_sent += 1
            continue
            
        name = lead.get('name', '')
        niche = lead.get('niche', '')
        
        # Match demo slug
        slug = slugify(name)
        matched_demo = ""
        if slug in demo_slugs:
            matched_demo = slug
        else:
            for d in demos:
                if re.sub(r'[^a-z0-9]', '', slug) == re.sub(r'[^a-z0-9]', '', d):
                    matched_demo = d
                    break
        
        demo_url = ""
        if matched_demo:
            demo_url = f"https://kevinpratap.github.io/lead-demos/{matched_demo}/"
            
        # Compose message
        temp_idx = unsent_count % 5
        template = templates[temp_idx]
        b_type = niche_types.get(niche, niche)
        clean_name = clean_business_name(name)
        
        if demo_url:
            msg = template
            msg = msg.replace("[business type]", b_type)
            msg = msg.replace("[business name]", clean_name)
            msg = msg.replace("[link]", demo_url)
        else:
            msg = f"hey, im kevin. i build websites for local businesses. saw your {b_type} on google and thought you could use one. if youre interested, i can build you a site. no pressure. here's my number."
            
        # Validation checks
        if "—" in msg:
            raise ValueError(f"Message contains em-dash: {msg}")
        if "!" in msg:
            raise ValueError(f"Message contains exclamation: {msg}")
        if len(msg) > 250:
            print(f"⚠️ Warning: Message exceeds 250 chars ({len(msg)} chars): {msg}")
            
        final_send.append({
            "phone": phone,
            "business_name": name,
            "niche": niche,
            "demo_url": demo_url,
            "message": msg
        })
        unsent_count += 1
        
    print(f"Skipped {skipped_no_phone} leads with no valid phone.")
    print(f"Skipped {skipped_already_sent} leads that were already sent.")
    print(f"Found {len(final_send)} leads to send to.")
    
    # Save wa_final_send.json
    with open(FINAL_SEND_FILE, 'w') as f:
        json.dump(final_send, f, indent=2)
    print(f"Saved {FINAL_SEND_FILE}")
    
    if len(final_send) == 0:
        print("No messages to send. Exiting.")
        return
        
    # ── Step 3: Send Messages ──
    results = []
    print("\n🚀 Starting to send messages via WhatsApp script...")
    
    for idx, entry in enumerate(final_send, 1):
        phone = entry["phone"]
        msg = entry["message"]
        biz_name = entry["business_name"]
        
        print(f"\n[{idx}/{len(final_send)}] Sending to {biz_name} (+{phone})...")
        
        # Execute send_whatsapp.js
        cmd = ["node", SENDER_SCRIPT, "--to", phone, "--msg", msg]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            stdout = res.stdout
            stderr = res.stderr
            
            # Determine success
            success = False
            error_msg = ""
            if "✅ Message sent!" in stdout:
                success = True
                print("   ✅ Sent successfully!")
            elif "❌ Failed to send:" in stdout or "❌ Failed to send:" in stderr:
                # Find error message
                match = re.search(r'❌ Failed to send:\s*(.*)', stdout + stderr)
                error_msg = match.group(1) if match else "Unknown error"
                print(f"   ❌ Failed: {error_msg}")
            else:
                # Check exit status or assume failed if no success message
                success = False
                error_msg = stderr.strip() or "No success indicator in output"
                print(f"   ❌ Failed: {error_msg}")
                
        except Exception as e:
            success = False
            error_msg = str(e)
            print(f"   ❌ Execution error: {error_msg}")
            
        results.append({
            "phone": phone,
            "business_name": biz_name,
            "success": success,
            "error": error_msg if not success else None,
            "sent_at": datetime.utcnow().isoformat() + "Z",
            "demo_url": entry["demo_url"],
            "message": msg
        })
        
        # Log to wa_sent_results.json
        with open(RESULTS_FILE, 'w') as f:
            json.dump(results, f, indent=2)
            
        # Wait 3-5 seconds between sends
        if idx < len(final_send):
            sleep_time = random.uniform(3, 5)
            print(f"   Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
            
    # ── Step 4: Update wa_sent.json ──
    print("\n🔄 Updating wa_sent.json...")
    
    # Reload wa_sent.json to get any other modifications
    current_wa_sent = []
    if os.path.exists(SENT_FILE):
        with open(SENT_FILE, 'r') as f:
            try:
                current_wa_sent = json.load(f)
            except Exception:
                current_wa_sent = []
                
    # Filter out the temporary logs created by send_whatsapp.js
    # send_whatsapp.js logs them with lead = phone (since we didn't pass --lead to it)
    phones_sent_this_run = {r["phone"] for r in results}
    cleaned_wa_sent = []
    for entry in current_wa_sent:
        p = clean_phone(entry.get('phone', ''))
        # If this phone was sent this run, and the lead field is identical to phone (temporary log), skip it
        if p in phones_sent_this_run and entry.get('lead') == entry.get('phone'):
            continue
        cleaned_wa_sent.append(entry)
        
    # Append the new records with requested format
    for r in results:
        # Step 4 requested: phone, business_name, message, sent_at (ISO timestamp), success (true/fail), demo_url
        new_entry = {
            "phone": r["phone"],
            "business_name": r["business_name"],
            "lead": r["business_name"], # keep compatibility
            "message": r["message"],
            "sent_at": r["sent_at"],
            "success": r["success"],
            "demo_url": r["demo_url"]
        }
        cleaned_wa_sent.append(new_entry)
        
    # Save back to wa_sent.json
    with open(SENT_FILE, 'w') as f:
        json.dump(cleaned_wa_sent, f, indent=2)
    print("✅ wa_sent.json updated successfully!")
    
    # ── Step 5: Print Summary ──
    attempted = len(results)
    successful = sum(1 for r in results if r["success"])
    failed = attempted - successful
    
    print("\n" + "="*40)
    print("📊 OUTREACH SUMMARY")
    print("="*40)
    print(f"Total Attempted:  {attempted}")
    print(f"Total Successful: {successful}")
    print(f"Total Failed:     {failed}")
    print("\nBusinesses Contacted:")
    for idx, r in enumerate(results, 1):
        status_char = "✅" if r["success"] else "❌"
        err_info = f" (Error: {r['error']})" if not r["success"] else ""
        print(f"{idx}. {r['business_name']} ({r['phone']}) — {status_char}{err_info}")
    print("="*40)

if __name__ == '__main__':
    main()
