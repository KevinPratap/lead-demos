# Task: Send WhatsApp Messages with Just Demo Links

## Goal
Send a SECOND WhatsApp message to the 20 leads. This time just send the demo link with a short follow-up. No long pitch text.

## Leads and Demo URLs
Read from /home/prata/leads/data/serpapi_leads.json
Match phone numbers. Demo URLs:

1. mumbai -> https://kevinpratap.github.io/lead-demos/demos/mumbai/
2. yogasadhana -> https://kevinpratap.github.io/lead-demos/demos/yogasadhana/
3. sanguine-fitness-studio -> https://kevinpratap.github.io/lead-demos/demos/sanguine-fitness-studio/
4. sudipa-yogalaya---yoga-classes-near-me-best-yoga-classesyoga-trainercorporate-yoga-in-andheri -> https://kevinpratap.github.io/lead-demos/demos/sudipa-yogalaya---yoga-classes-near-me-best-yoga-classesyoga-trainercorporate-yoga-in-andheri/
5. physio-fit-by-drtanvi-y-shah -> https://kevinpratap.github.io/lead-demos/demos/physio-fit-by-drtanvi-y-shah/
6. dr-karishmas-core-physio -> https://kevinpratap.github.io/lead-demos/demos/dr-karishmas-core-physio/
7. flex-and-flow-physiotherapy-clinic-expert-physiotherapist-in-vile-parle-east -> https://kevinpratap.github.io/lead-demos/demos/flex-and-flow-physiotherapy-clinic-expert-physiotherapist-in-vile-parle-east/
8. luxury-spa-in-juhu-mumbai -> https://kevinpratap.github.io/lead-demos/demos/luxury-spa-in-juhu-mumbai/
9. luxury-spa-premium-unisex-salon-in-mumbai -> https://kevinpratap.github.io/lead-demos/demos/luxury-spa-premium-unisex-salon-in-mumbai/
10. relax-at-a-spa-hotel-in-mumbai -> https://kevinpratap.github.io/lead-demos/demos/relax-at-a-spa-hotel-in-mumbai/
11. lubss-spa-luxuries-juhu -> https://kevinpratap.github.io/lead-demos/demos/lubss-spa-luxuries-juhu/
12. myrah---juhu -> https://kevinpratap.github.io/lead-demos/demos/myrah---juhu/
13. urban-luxury-spa-in-juhu -> https://kevinpratap.github.io/lead-demos/demos/urban-luxury-spa-in-juhu/
14. best-body-spa-in-andheri-mumbai -> https://kevinpratap.github.io/lead-demos/demos/best-body-spa-in-andheri-mumbai/
15. massage-centre-in-andheri-west-mumbai-massage-in-mumbai -> https://kevinpratap.github.io/lead-demos/demos/massage-centre-in-andheri-west-mumbai-massage-in-mumbai/
16. allure-thai-spa-wellness---spa-in-marol-andheri-east -> https://kevinpratap.github.io/lead-demos/demos/allure-thai-spa-wellness---spa-in-marol-andheri-east/
17. royal-thai-spa -> https://kevinpratap.github.io/lead-demos/demos/royal-thai-spa/
18. royal-spa-andheri -> https://kevinpratap.github.io/lead-demos/demos/royal-spa-andheri/
19. the-lash-house -> https://kevinpratap.github.io/lead-demos/demos/the-lash-house/
20. tip-and-toe-luxe-the-nail-lashes-brows-microblading---bandra -> https://kevinpratap.github.io/lead-demos/demos/tip-and-toe-luxe-the-nail-lashes-brows-microblading---bandra/

## Message Format
Keep it super short. Just the link with one line before it. Examples:
- "hey, here's that website i mentioned: [url]"
- "quick follow-up — the site is ready: [url]"
- "hey, in case you missed it: [url]"
- "the demo site is live now: [url]"
- "here's the link again: [url]"

Rotate through these. Keep it casual, lowercase, no punctuation except periods.

## Steps
1. Read serpapi_leads.json to get phone numbers
2. For each of the 20 leads, send: node /home/prata/leads/scripts/send_whatsapp.js --to <phone> --msg "<short message with url>"
3. Wait 3-5 seconds between sends
4. Log results to /home/prata/leads/data/wa_sent_links.json
5. Print summary
