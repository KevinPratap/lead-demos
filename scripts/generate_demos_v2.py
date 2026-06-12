#!/usr/bin/env python3
"""Generate demo sites for ANY niche. Template adapts services based on category."""
import sqlite3, re, os, json

DB = "/home/prata/leads/data/leads.db"
DEMOS = "/home/prata/leads/demos"
TEMPLATE_FILE = "/home/prata/leads/scripts/template.html"

# Niche-specific service cards and hero text
NICHE_DATA = {
    "default": {
        "hero_title": "Professional Services in {area}",
        "hero_text": "{name} provides trusted services to the {area} community. Rated {rating} stars from {reviews} client reviews.",
        "services": [
            ("Consultation", "Expert advice tailored to your specific needs."),
            ("Quality Service", "Professional care with attention to detail."),
            ("Customer Support", "Dedicated support for all your questions."),
            ("Bookings", "Easy appointment scheduling at your convenience."),
        ]
    },
    "dental": {
        "hero_title": "Modern Dental Care in {area}",
        "hero_text": "{name} provides exceptional dental services to the {area} community. {rating} stars from {reviews} patient reviews.",
        "services": [
            ("General Dentistry", "Cleanings, fillings, root canals, and preventive care."),
            ("Cosmetic Dentistry", "Veneers, whitening, and smile makeovers."),
            ("Orthodontics", "Braces and Invisalign for perfect alignment."),
            ("Emergency Care", "Same-day appointments for dental emergencies."),
        ]
    },
    "beauty": {
        "hero_title": "Premium Beauty Services in {area}",
        "hero_text": "{name} offers top-rated beauty and salon services in {area}. {rating} stars from {reviews} happy clients.",
        "services": [
            ("Hair Styling", "Cuts, color, treatments, and styling for all hair types."),
            ("Skin Care", "Facials, cleanups, and advanced skin treatments."),
            ("Makeup", "Bridal, party, and professional makeup services."),
            ("Spa Treatments", "Relaxing massages and wellness therapies."),
        ]
    },
    "gym": {
        "hero_title": "Fitness & Training in {area}",
        "hero_text": "{name} helps {area} residents achieve their fitness goals. {rating} stars from {reviews} member reviews.",
        "services": [
            ("Personal Training", "One-on-one coaching tailored to your goals."),
            ("Group Classes", "Yoga, HIIT, Zumba, and spin classes."),
            ("Cardio & Weights", "Modern equipment for all fitness levels."),
            ("Nutrition Plans", "Customized diet plans for better results."),
        ]
    },
    "lab": {
        "hero_title": "Diagnostic Services in {area}",
        "hero_text": "{name} provides accurate and timely diagnostic testing in {area}. {rating} stars from {reviews} patient reviews.",
        "services": [
            ("Blood Tests", "Complete blood count, lipid profile, and more."),
            ("Pathology", "Tissue analysis and specialized pathology services."),
            ("Health Packages", "Full body checkup packages at affordable rates."),
            ("Home Collection", "Sample collection from the comfort of your home."),
        ]
    },
}

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    return s.strip('-')

def detect_niche(name, category):
    """Map lead to niche type based on name/category."""
    text = f"{name} {category}".lower()
    if any(w in text for w in ['dental', 'dentist', 'smile', 'tooth', 'oral']):
        return 'dental'
    if any(w in text for w in ['salon', 'beauty', 'parlour', 'parlor', 'hair', 'spa', 'makeup']):
        return 'beauty'
    if any(w in text for w in ['gym', 'fitness', 'health club', 'crossfit', 'yoga']):
        return 'gym'
    if any(w in text for w in ['lab', 'diagnostic', 'pathology', 'blood', 'test', 'xray', 'scan']):
        return 'lab'
    return 'default'

def main():
    template = open(TEMPLATE_FILE).read()
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
    for r in rows:
        slug = slugify(r['name'])
        niche = detect_niche(r['name'], r['category'] or '')
        nd = NICHE_DATA.get(niche, NICHE_DATA['default'])
        
        area = (r['address'] or 'Mumbai').split(',')[0].strip()
        name_short = ' '.join(r['name'].split()[:3])
        rating = f"{r['rating']:.1f}" if r['rating'] else "4.5"
        reviews = str(r['reviews'] or 50)
        phone = re.sub(r'[^0-9]', '', r['phone'] or '')
        phone_display = f"+91 {phone[-10:-5]} {phone[-5:]}" if len(phone) >= 10 else (r['phone'] or '')
        
        # Build services HTML
        services_html = '\n'.join(
            f'<div class="service-card"><h3>{s[0]}</h3><p>{s[1]}</p></div>'
            for s in nd['services']
        )
        
        html = template
        html = html.replace('{{CLINIC_NAME}}', r['name'])
        html = html.replace('{{CLINIC_NAME_SHORT}}', name_short)
        html = html.replace('{{CLINIC_ADDRESS}}', r['address'] or 'Mumbai')
        html = html.replace('{{RATING}}', rating)
        html = html.replace('{{REVIEWS}}', reviews)
        html = html.replace('{{AREA}}', area)
        html = html.replace('{{PHONE}}', phone)
        html = html.replace('{{PHONE_DISPLAY}}', phone_display)
        html = html.replace('{{YEARS_ACTIVE}}', '3')
        
        # Replace hero text
        hero_title = nd['hero_title'].format(area=area)
        hero_text = nd['hero_text'].format(name=r['name'], area=area, rating=rating, reviews=reviews)
        html = html.replace('<h1>Modern Dental Care in {{AREA}}</h1>', f'<h1>{hero_title}</h1>')
        html = html.replace('<p>{{CLINIC_NAME}} has been providing exceptional dental services', f'<p>{hero_text[:200]}')
        
        # Replace services section
        old_services_start = html.find('<div class="services">')
        old_services_end = html.find('</div>', html.find('<div class="cta">'))
        if old_services_start > 0 and old_services_end > 0:
            html = html[:old_services_start] + f'<div class="services">\n{services_html}\n</div>\n' + html[old_services_end+6:]
        
        # Write
        os.makedirs(f'{DEMOS}/{slug}', exist_ok=True)
        with open(f'{DEMOS}/{slug}/index.html', 'w') as f:
            f.write(html)
        generated.append((r['name'], slug, niche))
    
    print(f"Generated {len(generated)} demo sites")
    for name, slug, niche in generated[:5]:
        print(f"  {name[:40]} | {slug[:40]} | {niche}")
    print(f"  ... and {len(generated)-5} more")

if __name__ == '__main__':
    main()
