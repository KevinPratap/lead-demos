# Task: Save Real Design Token Data to Obsidian

## Goal
Take the actual CSS design tokens extracted from 9 live websites at /home/prata/leads/design-inspiration/design_tokens.json and save them to the Obsidian vault as structured, actionable design reference docs.

## Source Data
Read: /home/prata/leads/design-inspiration/design_tokens.json

This contains real CSS extracted via Chrome DevTools from:
- Dental: Seattle Dental Co (Lato, 45px/700 H1, dark CTA, sharp corners), BiteStudio (Assistant, 40px/400 H1, minimal)
- Spa: Scandinave (Times New Roman, 72px white hero), SpaBelles (proxima-nova, 72px white hero, white sections)
- Salon: Oasis Aveda (Poppins, 84px, pink #f0c8e0 text, alternating #f8ecf3 pink and #15112a dark sections)
- Yoga: Yogaworks (Seabirds Trial, 64px/430, white/f8f8f8 alternating, 100px pill buttons), CorePower Yoga (Poppins, 40px radius buttons)
- Physio: Athletico (acumin-pro, 90px/400 white on black)
- Gym: Barry's (Benton Sans Pro, 48px/700 white, dark sections)

## What to Create

### 1. Update all 6 niche design files
Replace the guessed values with REAL extracted CSS values. Files at:
/mnt/c/Users/prata/OneDrive/Documents/Obsidian Vault/20_Areas/Dev/Design_References/

Each file MUST include:

#### Actual CSS Token Table
```markdown
| Site | Font | H1 Size | H1 Weight | H1 Color | BG Colors | CTA Style |
|------|------|---------|-----------|----------|-----------|-----------|
| Seattle Dental Co | Lato | 45px | 700 | #3a3a3a | #fff | Dark bg (#3a3a3a), 0px radius |
| BiteStudio | Assistant | 40px | 400 | #121212 | #fff | Transparent, 0px radius |
```

#### CSS Custom Properties Snippet
```css
/* Put the actual hex values, not guesses */
:root {
  --color-text: #3a3a3a;
  --color-heading: #3a3a3a;
  --color-bg: #ffffff;
  --color-accent: #3a3a3a;
  --font-primary: 'Lato', sans-serif;
  --font-size-h1: 45px;
  --font-weight-h1: 700;
  --button-radius: 0px;
  --button-bg: #3a3a3a;
  --button-color: #fff;
}
```

### 2. Create a master summary doc
/mnt/c/Users/prata/OneDrive/Documents/Obsidian Vault/20_Areas/Dev/Design_References/Real_Design_Tokens.md

This one file has ALL 9 sites in a comparison table with their actual CSS values side by side.

### 3. Key rules
- Use actual extracted values, not guesses
- If a value wasn't extracted, mark it as "—"
- Convert rgb() to hex where possible
- Keep the CSS snippets copy-paste ready
- Link to the original screenshots URL
- Tag all files: tags: [design-reference, css-tokens, extracted]
