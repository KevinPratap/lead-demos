# Task: Compile Lead Generation Pitch Excel Document

## Goal
Create a comprehensive Excel workbook that combines:
1. All scraped leads from SerpAPI (new leads)
2. All previously sent WhatsApp leads (existing)
3. Pitch scripts and demo site links for each lead
4. A master pitch sheet with everything needed for outreach

## Data Sources
1. `/home/prata/leads/data/serpapi_leads.json` — 110 new leads from SerpAPI scrape (74 with phones)
2. `/home/prata/leads/data/wa_sent.json` — 104 previously sent WhatsApp messages
3. `/home/prata/leads/data/exports/pitch_sheet.md` — existing pitch sheet with scripts
4. `/home/prata/leads/demos/` — folder with generated demo sites

## Output
Save to: `/home/prata/leads/data/exports/Pitch_Book.xlsx`

## Excel Sheets to Create

### Sheet 1: "All Leads Master"
Columns:
- Business Name
- Niche (dental/salon/gym/barber/skin/cafe/yoga/physio/bakery/spa/eyelash)
- Phone Number
- Address
- Rating
- Website URL
- Demo Site URL (if generated)
- WhatsApp Sent (Yes/No)
- Sent Date
- Source (serpapi_organic / serpapi_local / previous_wa)

### Sheet 2: "Ready to Pitch" 
Filter of Sheet 1 where:
- Phone number exists
- WhatsApp Sent = No
- Has demo site OR needs demo generated
Columns same as Sheet 1 plus:
- Pitch Script (WhatsApp message template)
- Call Script (phone call template)
- Priority Score (based on rating + reviews — higher = better)

### Sheet 3: "WhatsApp Scripts"
For each lead in "Ready to Pitch":
- Business Name
- Phone
- Niche
- WhatsApp Message (copy-paste ready, with {demo_url} placeholder)
- Call Script (short version)
- Demo URL

### Sheet 4: "Sent Log"
From wa_sent.json:
- Business Name
- Phone
- Sent Date/Time
- Success (Yes/No)
- Demo URL used

### Sheet 5: "Summary Dashboard"
- Total leads count
- Leads by niche (table)
- Leads with phones count
- WhatsApp sent count
- Remaining to send count
- Demo sites generated count

## Formatting
- Professional clean look
- Header row: bold, dark background, white text
- Alternate row colors for readability
- Auto-filter on all sheets
- Freeze top row
- Column widths auto-fit
- Priority scores: conditional formatting (green=high, yellow=medium, red=low)

## Notes
- Use openpyxl for Excel generation
- If demo site folder exists in /home/prata/leads/demos/ for a business, link to it
- Match previous leads from wa_sent.json by phone number to mark as "Already Sent"
- For pitch scripts, use niche-specific templates (dental, salon, gym, etc.)
- Keep WhatsApp messages under 300 characters
