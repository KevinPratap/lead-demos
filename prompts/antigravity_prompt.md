# Antigravity Prompt — Demo Site Build

Copy this into Google Antigravity (or Claude Code, or Cursor). Fill in the business
name and Maps URL for the lead you want to demo. The model will read the Maps profile
and build a single-page HTML site in a subfolder.

---

**Prompt template (replace {NAME} and {MAPS_URL} with the lead from `data/exports/pitch_sheet.md`):**

```
Build a single-page website for this business. Folder name: leads/{slug}
where slug is the business name lowercased, dashes instead of spaces, no special chars.

Business name: {NAME}
Google Maps profile: {MAPS_URL}

Requirements:
1. Read the Google Maps profile URL and extract: phone, address, hours, rating, reviews count, category, services, photos.
2. Create leads/{slug}/index.html with embedded CSS. No JS frameworks. Pure HTML+CSS, fully responsive.
3. Structure:
   - Top nav with business name + phone (clickable tel: link) + "Get Directions" button (links to the Google Maps URL above)
   - Hero section: business name as H1, rating badge (e.g. "4.9 ⭐ on Google · 312 reviews"), tagline pulled from their category/services
   - About section: 2-3 short paragraphs about the business (write copy based on their category + services)
   - Services section: bullet list / icon grid of services
   - Why choose us: 3-4 differentiators (write reasonable defaults if no data)
   - Hours section: table of opening hours from the Maps data
   - Contact section: address, phone, embedded Google Maps iframe, "Book Appointment" CTA (phone: link)
   - Footer with business name and a small "Demo created by Kevin" credit
4. Use 1-2 of the actual photos from their Google Maps profile as the hero/section images (or generate placeholder gradients if you can't fetch). Keep file size small.
5. Make it look like a real, premium local business site — clean typography (system font stack), generous whitespace, single accent color. NOT generic "AI slop" — think how a real web designer would build a dental clinic site in 2024.
6. When done, show me a one-line summary of what you built and the file path.
7. Do NOT create a git commit — I'll do that manually after I review it.

When the site looks good, stop and let me review.
```

**After Antigravity finishes:**
```bash
cd ~/leads
# preview locally
python3 -m http.server 8000 --directory /tmp/preview/leads/{slug}  # or just open the HTML file
# if happy, push to GitHub Pages repo
cd ~/lead-demos   # your GitHub Pages repo (one-time clone)
mkdir -p {slug}
cp -r ~/leads/leads/{slug}/* {slug}/
cd lead-demos
git add {slug}
git commit -m "demo: {NAME}"
git push
# Live URL: https://<your-username>.github.io/lead-demos/{slug}/
```

**Pitch script (use after the demo is live):**

Call the business. Once they answer:

> "Hi, this is Kevin. I'm a web developer here in Mumbai, and I came across {NAME} on Google Maps.
> I was really impressed by your reviews — {RATING} stars, {N} reviews — but I noticed you don't
> have a website yet, so when patients search for {NICHE}, they can't book online or see your
> services properly.
> I actually took the liberty of building a sample website for you — completely free, no strings
> attached. Can I send you the link? It's at [URL]. Even if you don't like it, you can see what
> your practice could look like online in a day. Would that be helpful?"

**Tracking**: update the `leads` table to mark when pitched, and the outcome.
