#!/usr/bin/env python3
"""Mega blast — send WhatsApp demos to 100 unsent leads. Python, no bash pipe issues."""
import sqlite3, json, os, re, subprocess, time, sys

DB = "/home/prata/leads/data/leads.db"
DEMOS = "/home/prata/leads/demos"
SENT_LOG = "/home/prata/leads/data/wa_sent.json"
SEND_SCRIPT = "/home/prata/leads/scripts/send_whatsapp.js"
MAX = 100
DELAY = 35

# Load sent phones
sent_phones = set()
if os.path.exists(SENT_LOG):
    with open(SENT_LOG) as f:
        for e in json.load(f):
            if e.get("success"):
                sent_phones.add(e.get("phone", ""))

# Get unsent leads with demos
db = sqlite3.connect(DB)
db.row_factory = sqlite3.Row
rows = db.execute("""
    SELECT name, phone, rating, reviews, category
    FROM leads 
    WHERE (website IS NULL OR website = '') 
    AND phone IS NOT NULL AND phone != ''
    ORDER BY reviews DESC
""").fetchall()
db.close()

def slug(name):
    s = re.sub(r'[^a-z0-9\s-]', '', name.lower()).strip()
    return re.sub(r'\s+', '-', s)

def make_pitch(name, category, rating, reviews, url):
    cat = (category or "").lower()
    stars = f"{rating:.1f}" if rating else "4.5"
    rev = str(reviews or 0)
    
    if any(w in cat for w in ["dental", "dentist"]):
        return (f"hi, kevin here — web dev student at NMIMS. noticed {name} on Google Maps "
                f"({stars}★, {rev} reviews) but no website. built a quick preview: {url} — "
                f"30 sec to check. if you like it, i can finish it properly with your real photos, "
                f"services, and domain. no pressure at all")
    elif any(w in cat for w in ["salon", "beauty", "hair", "barber", "spa"]):
        return (f"hi, kevin here — NMIMS web dev student. found {name} on Google ({stars}★) "
                f"and noticed no website. built you a quick preview: {url} — 30 seconds. "
                f"if you like the look, i can build the full thing with your actual photos, "
                f"pricing menu, and online booking. totally free to look")
    elif any(w in cat for w in ["cafe", "restaurant", "food", "coffee", "bake"]):
        return (f"hi, kevin here — NMIMS student and web developer. came across {name} on Google "
                f"({stars}★, {rev} reviews). noticed no website. made a quick preview: {url} — "
                f"30 sec look. if interested, can build full site with menu, photos, location. no commitment")
    else:
        return (f"hi, kevin here — web dev student at NMIMS Mumbai. found {name} on Google Maps "
                f"({stars}★) and noticed no website. built a quick preview: {url} — 30 sec to look. "
                f"if you want a proper site, i can make one with your actual photos and details. no pressure")

def clean_phone(raw):
    """Convert any Indian phone format to 91XXXXXXXXXX for WhatsApp."""
    digits = re.sub(r'[^0-9]', '', raw or '')
    if not digits:
        return ''
    if digits.startswith('0'):
        digits = digits[1:]
    if len(digits) == 10 and not digits.startswith('91'):
        digits = '91' + digits
    return digits

count = 0
for r in rows:
    phone = clean_phone(r['phone'])
    if not phone or phone in sent_phones:
        continue
    
    s = slug(r['name'])
    demo_path = f"{DEMOS}/{s}/index.html"
    if not os.path.exists(demo_path):
        continue
    
    if count >= MAX:
        break
    
    url = f"https://kevinpratap.github.io/lead-demos/{s}/"
    msg = make_pitch(r['name'], r['category'], r['rating'], r['reviews'], url)
    
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] #{count+1}/{MAX} → {r['name'][:50]}")
    print(f"       ⭐{r['rating'] or '?'} ({r['reviews'] or 0} reviews) | {r['category']}")
    print(f"       📱 {phone}")
    
    result = subprocess.run(
        ["node", SEND_SCRIPT, "--to", phone, "--msg", msg],
        capture_output=True, text=True, timeout=60, cwd="/home/prata/leads"
    )
    print(f"       {'✓' if result.returncode == 0 else '✗'} {result.stdout.strip()[-80:]}")
    
    count += 1
    sent_phones.add(phone)
    
    if count < MAX:
        print(f"       ⏳ waiting {DELAY}s...")
        time.sleep(DELAY)

print(f"\n=== DONE === Sent: {count} messages | Time: {time.strftime('%H:%M:%S')}")
