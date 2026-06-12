# Task: Create WhatsApp message templates for new leads

## Goal
Create a JSON file with personalized WhatsApp messages for each new lead from serpapi_leads.json. Messages should sound like a real human wrote them — not a bot.

## Rules for messages
- NO em dashes (—)
- NO exclamation marks
- NO corporate speak ("no commitment", "what's possible", "great reviews")
- Casual, lowercase, Indian English
- Vary the structure — don't use the same template for every message
- Keep it under 250 characters
- Sound like a 20 year old student, not a salesperson
- Some can be shorter, some slightly longer
- Use "kevin" not "Kevin"
- Reference the specific business name or niche naturally

## Message style variations (rotate through these)
1. Short and direct: "hey, im kevin. i build websites for local businesses. saw your [business type] on google and put together a quick mockup. no pressure, just thought you might want to see it: [link]"

2. Question hook: "hey, quick question — does [business name] have a website? i found you on google maps and thought you could use one. i made a rough version, take a look: [link]"

3. Compliment first: "hey, your [business type] looks solid on google. noticed you dont have a site though. i threw together a quick one for you — zero obligation. check it out: [link]"

4. Super short: "hey kevin here. i make websites. saw your [business type] on google, made you a quick demo. have a look: [link]"

5. Casual mention: "yo, im kevin. i build sites for local spots in mumbai. came across [business name] and whipped up a quick version. see what you think: [link]"

## Data
Read from: /home/prata/leads/data/serpapi_leads.json
Filter: leads with phone numbers, not in wa_sent.json

## Output
Save to: /home/prata/leads/data/wa_messages_to_send.json
Format: JSON array of objects:
{
  "phone": "phone number",
  "business_name": "name",
  "niche": "niche",
  "demo_url": "url or empty string",
  "message": "the actual message text"
}

## Important
- Do NOT send any messages. Just create the file.
- Vary the message structure across leads — do NOT use the same template for all
- Some messages can be 2 lines, some 3, some 4
- Keep it natural. If you wouldn't send it to a real person, rewrite it.
