# Task: Scrape More Award-Winning Design References

## Goal
Expand our design reference library beyond the initial 127 screenshots. Scrape additional award-winning local business website designs from:

## Sources to Scrape

### 1. SiteInspire (siteinspire.com)
- https://www.siteinspire.com/websites?categories=40 (healthcare)
- https://www.siteinspire.com/websites?categories=38 (fitness)
- https://www.siteinspire.com/websites?categories=32 (beauty)
- https://www.siteinspire.com/websites?categories=23 (food)

### 2. Awwwards (awwwards.com)
- https://www.awwwards.com/websites/health/
- https://www.awwwards.com/websites/beauty/
- https://www.awwwards.com/websites/fitness/

### 3. CSS Design Awards (cssdesignawards.com)
- Search: dentist website, spa website, salon website, yoga studio, gym website, physio clinic

### 4. Best Website Gallery (bestwebsite.gallery)
- Search: dental, spa, salon, fitness, yoga

## Method
For each source:
1. Navigate to page via Chrome CDP (port 9222)
2. Wait for load
3. Extract all screenshot image URLs
4. Download images to /home/prata/leads/design-inspiration/<niche>/
5. Name files after the business/domain

Also for the top 3-4 best looking sites, visit the actual live website and extract real CSS:
- Font family
- H1 size/weight/color
- Body background
- Button styles (bg, color, radius)
- Section colors

Save CSS tokens to /home/prata/leads/design-inspiration/design_tokens.json (append, don't overwrite)

## Output
- New screenshots in /home/prata/leads/design-inspiration/<niche>/
- Updated design_tokens.json
- Updated index.html gallery
- Push to GitHub
- Print summary: how many new images per niche, how many new CSS extractions
