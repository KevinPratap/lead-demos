# Task: Regenerate 20 Demo Sites Using Original Design Style

## Goal
The 20 new demos at /home/prata/leads/demos/ look generic and sad. Regenerate them using the SAME design language as the original early demos (dental-clinic, the-glam-bar-salon) which looked clean and premium.

## Reference Files (READ THESE FIRST)
1. /home/prata/leads/demos/dental-clinic/index.html — the gold standard. Inter weight 200/300, minimal, clean
2. /home/prata/leads/demos/the-glam-bar-salon/index.html — salon style. Playfair Display + Inter, warm accent, hero image with overlay

## Design System (MATCH THE ORIGINAL EXACTLY)

### For DENTAL / PHYSIO / YOGO (clean, medical, trust)
- Font: Inter weight 200, 300, 400 only (NO weight 500+ for headings)
- Accent: #2563eb (blue) or #16a34a (green) for yoga
- Background: #fafafa
- Text: #111111
- Text-light: #666666
- Nav: uppercase letter-spacing 0.1em, logo left, phone right
- Hero: centered, rating badge pill, hero-label uppercase, h1 weight 200 large, stats-line with bullets
- Services: vertical list with border-bottom separators, h3 weight 300
- Gallery: full-width image break with 70vh height
- Featured section: centered, featured-title weight 200, featured-cta with border-bottom
- CTA section: centered, cta-button with accent bg, border-radius 100px
- Footer: uppercase, letter-spacing 0.15em, "Built by Kevin"
- Unsplash images with proper alt text

### For SALON / SPA / EYELASH (warm, premium, beauty)
- Font: Inter + Playfair Display (serif for headings)
- Accent: #b76e5a (warm terracotta) or #a78bfa (soft purple) or #d4a574 (gold)
- Background: #fafafa
- Hero: FULL SCREEN with background image + gradient overlay, white text, Playfair Display h1
- Phone link: white border, border-radius 100px, hover fills white
- Sections: alternating white/warm backgrounds
- Services: grid or list, serif headings
- CTA: accent color button, border-radius 100px
- Footer: simple, "Built by Kevin"

## Rules
- Copy the EXACT CSS structure from the reference files
- Use the same class names, same layout pattern, same spacing
- Only change: business name, phone, address, services, images, accent color
- Each demo should look like it belongs to the same family as dental-clinic and the-glam-bar-salon
- NO DM Sans, NO heavy weights, NO box shadows, NO card grids
- Keep it minimal, editorial, spacious
- Real Unsplash images per niche

## Leads to Regenerate (20)
All in /home/prata/leads/demos/<slug>/index.html:
1. mumbai (yoga) — green accent, yoga images
2. yogasadhana (yoga) — green accent
3. sanguine-fitness-studio (yoga) — green accent
4. sudipa-yogalaya (yoga) — green accent
5. physio-fit-by-drtanvi-y-shah (physio) — blue accent
6. dr-karishmas-core-physio (physio) — blue accent
7. flex-and-flow-physiotherapy-clinic (physio) — blue accent
8. luxury-spa-in-juhu-mumbai (spa) — warm terracotta, hero image
9. luxury-spa-premium-unisex-salon-in-mumbai (spa/salon) — warm terracotta
10. relax-at-a-spa-hotel-in-mumbai (spa) — warm terracotta
11. lubss-spa-luxuries-juhu (spa) — warm terracotta
12. myrah---juhu (spa) — soft purple
13. urban-luxury-spa-in-juhu (spa) — warm terracotta
14. best-body-spa-in-andheri-mumbai (spa) — warm terracotta
15. massage-centre-in-andheri-west-mumbai (spa) — warm terracotta
16. allure-thai-spa-wellness (spa) — warm terracotta
17. royal-thai-spa (spa) — gold accent
18. royal-spa-andheri (spa) — warm terracotta
19. the-lash-house (eyelash/salon) — soft purple, Playfair Display
20. tip-and-toe-luxe (eyelash/salon) — soft purple, Playfair Display

## After Regenerating
1. Push all changes to GitHub: cd /home/prata/leads/demos && git add -A && git commit -m "fix: regenerate 20 demos with original design style" && git push origin main
2. Wait 10 seconds for GitHub Pages to build
3. Verify 2-3 URLs work: https://kevinpratap.github.io/lead-demos/demos/mumbai/ etc.
4. Print summary of all 20 regenerated sites
