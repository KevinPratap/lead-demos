# Task: Create a Sample Gym Demo Website Using Real Design Reference

## Goal
Create ONE demo for a gym business using the EXACT design tokens extracted from Barry's (barrys.com) — a world-class HIIT fitness brand. This is a SAMPLE to prove we're on the right path.

## Business
Pick any gym lead from serpapi_leads.json that has a phone number. Use their real name, phone, and address.

## Design System (EXTRACTED FROM LIVE SITE)

### Typography
- Font: Benton Sans Pro → substitute with 'Inter', system-ui, sans-serif (closest match)
- H1: 48px / weight 700 / white (#ffffff)
- Body: 16px / weight 400 / white on dark

### Colors
- Background: #000000 (black) or very dark #111111
- Text: #ffffff on dark sections
- Accent/CTA: #ff0000 (red — from real Barry's buttons)
- No soft colors. This is intense, bold, gym energy.

### Layout
- Hero: FULL SCREEN dark background with large white H1
- No card shadows — sharp edges, brutalist
- 0px border radius everywhere (sharp corners)
- Bold, aggressive, high-contrast
- Full-width image sections

### Buttons
- Transparent background, red (#ff0000) text
- 0px border radius — SHARP corners
- Uppercase text or bold weight
- White outline on dark bg

### Sections
- Hero → Classes/Programs → Pricing → Location → CTA
- Dark backgrounds throughout
- Alternating black (#000000) and very dark gray (#111111)
- High-contrast white text

### Anti-patterns (DO NOT USE)
- NO rounded corners (no border-radius)
- NO soft pastels or calming colors
- NO cards with shadows
- NO serif fonts
- NO playful elements
- NO light backgrounds
- NO em dashes, no exclamation marks in copy

## HTML Structure
```html
<!DOCTYPE html>
<html>
<head>
  <title>Gym Name — Mumbai</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" rel="stylesheet">
  <style>
    /* Black background, white text, red accent, 0px radius */
    /* H1: 48px/700, sharp, bold */
    /* Full bleed sections */
  </style>
</head>
<body>
  <!-- Dark nav -->
  <!-- Full screen hero with white H1 -->
  <!-- Classes grid -->
  <!-- Pricing section -->
  <!-- Location with map -->
  <!-- CTA: red text on dark bg -->
  <!-- Footer -->
</body>
</html>
```

## Output
Save to: /home/prata/leads/demos/<slug>/index.html
Push to GitHub Pages
Print the demo URL and a brief summary of what design decisions were made

## Reference
Barry's real CSS: H1 48px/700 white, black bg, red #ff0000 accent, Benton Sans Pro font, 0px radius, dark intense energy
