#!/bin/bash
# Morning WhatsApp blast — send to all unsent leads with demos
# Run at 9:30 AM IST for best reply rates
cd /home/prata/leads

COUNT=0
SKIP=0
MAX=100  # Safe daily limit — spread over ~1hr with 35s delay

# Get all leads with demos that haven't been sent yet
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
except:
    pass

# Find unsent leads with demos
rows = db.execute(\"\"\"
    SELECT name, phone, rating, reviews 
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
        print(f'NEXT|||{name}|||{phone_clean}|||https://kevinpratap.github.io/lead-demos/{s}/')
db.close()
" | while IFS='|||' read -r _ name phone url; do
    if [ $COUNT -ge $MAX ]; then
        echo "Reached max $MAX sends for today"
        break
    fi
    
    echo "[$(date +%H:%M)] Sending to: $name ($phone)"
    node scripts/send_whatsapp.js --lead "$name" --url "$url" 2>&1 | tail -1
    
    COUNT=$((COUNT + 1))
    echo "  Sent: $COUNT | Remaining delay: 35s"
    sleep 35
done

echo "Morning blast complete. Sent: $COUNT"
