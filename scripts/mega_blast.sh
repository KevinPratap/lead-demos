#!/bin/bash
# ONE-TIME MEGA BLAST — Send to ALL unsent leads with demos
# Run once to hit 100+ sends, then let the daily cron take over
cd /home/prata/leads

COUNT=0
MAX=100

echo "=== MEGA BLAST — $(date) ==="

# Get ALL leads with demos that haven't been sent, sort by rating
python3 -c "
import json, os, sqlite3, re
db = sqlite3.connect('data/leads.db')
db.row_factory = sqlite3.Row

# Load sent phones
sent_phones = set()
try:
    with open('data/wa_sent.json') as f:
        for e in json.load(f):
            if e.get('success'):
                sent_phones.add(e.get('phone', ''))
except: pass

# Find all leads with demos
rows = db.execute(\"\"\"
    SELECT name, phone, rating, reviews, category
    FROM leads 
    WHERE (website IS NULL OR website = '') 
    AND phone IS NOT NULL AND phone != ''
    ORDER BY reviews DESC
\"\"\").fetchall()

def slug(name):
    s = re.sub(r'[^a-z0-9\s-]', '', name.lower()).strip()
    return re.sub(r'\s+', '-', s)

for r in rows:
    phone_clean = re.sub(r'[^0-9]', '', r['phone'] or '')
    if phone_clean in sent_phones:
        continue
    s = slug(r['name'])
    demo = f'demos/{s}/index.html'
    if os.path.exists(demo):
        name = r['name'].replace(\"'\", \"'\\\\''\")
        cat = r['category'] or 'business'
        rating = r['rating'] or 0
        reviews = r['reviews'] or 0
        print(f'NEXT|||{name}|||{phone_clean}|||https://kevinpratap.github.io/lead-demos/{s}/|||{cat}|||{rating}|||{reviews}')
db.close()
" | while IFS='|||' read -r _ name phone url category rating reviews; do
    if [ $COUNT -ge $MAX ]; then
        echo "Reached max $MAX sends"
        break
    fi
    
    # CUSTOM WEB-DEV PITCH per category
    if [[ "$category" == *"dental"* ]] || [[ "$category" == *"Dentist"* ]]; then
        MSG="hi, kevin here — web dev student at NMIMS. i noticed $name on Google Maps (${rating}★, ${reviews} reviews) but no website. built a quick preview using your actual profile details: $url — takes 30 sec to check. if you like it, i can finish it properly with your real photos, services, and domain. no pressure at all"
    elif [[ "$category" == *"salon"* ]] || [[ "$category" == *"beauty"* ]] || [[ "$category" == *"hair"* ]]; then
        MSG="hi, kevin here — NMIMS web dev student. found $name on Google (${rating}★) and noticed no website. built you a quick preview: $url — 30 seconds. if you like the look, i can build the full thing with your actual photos, pricing menu, and booking. totally free to look"
    elif [[ "$category" == *"cafe"* ]] || [[ "$category" == *"restaurant"* ]] || [[ "$category" == *"food"* ]]; then
        MSG="hi, kevin here — NMIMS student and web developer. came across $name on Google — ${rating}★, great reviews. noticed no website though. made a quick preview: $url — 30 sec look. if interested, i can build a full site with your menu, photos, location, and online ordering link. no commitment"
    else
        MSG="hi, kevin here — web dev student at NMIMS Mumbai. found $name on Google Maps (${rating}★) and noticed no website. built a quick preview using your profile: $url — 30 sec to look. if you want a proper site, i can make one with your actual photos and details. just checking, no pressure"
    fi
    
    echo "[$(date +%H:%M)] Sending to: $name ($phone)"
    echo "  Category: $category | ⭐$rating ($reviews reviews)"
    
    node scripts/send_whatsapp.js --to "$phone" --msg "$MSG" 2>&1 | tail -1
    
    COUNT=$((COUNT + 1))
    echo "  Sent: $COUNT/$MAX | Waiting 35s..."
    sleep 35
done

echo ""
echo "=== MEGA BLAST COMPLETE ==="
echo "Sent: $COUNT messages"
echo "Time: $(date)"
