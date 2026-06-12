#!/usr/bin/env python3
"""Generate demo sites for ANY niche. v4 — 4 distinct templates, randomly assigned."""
import sqlite3, re, os, json, hashlib, random

DB = "/home/prata/leads/data/leads.db"
DEMOS = "/home/prata/leads/demos"

# 4 templates with distinct layouts — randomly picked per lead
TEMPLATE_FILES = [
    "/home/prata/leads/scripts/template_1_card.html",
    "/home/prata/leads/scripts/template_2_editorial.html",
    "/home/prata/leads/scripts/template_3_split.html",
    "/home/prata/leads/scripts/template_4_boutique.html",
]

# Verify templates exist
for tf in TEMPLATE_FILES:
    if not os.path.exists(tf):
        print(f"WARNING: Template not found: {tf}")
        TEMPLATE_FILES.remove(tf)

if not TEMPLATE_FILES:
    print("ERROR: No templates found!")
    exit(1)

print(f"Loaded {len(TEMPLATE_FILES)} templates: {[os.path.basename(t) for t in TEMPLATE_FILES]}")

# ── Niche accent colors (CSS hex) & Real Unsplash Images ──
NICHE_ACCENT = {
    "dental":    {
        "accent": "#2563eb",
        "accent_light": "#dbeafe",
        "hero_img1": "https://images.unsplash.com/photo-1606811971618-4486d14f3f99?w=600&h=800&fit=crop",
        "hero_img2": "https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=600&h=800&fit=crop",
        "gallery_img1": "https://images.unsplash.com/photo-1598256989800-fe5f95da9787?w=600&h=800&fit=crop",
        "gallery_img2": "https://images.unsplash.com/photo-1512223792601-592a9809eed4?w=600&h=800&fit=crop",
        "gallery_img3": "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=600&h=400&fit=crop"
    },
    "beauty":    {
        "accent": "#b76e5a",
        "accent_light": "#fdf2ed",
        "hero_img1": "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=600&h=800&fit=crop",
        "hero_img2": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&h=800&fit=crop",
        "gallery_img1": "https://images.unsplash.com/photo-1487412912498-0447578fcca8?w=600&h=800&fit=crop",
        "gallery_img2": "https://images.unsplash.com/photo-1600948836101-f9ffda59d250?w=600&h=800&fit=crop",
        "gallery_img3": "https://images.unsplash.com/photo-1560750588-73207b1ef5b8?w=600&h=400&fit=crop"
    },
    "gym":       {
        "accent": "#16a34a",
        "accent_light": "#dcfce7",
        "hero_img1": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&h=800&fit=crop",
        "hero_img2": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&h=800&fit=crop",
        "gallery_img1": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&h=800&fit=crop",
        "gallery_img2": "https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=600&h=800&fit=crop",
        "gallery_img3": "https://images.unsplash.com/photo-1540497077202-7c8a3999166f?w=600&h=400&fit=crop"
    },
    "lab":       {
        "accent": "#7c3aed",
        "accent_light": "#ede9fe",
        "hero_img1": "https://images.unsplash.com/photo-1579154204601-01588f35116f?w=600&h=800&fit=crop",
        "hero_img2": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=600&h=800&fit=crop",
        "gallery_img1": "https://images.unsplash.com/photo-1530026405186-ed1ea0ac7a63?w=600&h=800&fit=crop",
        "gallery_img2": "https://images.unsplash.com/photo-1614935151651-0dec300bb0db?w=600&h=800&fit=crop",
        "gallery_img3": "https://images.unsplash.com/photo-1513224502586-d1e602410265?w=600&h=400&fit=crop"
    },
    "default":   {
        "accent": "#4f46e5",
        "accent_light": "#eef2ff",
        "hero_img1": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=800&fit=crop",
        "hero_img2": "https://images.unsplash.com/photo-1497366216548-37526070297c?w=600&h=800&fit=crop",
        "gallery_img1": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&h=800&fit=crop",
        "gallery_img2": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=600&h=800&fit=crop",
        "gallery_img3": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=600&h=400&fit=crop"
    },
}

NICHE_SERVICE_ICONS = {
    "dental":    ["", "", "", ""],
    "beauty":    ["", "", "", ""],
    "gym":       ["", "", "", ""],
    "lab":       ["", "", "", ""],
    "default":   ["", "", "", ""],
}

NICHE_DATA = {
    "dental": {
        "hero_label": "TRUSTED DENTAL CARE",
        "hero_title": "Modern Dentistry in {area}",
        "hero_text": "{name} provides exceptional dental services to the {area} community. Rated {rating} stars from {reviews} patient reviews — trusted care, gentle touch.",
        "services_heading": "Our Services",
        "services": [
            ("General Dentistry", "Cleanings, fillings, root canals & preventive care"),
            ("Cosmetic Dentistry", "Veneers, whitening & complete smile makeovers"),
            ("Orthodontics", "Braces & Invisalign for perfect alignment"),
            ("Emergency Care", "Same-day appointments for dental emergencies"),
        ],
        "featured_title": "New Patient Special",
        "featured_text": "First consultation + cleaning at a special rate. Experienced team, modern equipment, comfortable care.",
        "featured_cta": "Call to Book",
        "cta_title": "Ready for a healthier smile?",
        "cta_text": "Call or message us today. Walk-ins welcome.",
        "cta_button": "Book Appointment →",
        "gallery_heading": "Our Work",
    },
    "beauty": {
        "hero_label": "PREMIUM SALON",
        "hero_title": "Look & Feel Your Best in {area}",
        "hero_text": "{name} is {area}'s go-to destination for beauty and wellness. {rating} stars from {reviews} happy clients — because you deserve the best.",
        "services_heading": "What We Offer",
        "services": [
            ("Hair Styling", "Cuts, color, treatments & styling for all hair types"),
            ("Skin Care", "Facials, cleanups & advanced skin treatments"),
            ("Makeup Artistry", "Bridal, party & professional makeup"),
            ("Spa & Wellness", "Relaxing massages, body treatments & more"),
        ],
        "featured_title": "First-Time Client Offer",
        "featured_text": "Enjoy 20% off your first visit. Experience premium care from {area}'s top-rated beauty professionals.",
        "featured_cta": "Call to Reserve",
        "cta_title": "Book your glow-up",
        "cta_text": "Slots fill fast — message us to secure your appointment.",
        "cta_button": "Message on WhatsApp →",
        "gallery_heading": "Our Work",
    },
    "gym": {
        "hero_label": "FITNESS CENTER",
        "hero_title": "Transform at {area}'s Best Gym",
        "hero_text": "{name} helps {area} residents crush their fitness goals. {rating} stars from {reviews} members — real results, real community.",
        "services_heading": "Training Programs",
        "services": [
            ("Personal Training", "1-on-1 coaching tailored to your goals"),
            ("Group Classes", "Yoga, HIIT, Zumba & spin sessions"),
            ("Strength & Cardio", "Premium equipment for all levels"),
            ("Nutrition Plans", "Custom diet plans for better results"),
        ],
        "featured_title": "Free Trial Session",
        "featured_text": "Try us out — first session free. No commitment, just results.",
        "featured_cta": "Claim Free Trial",
        "cta_title": "Start your journey today",
        "cta_text": "Join {area}'s top fitness community.",
        "cta_button": "Get Started →",
        "gallery_heading": "Facility Tour",
    },
    "lab": {
        "hero_label": "DIAGNOSTIC CENTER",
        "hero_title": "Accurate Testing in {area}",
        "hero_text": "{name} delivers fast, reliable diagnostic results. {rating} stars from {reviews} patients — precision you can trust.",
        "services_heading": "Our Tests",
        "services": [
            ("Blood Work", "CBC, lipid profile, thyroid & more"),
            ("Pathology", "Tissue analysis & specialized testing"),
            ("Health Packages", "Full body checkups at affordable rates"),
            ("Home Collection", "Free sample pickup at your doorstep"),
        ],
        "featured_title": "Full Body Checkup — 999/-",
        "featured_text": "Complete health package including 60+ tests. Reports in 24 hours.",
        "featured_cta": "Book a Test",
        "cta_title": "Need a test today?",
        "cta_text": "Home collection available across {area}.",
        "cta_button": "Schedule Pickup →",
        "gallery_heading": "Our Facility",
    },
}

DEFAULT_DATA = {
    "hero_label": "LOCAL BUSINESS",
    "hero_title": "Professional Services in {area}",
    "hero_text": "{name} provides trusted services to the {area} community. {rating} stars from {reviews} client reviews — quality you can rely on.",
    "services_heading": "Services",
    "services": [
        ("Consultation", "Expert advice tailored to your needs"),
        ("Quality Work", "Professional service with attention to detail"),
        ("Support", "Dedicated help for all your questions"),
        ("Bookings", "Easy scheduling at your convenience"),
    ],
    "featured_title": "Why Choose Us?",
    "featured_text": "Rated {rating} stars by {reviews} clients. Trusted in {area} for quality service.",
    "featured_cta": "Call Us",
    "cta_title": "Get in touch",
    "cta_text": "We're here to help. Reach out anytime.",
    "cta_button": "Contact Us →",
    "gallery_heading": "Gallery",
}


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    return s.strip('-')


def detect_niche(name, category):
    text = f"{name} {category}".lower()
    if any(w in text for w in ['dental', 'dentist', 'smile', 'tooth', 'oral']):
        return 'dental'
    if any(w in text for w in ['salon', 'beauty', 'parlour', 'parlor', 'hair', 'spa', 'makeup', 'eyelash', 'barber', 'wig']):
        return 'beauty'
    if any(w in text for w in ['gym', 'fitness', 'health club', 'crossfit', 'yoga']):
        return 'gym'
    if any(w in text for w in ['lab', 'diagnostic', 'pathology', 'blood', 'test', 'xray', 'scan', 'diagnostics']):
        return 'lab'
    return 'default'


def compute_css_vars(accent_hex):
    """Derive light, dark, bg, text, text-light from accent hex."""
    # Simple lighten/darken via RGB manipulation
    hex_color = accent_hex.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    
    # Light: mix with white (90% white, 10% accent)
    rl = int(r * 0.10 + 255 * 0.90)
    gl = int(g * 0.10 + 255 * 0.90)
    bl = int(b * 0.10 + 255 * 0.90)
    accent_light = f"#{rl:02x}{gl:02x}{bl:02x}"
    
    # Dark: 70% of original
    rd = int(r * 0.70)
    gd = int(g * 0.70)
    bd = int(b * 0.70)
    accent_dark = f"#{rd:02x}{gd:02x}{bd:02x}"
    
    # BG: very light gray-white
    bg = "#fafafa"
    text = "#111111"
    text_light = "#666666"
    
    return {
        'accent': accent_hex,
        'accent_light': accent_light,
        'accent_dark': accent_dark,
        'bg': bg,
        'text': text,
        'text_light': text_light,
    }


def fill_template(html, r, nd, accent, css):
    """Fill all placeholders in any template."""
    area = (r['address'] or 'Mumbai').split(',')[0].strip()
    # Cleaner area extraction
    parts = (r['address'] or 'Mumbai').split(',')
    for p in parts:
        p = p.strip()
        if not p[0].isdigit() if p else False:
            pass  # keep scanning
    area = parts[0].strip()
    name_short = ' '.join(r['name'].split()[:3])
    rating = f"{r['rating']:.1f}" if r['rating'] else "4.5"
    reviews = str(r['reviews'] or 50)
    phone = re.sub(r'[^0-9]', '', r['phone'] or '')
    
    # Build services HTML (generic format, templates use CSS to style)
    services_html = '\n'.join(
        f'    <div class="service-card"><h3>{s[0]}</h3><p>{s[1]}</p></div>'
        for s in nd['services']
    )
    
    # CSS variables
    html = html.replace('{{ACCENT}}', css['accent'])
    html = html.replace('{{ACCENT_LIGHT}}', css['accent_light'])
    html = html.replace('{{ACCENT_DARK}}', css['accent_dark'])
    html = html.replace('{{BG}}', css['bg'])
    html = html.replace('{{TEXT}}', css['text'])
    html = html.replace('{{TEXT_LIGHT}}', css['text_light'])
    
    # Images (legacy, some templates still use these)
    for key in ['HERO_IMG1', 'HERO_IMG2', 'GALLERY_IMG1', 'GALLERY_IMG2', 'GALLERY_IMG3']:
        placeholder = '{{' + key + '}}'
        if placeholder in html:
            html = html.replace(placeholder, accent.get(key.lower(), ''))
    
    # Business data
    html = html.replace('{{CLINIC_NAME}}', r['name'])
    html = html.replace('{{CLINIC_NAME_SHORT}}', name_short)
    html = html.replace('{{CLINIC_ADDRESS}}', r['address'] or 'Mumbai')
    html = html.replace('{{RATING}}', rating)
    html = html.replace('{{REVIEWS}}', reviews)
    html = html.replace('{{AREA}}', area)
    html = html.replace('{{PHONE}}', phone)
    html = html.replace('{{PHONE_DISPLAY}}', phone[:10] if len(phone) >= 10 else phone)
    html = html.replace('{{YEARS_ACTIVE}}', '3')
    
    # Content blocks
    html = html.replace('{{HERO_LABEL}}', nd['hero_label'])
    html = html.replace('{{HERO_TITLE}}', nd['hero_title'].format(area=area))
    html = html.replace('{{HERO_TEXT}}', nd['hero_text'].format(name=r['name'], area=area, rating=rating, reviews=reviews))
    html = html.replace('{{SERVICES_HEADING}}', nd['services_heading'])
    html = html.replace('{{SERVICES_HTML}}', services_html)
    html = html.replace('{{FEATURED_TITLE}}', nd['featured_title'])
    html = html.replace('{{FEATURED_TEXT}}', nd['featured_text'].format(area=area, name=r['name'], rating=rating, reviews=reviews))
    html = html.replace('{{FEATURED_CTA}}', nd['featured_cta'])
    html = html.replace('{{CTA_TITLE}}', nd['cta_title'])
    html = html.replace('{{CTA_TEXT}}', nd['cta_text'].format(area=area))
    html = html.replace('{{CTA_BUTTON}}', nd['cta_button'])
    html = html.replace('{{GALLERY_HEADING}}', nd['gallery_heading'])
    
    return html


def main():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row

    rows = db.execute("""
        SELECT name, phone, address, rating, reviews, category
        FROM leads
        WHERE (website IS NULL OR website = '')
        AND phone IS NOT NULL AND phone != ''
        ORDER BY reviews DESC
    """).fetchall()

    generated = []
    template_counts = {}
    
    for r in rows:
        slug = slugify(r['name'])
        niche = detect_niche(r['name'], r['category'] or '')
        nd = NICHE_DATA.get(niche, DEFAULT_DATA)
        accent = NICHE_ACCENT.get(niche, NICHE_ACCENT["default"])
        css = compute_css_vars(accent['accent'])
        
        # Randomly pick a template
        template_file = random.choice(TEMPLATE_FILES)
        template_name = os.path.basename(template_file)
        template_counts[template_name] = template_counts.get(template_name, 0) + 1
        template = open(template_file).read()
        
        html = fill_template(template, r, nd, accent, css)

        # Write
        os.makedirs(f'{DEMOS}/{slug}', exist_ok=True)
        with open(f'{DEMOS}/{slug}/index.html', 'w') as f:
            f.write(html)
        generated.append((r['name'], slug, niche, template_name))

    print(f"Generated {len(generated)} demo sites")
    for name, slug, niche, tpl in generated[:10]:
        print(f"  [{niche:8s}] [{tpl.replace('template_','').replace('.html',''):20s}] {name[:40]:40s} → {slug}")
    if len(generated) > 10:
        print(f"  ... and {len(generated)-10} more")
    print(f"\nTemplate distribution: {template_counts}")


if __name__ == '__main__':
    main()
