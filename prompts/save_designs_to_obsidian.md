# Task: Analyze Design Reference Screenshots and Save Patterns to Obsidian

## Goal
Go through the 127 design reference screenshots at `/home/prata/leads/design-inspiration/` and extract the DESIGN PATTERNS from each niche. Save these as markdown reference docs in the Obsidian vault so the designs can be referenced without opening images.

## Source
127 screenshots in `/home/prata/leads/design-inspiration/`:
- dental/ (29)
- spa/ (47)  
- salon/ (19)
- yoga/ (25)
- gym/ (5)
- physio/ (2)

## What to Extract Per Niche
For each niche, create a design pattern document analyzing:

### 1. Common Layout Patterns
- Hero section structure (what's above the fold)
- Navigation style
- Content section ordering
- CTA placement
- Footer style

### 2. Color Palettes
- Most common accent colors
- Background colors (white, off-white, dark, gradient)
- Text color conventions
- Any niche-specific color themes

### 3. Typography
- Common font pairings
- Heading styles (weight, size, case)
- Body text conventions

### 4. Component Patterns
- Button styles (filled, outlined, pill, rounded)
- Card layouts
- Image treatment
- Form styles
- Icon usage

### 5. Unique Elements
- What makes the best designs stand out
- Any recurring motifs
- Animation/interaction patterns visible

### 6. Anti-Patterns
- What looks dated or cheap
- What to avoid

## Output
Save to Obsidian vault at `/mnt/c/Users/prata/OneDrive/Documents/Obsidian Vault/20_Areas/Dev/Design_References/`

One file per niche:
- `Dental_Design_Patterns.md`
- `Spa_Design_Patterns.md`
- `Salon_Design_Patterns.md`
- `Yoga_Design_Patterns.md`
- `Gym_Design_Patterns.md`
- `Physio_Design_Patterns.md`

Plus a master MOC:
- `Design_Reference_MOC.md`

## Approach
Since you can't actually "see" the images, use your training knowledge of these known design references based on the business names in the filenames. The dental images include well-documented sites like:
- Seattle Dental Co (ultra-clean, minimal, Inter font, blue accent)
- Tend (bold branding, dark green, lifestyle photography)
- Bite Dental (modern, warm colors, editorial photography)
- Zen Dental (calm, spa-like, muted tones)
- Spencer Dentistry (professional, clean, blue-white)
- Beverly Hills Dentistry (luxury, gold accents)

The spa images include:
- Float Luxury Spa (dark, moody, premium)
- Mamounia (Moroccan luxury, gold, ornate)
- Scandinave (Nordic minimal, nature-focused)
- Various Colorlib spa themes

## Rules
- Write as actionable design specs, not just observations
- Include CSS snippets where useful (hex codes, font stacks, shadow values)
- Link back to the inspiration index URL
- Keep each doc under 500 lines
- Use consistent headings and structure across all docs
- Tag all files: `tags: [design-reference, html, css, templates]`
