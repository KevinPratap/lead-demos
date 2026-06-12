# Task: Send WhatsApp Messages to New Leads

## Goal
Send WhatsApp messages to all new leads from the SerpAPI scrape that haven't been contacted yet. Use the existing Baileys-based sender at `/home/prata/leads/scripts/send_whatsapp.js`.

## Data Sources
1. `/home/prata/leads/data/serpapi_leads.json` — 110 new leads (74 with phones)
2. `/home/prata/leads/data/wa_sent.json` — 104 already sent (check by phone to avoid duplicates)
3. `/home/prata/leads/demos/` — 78 existing demo sites
4. `/home/prata/leads/scripts/send_whatsapp.js` — the WhatsApp sender

## Steps

### Step 1: Identify unsent leads
Read serpapi_leads.json and wa_sent.json. Filter to leads where:
- Phone number exists
- Phone number NOT in wa_sent.json (not already contacted)
- Has a demo site in /home/prata/leads/demos/ OR can use a generic demo URL

### Step 2: For each unsent lead, send WhatsApp message
Use the sender script: `node /home/prata/leads/scripts/send_whatsapp.js --to <phone> --msg "<message>"`

The message format (keep under 300 chars):
```
Hi, this is Kevin — web developer based in Mumbai. I came across [Business Name] on Google Maps and noticed you don't have a website. You've got great reviews so I built a quick preview site using your Google profile details. No commitment — just wanted to show you what's possible. 30 seconds to look: [DEMO_URL]
```

Rules:
- Replace [Business Name] with the actual business name
- Replace [DEMO_URL] with the demo site URL if it exists in demos/ folder
- If no demo exists, use: `https://kevinpratap.github.io/lead-demos/<slug>/` where slug is the business name lowercase, spaces replaced with hyphens
- Add 3-5 second delay between messages to avoid rate limiting
- Log each send to a new file: `/home/prata/leads/data/wa_sent_new.json`

### Step 3: After sending, update wa_sent.json
Append all new sends to the existing wa_sent.json file.

### Step 4: Print summary
- Total messages sent
- Total failed
- List of businesses contacted
- Time taken

## Important
- DO NOT send to numbers already in wa_sent.json
- DO NOT send more than 1 message per business
- If a message fails (error), skip and continue to next
- Keep messages natural and non-spammy
- Use the exact phone format as stored in serpapi_leads.json
