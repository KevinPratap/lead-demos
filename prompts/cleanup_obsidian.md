# Task: Clean Up and Reorganize Obsidian Vault

## Goal
Clean up the Obsidian vault at `/mnt/c/Users/prata/OneDrive/Documents/Obsidian Vault/` by:
1. Moving misplaced files to their correct locations
2. Creating proper MOC (Map of Content) files for all folders
3. Ensuring all project data from /home/prata/leads/ is documented in Obsidian
4. Creating a proper structure for the Lead Pipeline project
5. Removing duplicates and backup files
6. Updating Atlas.md to reflect the full structure

## Current Issues to Fix

### 1. Duplicate Hermes folders
- `/Hermes/` (root level) — contains only Journal folder, should be removed (duplicate of 90_System/Hermes)
- `/90_System/Hermes/` — this is the canonical one, keep it
- ACTION: Delete `/Hermes/` folder entirely (it's a duplicate, the real one is in 90_System)

### 2. Loose file in 20_Areas
- `/20_Areas/Sudiksha_Singh_Info.md` — should move to `/20_Areas/Cybersecurity/Investigations/`

### 3. Lead Pipeline project needs Obsidian documentation
The `/home/prata/leads/` folder has all the pipeline data but it's not reflected in Obsidian.
Create the following notes in `/10_Projects/Lead_Pipeline/`:

#### 3a. `Lead_Pipeline.md` — Main MOC for the project
Content should include:
- Project overview: Mumbai business lead generation for web dev outreach
- Data sources: SerpAPI (110 leads), previous WhatsApp sends (104 messages)
- Pipeline stages: Scrape → Demo Generation → WhatsApp Send → Follow-up
- Key files and their locations (in /home/prata/leads/)
- Links to all sub-notes

#### 3b. `SerpAPI_Leads.md` — About the SerpAPI scrape
- 110 unique leads across 10 niches
- 74 with phone numbers
- Search queries used
- Link to the data file

#### 3c. `WhatsApp_Outreach.md` — About the WhatsApp sending system
- 104 messages already sent to 91 unique businesses
- Baileys-based sender (send_whatsapp.js)
- Message templates per niche
- Success rate

#### 3d. `Demo_Sites.md` — About demo site generation
- 78 demo sites generated in /home/prata/leads/demos/
- Template system (4 templates)
- GitHub Pages deployment
- Per-niche design approach

#### 3e. `Pitch_Book.md` — About the Excel pitch book
- Pitch_Book.xlsx location and structure
- 5 sheets summary
- 40 leads ready to pitch
- Link to the Excel file

### 4. Create/update MOC files

#### 4a. `/10_Projects/10_Projects_MOC.md`
List all projects with brief descriptions:
- Lead_Pipeline — Mumbai business lead gen + WhatsApp outreach
- IncomeAutomation — Gumroad digital products
- Nebula — Interview copilot app
- Saifee_Dental_Clinic — Demo client project
- Kevin_EXE — Personal executable project
- Agents_Orchestrators — Multi-agent system
- Computer_Vision — CV projects
- Machine_Dealer — ML project
- Voice_Intelligence — Voice AI projects
- Productivity_Tools — Tool collection
- Sonic Pill — Audio project
- Industrial_B2B — B2B project
- Cold_Mail_AI — Cold email automation
- Face_Recognition — Face recognition project
- Hand_Tracking — Hand tracking project
- Image_Recognition — Image recognition project
- Jarvis_Agentic_Core — AI agent core
- ML_Chatbot — ML chatbot project
- Nebula_Assistant — Nebula assistant
- Nebula_Ecosystem — Nebula ecosystem

#### 4b. `/20_Areas/20_Areas_MOC.md`
List all areas:
- AI — AI/ML notes (LangChain.md)
- Career — Career and internship notes
- Cybersecurity — Security tools, investigations, OSINT
- Dev — Development tools (Deno.md, Neovim.md)
- DevOps — DevOps tools (Docker, K8s, Vercel, Netlify, GitLab, PlanetScale)

#### 4c. Update `/20_Areas/Cybersecurity/Cybersecurity_MOC.md`
Ensure it links to ALL cybersecurity notes:
- Burp_Suite.md, GODMODE.md, Kali_Linux.md, Mantis.md, Metasploit_Framework.md
- Nmap.md, Phishing.md, Sherlock.md, Tshark.md
- Investigations/ folder with all OSINT dossiers
- Kevin_Pratap_SELF_OSINT.md

### 5. Clean up Lead_Pipeline folder
In `/10_Projects/Lead_Pipeline/`:
- Delete `pitch_sheet.md.bak` (backup file)
- Delete `pitch_sheet_fresh.md` (duplicate)
- Keep only: config.yaml, data/, prompts/, scripts/, README.md, Lead_Pipeline.md, and the new notes

### 6. Update Atlas.md
Ensure Atlas.md at vault root links to:
- All major MOCs
- Lead_Pipeline project
- Cybersecurity hub
- Agent_Bootstrap system
- All areas and projects

## Rules
- Use wikilinks [[like this]] for all internal links
- Keep descriptions concise (1-2 lines per item)
- Use consistent formatting: ## for sections, bullet points for lists
- All new notes should have a frontmatter tag: `tags: [moc]` for MOC files
- Don't delete any data files (.json, .db, .csv) — only delete .md backup/duplicate files
- Don't touch the .obsidian/ folder
