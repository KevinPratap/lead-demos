# Task: Send WhatsApp Messages to New Leads (CORRECTED URLS)

## Goal
Send WhatsApp messages to new leads. Demo URLs use the format: https://kevinpratap.github.io/lead-demos/demos/<slug>/

## Data
Read from: /home/prata/leads/data/serpapi_leads.json
Already sent: /home/prata/leads/data/wa_sent.json (check by phone number to skip)

## The 20 leads and their demo URLs
Match each lead from serpapi_leads.json to a demo folder in /home/prata/leads/demos/demos/:
- mumbai -> https://kevinpratap.github.io/lead-demos/demos/mumbai/
- yogasadhana -> https://kevinpratap.github.io/lead-demos/demos/yogasadhana/
- sanguine-fitness-studio -> https://kevinpratap.github.io/lead-demos/demos/sanguine-fitness-studio/
- sudipa-yogalaya---yoga-classes-near-me-best-yoga-classesyoga-trainercorporate-yoga-in-andheri -> https://kevinpratap.github.io/lead-demos/demos/sudipa-yogalaya---yoga-classes-near-me-best-yoga-classesyoga-trainercorporate-yoga-in-andheri/
- physio-fit-by-drtanvi-y-shah -> https://kevinpratap.github.io/lead-demos/demos/physio-fit-by-drtanvi-y-shah/
- dr-karishmas-core-physio -> https://kevinpratap.github.io/lead-demos/demos/dr-karishmas-core-physio/
- flex-and-flow-physiotherapy-clinic-expert-physiotherapist-in-vile-parle-east -> https://kevinpratap.github.io/lead-demos/demos/flex-and-flow-physiotherapy-clinic-expert-physiotherapist-in-vile-parle-east/
- luxury-spa-in-juhu-mumbai -> https://kevinpratap.github.io/lead-demos/demos/luxury-spa-in-juhu-mumbai/
- luxury-spa-premium-unisex-salon-in-mumbai -> https://kevinpratap.github.io/lead-demos/demos/luxury-spa-premium-unisex-salon-in-mumbai/
- relax-at-a-spa-hotel-in-mumbai -> https://kevinpratap.github.io/lead-demos/demos/relax-at-a-spa-hotel-in-mumbai/
- lubss-spa-luxuries-juhu -> https://kevinpratap.github.io/lead-demos/demos/lubss-spa-luxuries-juhu/
- myrah---juhu -> https://kevinpratap.github.io/lead-demos/demos/myrah---juhu/
- urban-luxury-spa-in-juhu -> https://kevinpratap.github.io/lead-demos/demos/urban-luxury-spa-in-juhu/
- best-body-spa-in-andheri-mumbai -> https://kevinpratap.github.io/lead-demos/demos/best-body-spa-in-andheri-mumbai/
- massage-centre-in-andheri-west-mumbai-massage-in-mumbai -> https://kevinpratap.github.io/lead-demos/demos/massage-centre-in-andheri-west-mumbai-massage-in-mumbai/
- allure-thai-spa-wellness---spa-in-marol-andheri-east -> https://kevinpratap.github.io/lead-demos/demos/allure-thai-spa-wellness---spa-in-marol-andheri-east/
- royal-thai-spa -> https://kevinpratap.github.io/lead-demos/demos/royal-thai-spa/
- royal-spa-andheri -> https://kevinpratap.github.io/lead-demos/demos/royal-spa-andheri/
- the-lash-house -> https://kevinpratap.github.io/lead-demos/demos/the-lash-house/
- tip-and-toe-luxe-the-nail-lashes-brows-microblading---bandra -> https://kevinpratap.github.io/lead-demos/demos/tip-and-toe-luxe-the-nail-lashes-brows-microblading---bandra/

## Steps

### Step 1: Build send list from serpapi_leads.json
For each lead with phone number NOT in wa_sent.json, create entry with:
- phone (with 91 prefix)
- business_name
- niche
- demo_url (from mapping above)

### Step 2: Write send list
Save to /home/prata/leads/data/wa_final_send.json

### Step 3: Send each message
Use: node /home/prata/leads/scripts/send_whatsapp.js --to <phone> --msg "<message>"

Message rules:
- NO em dashes
- NO exclamation marks
- NO corporate speak
- Casual, lowercase, Indian English
- Vary structure across messages
- Under 250 chars
- Reference business name naturally

Message templates (rotate):
1. "hey, im kevin. i build websites for local businesses. saw your [type] on google and put together a quick mockup. no pressure, just thought you might want to see it: [url]"
2. "hey, quick question — does [name] have a website? i found you on google maps and thought you could use one. i made a rough version, take a look: [url]"
3. "hey, your [type] looks solid on google. noticed you dont have a site though. i threw together a quick one for you, check it out: [url]"
4. "hey kevin here. i make websites. saw your [type] on google, made you a quick demo. have a look: [url]"
5. "yo, im kevin. i build sites for local spots in mumbai. came across [name] and whipped up a quick version. see what you think: [url]"

Wait 3-5 seconds between sends.
Log each result to /home/prata/leads/data/wa_sent_results.json

### Step 4: Update wa_sent.json
Append new sends to wa_sent.json

### Step 5: Print summary
Total attempted, successful, failed, list of businesses
