# Task: Send WhatsApp Messages to New Leads with Demo Links

## Goal
Send WhatsApp messages to the 20 new leads. Demo sites have been generated. Now we need to match phones and send.

## Data Sources
1. `/home/prata/leads/data/serpapi_leads.json` — has phone numbers and business names
2. `/home/prata/leads/data/wa_sent.json` — already sent (skip these)
3. `/home/prata/leads/demos/` — 20 new demo sites just generated
4. `/home/prata/leads/scripts/send_whatsapp.js` — WhatsApp sender

## Steps

### Step 1: Build the send list
Read serpapi_leads.json. For each lead with a phone number that is NOT in wa_sent.json:
- Get the phone number
- Get the business name
- Determine the niche
- Check if a demo exists in /home/prata/leads/demos/ (match by business name, case-insensitive, fuzzy)
- If demo exists, use URL: `https://kevinpratap.github.io/lead-demos/<slug>/`
- If no demo, use empty string

### Step 2: Write messages to send
Create `/home/prata/leads/data/wa_final_send.json` with array of:
{
  "phone": "phone number with country code (91...)",
  "business_name": "name",
  "niche": "niche",
  "demo_url": "url or empty",
  "message": "message text"
}

Message rules:
- NO em dashes (—)
- NO exclamation marks (!)
- NO corporate speak ("no commitment", "what's possible", "great reviews")
- Casual, lowercase, Indian English
- Vary the structure — use 5 different message templates
- Reference the business name naturally
- Keep under 250 characters
- Sound like a real 20 year old student

Message templates (rotate through these):
1. "hey, im kevin. i build websites for local businesses. saw your [business type] on google and put together a quick mockup. no pressure, just thought you might want to see it: [link]"
2. "hey, quick question — does [business name] have a website? i found you on google maps and thought you could use one. i made a rough version, take a look: [link]"
3. "hey, your [business type] looks solid on google. noticed you dont have a site though. i threw together a quick one for you, check it out: [link]"
4. "hey kevin here. i make websites. saw your [business type] on google, made you a quick demo. have a look: [link]"
5. "yo, im kevin. i build sites for local spots in mumbai. came across [business name] and whipped up a quick version. see what you think: [link]"

If no demo URL: "hey, im kevin. i build websites for local businesses. saw your [business type] on google and thought you could use one. if youre interested, i can build you a site. no pressure. here's my number."

### Step 3: Send messages
For each entry in wa_final_send.json:
- Run: `node /home/prata/leads/scripts/send_whatsapp.js --to <phone> --msg "<message>"`
- Wait 3-5 seconds between sends
- Log result (success/fail) to `/home/prata/leads/data/wa_sent_results.json`
- If a send fails, skip and continue to next

### Step 4: Update wa_sent.json
After all sends, append the new sends to wa_sent.json with:
- phone, business_name, message, sent_at (ISO timestamp), success (true/fail), demo_url

### Step 5: Print summary
- Total attempted
- Total successful
- Total failed
- List of businesses contacted
