# Task: Generate Demo Sites for New Leads Using Award-Winning Designs

## Goal
Generate demo website HTML files for 20 new leads that don't have demos yet. Use design patterns from award-winning websites (Airbnb, Stripe, Notion) — NOT generic AI slop templates.

## Leads to Generate
Read from: /home/prata/leads/data/wa_messages_to_send.json
These 20 leads need demo sites:
1. Mumbai (yoga studio)
2. Yogasadhana (yoga studio)
3. Sanguine Fitness Studio (yoga studio)
4. Sudipa Yogalaya (yoga studio)
5. Physio-Fit by Dr.Tanvi Y Shah (physio)
6. Dr. Karishma's Core Physio (physio)
7. Flex and Flow Physiotherapy Clinic (physio)
8. Luxury Spa in Juhu, Mumbai (spa)
9. Luxury Spa & Premium Unisex Salon in Mumbai (spa)
10. Relax at a Spa Hotel in Mumbai (spa)
11. Lubss Spa Luxuries Juhu (spa)
12. MYRAH - Juhu (spa)
13. Urban Luxury Spa In Juhu (spa)
14. Best Body Spa in Andheri, Mumbai (spa)
15. Massage Centre in Andheri West Mumbai (spa)
16. Allure Thai Spa & Wellness (spa)
17. Royal Thai Spa (spa)
18. Royal Spa Andheri (spa)
19. The Lash House (eyelash)
20. Tip and Toe Luxe (eyelash)

## Design System (use these exact values)

### For SPA / SALON / EYELASH leads (warm, premium, Airbnb-inspired)
- Background: #ffffff
- Text: #222222 (near-black, NOT pure black)
- Accent: #ff385c (Rausch Red) OR #e07b5a (warm terracotta)
- Secondary text: #6a6a6a
- Font: 'DM Sans', system-ui, sans-serif
- Border radius: 12px cards, 8px buttons, 50% for circular elements
- Shadows: three-layer warm stack — rgba(0,0,0,0.02) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 6px, rgba(0,0,0,0.1) 0px 4px 8px
- Spacing: 8px base unit, generous whitespace
- Hero: large heading (48px), warm accent color, photography placeholder with gradient
- Sections: alternating white and warm white (#f8f7f6)
- CTA button: accent color bg, white text, 8px radius, 12px 28px padding
- NO em dashes, NO exclamation marks in copy

### For YOGA / PHYSIO leads (calm, Notion-inspired)
- Background: #ffffff
- Text: rgba(0,0,0,0.95)
- Accent: #2a9d9d (teal) OR #5b8c5a (sage green)
- Secondary text: #615d59
- Font: 'Inter', system-ui, sans-serif
- Border radius: 12px cards, 4px buttons
- Borders: 1px solid rgba(0,0,0,0.1) whisper borders
- Shadows: multi-layer, max opacity 0.04
- Sections: alternating white and #f6f5f4 (warm white)
- CTA: accent color, 4px radius, subtle
- Calm, spacious layout — lots of breathing room

## HTML Structure (each file)
```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Business Name] — [City]</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <!-- OR for yoga/physio: -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* All CSS embedded — no external dependencies except Google Fonts */
  </style>
</head>
<body>
  <!-- Sticky nav: business name left, phone link right, CTA button -->
  <!-- Hero: H1, tagline, CTA button, gradient/photo placeholder -->
  <!-- About section: 2-3 paragraphs about the business -->
  <!-- Services grid: 3-4 service cards with icons/emoji -->
  <!-- Why choose us: 3 points -->
  <!-- Hours table -->
  <!-- Contact: phone, address, embedded Google Maps iframe -->
  <!-- Footer: "Demo by Kevin" credit -->
</body>
</html>
```

## Rules
- Each demo goes in its own folder: /home/prata/leads/demos/<slug>/index.html
- Slug format: business name lowercase, spaces to hyphens, remove special chars
- Pure HTML+CSS, fully responsive, no JS frameworks
- Use REAL Unsplash photos for hero images (search by niche: spa, yoga, physio, salon)
  - Format: https://images.unsplash.com/photo-[ID]?w=1200&h=600&fit=crop
  - Good spa photos: photo-1544161515-4ab6ce6db874, photo-1540555700478-4be289fbecef
  - Good yoga photos: photo-1545205597-3d9d02c29597, photo-1506126613408-eca07ce68773
  - Good physio photos: photo-1576091160399-112ba8d25d1d, photo-1519824145371-296894a0daa5
  - Good salon/lash photos: photo-1560066984-138dadb4c035, photo-1487412912498-0447578fcca8
- NO placeholder "lorem ipsum" — write real-sounding business copy
- NO generic "we are the best" — be specific to the niche
- NO em dashes (—), NO exclamation marks (!)
- Phone numbers should be clickable tel: links
- Maps iframe should use the business name in the query
- Each demo should look DISTINCT — vary the layout, color accent, and section order

## Output
For each lead, create: /home/prata/leads/demos/<slug>/index.html
Print progress: "Created: <business name> -> demos/<slug>/index.html"
Print total count at the end.
