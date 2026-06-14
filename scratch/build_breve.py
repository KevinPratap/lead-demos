#!/usr/bin/env python3
import os
import re

TEMPLATE_PATH = "/home/prata/leads/scripts/template.html"
OUTPUT_PATH = "/home/prata/leads/demos/breve-bakery/index.html"

def main():
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Define replacements
    replacements = {
        "{{CLINIC_NAME}}": "Brevé Bakery",
        "{{CLINIC_NAME_SHORT}}": "Brevé Bakery",
        "{{CLINIC_ADDRESS}}": "Fresh breads, cakes & pastries daily",
        "{{ACCENT}}": "#a0522d",
        "{{ACCENT_LIGHT}}": "#f0ddd0",
        "{{RATING}}": "4.0",
        "{{REVIEWS}}": "808",
        "{{YEARS_ACTIVE}}": "5",
        "{{HERO_LABEL}}": "Neighbourhood Bakery",
        "{{HERO_TITLE}}": "Brevé Bakery",
        "{{HERO_TEXT}}": "Your neighbourhood bakery. Fresh bread every morning, custom cakes for every occasion, and pastries that make your evening walk worth it.",
        "{{SERVICES_HEADING}}": "Our Specialities",
        "{{GALLERY_HEADING}}": "Bakery Gallery",
        "{{GALLERY_IMG1}}": "url('https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&q=80')",
        "{{GALLERY_IMG2}}": "url('https://images.unsplash.com/photo-1556217477-d325251ece38?w=400&q=80')",
        "{{GALLERY_IMG3}}": "url('https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&q=80')",
        "{{FEATURED_TITLE}}": "Custom Cakes & Catering",
        "{{FEATURED_TEXT}}": "Let us make your next event special. We specialize in custom cakes and catering orders for parties and get-togethers.",
        "{{FEATURED_CTA}}": "Call +91 90825 87137",
        "{{PHONE}}": "+91 90825 87137",
        "{{CTA_TITLE}}": "Order Now",
        "{{CTA_TEXT}}": "To order custom cakes or reserve daily bakery items, send us a message on WhatsApp.",
        "{{CTA_BUTTON}}": "Message on WhatsApp",
    }

    # Perform standard replacements
    for key, val in replacements.items():
        html = html.replace(key, val)

    # Replace Hero Gradient and add background properties for hero banner
    old_hero_banner = """  .hero-banner {
    width: 100%;
    height: 220px;
    border-radius: var(--radius);
    background: {{HERO_GRADIENT}};
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
  }"""
  
    new_hero_banner = """  .hero-banner {
    width: 100%;
    height: 220px;
    border-radius: var(--radius);
    background: linear-gradient(135deg, rgba(160, 82, 45, 0.45) 0%, rgba(200, 120, 74, 0.65) 100%), url('https://images.unsplash.com/photo-1486427944544-d2c246c4df4e?w=800&q=80');
    background-size: cover;
    background-position: center;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
  }"""
    
    html = html.replace(old_hero_banner, new_hero_banner)
    # Just in case the formatting in the template file was slightly different
    html = html.replace("background: {{HERO_GRADIENT}};", "background: linear-gradient(135deg, rgba(160, 82, 45, 0.45) 0%, rgba(200, 120, 74, 0.65) 100%), url('https://images.unsplash.com/photo-1486427944544-d2c246c4df4e?w=800&q=80');\n    background-size: cover;\n    background-position: center;")

    # Services HTML
    services_html = """    <div class="service-card">
      <div class="service-icon">🥖</div>
      <h3>Fresh Daily Bread</h3>
      <p>Warm, crusty, and baked fresh every single morning using traditional recipes.</p>
    </div>
    <div class="service-card">
      <div class="service-icon">🎂</div>
      <h3>Custom Birthday Cakes</h3>
      <p>Handcrafted cakes customized for your special celebrations and milestones.</p>
    </div>
    <div class="service-card">
      <div class="service-icon">🥐</div>
      <h3>Pastries & Muffins</h3>
      <p>Delicious sweet treats, flaky croissants, and soft muffins baked daily.</p>
    </div>
    <div class="service-card">
      <div class="service-icon">☕</div>
      <h3>Tea & Coffee</h3>
      <p>The perfect pairing for your favourite baked goods, brewed to perfection.</p>
    </div>
    <div class="service-card">
      <div class="service-icon">🛍️</div>
      <h3>Catering Orders</h3>
      <p>Delight your guests with our customized platters of baked delights.</p>
    </div>
    <div class="service-card">
      <div class="service-icon">🛵</div>
      <h3>Home Delivery</h3>
      <p>Freshly baked goodness delivered right to your doorstep across Mumbai.</p>
    </div>"""
    
    html = html.replace("{{SERVICES_HTML}}", services_html)

    # Let's insert the Visit Us section before the Featured Strip
    visit_us_html = """  <!-- Visit Us -->
  <div class="services-heading">Visit Us</div>
  <div class="services-grid" style="grid-template-columns: 1fr; margin-bottom: 48px;">
    <div class="service-card" style="text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px;">
      <div class="service-icon">📍</div>
      <h3>Location & Hours</h3>
      <p style="color: var(--text); font-weight: 500;">Mumbai, Maharashtra, India</p>
      <p>Mon-Sat: 7am-9pm | Sun: 8am-6pm</p>
      <p style="color: var(--accent); font-weight: 600; margin-top: 4px;">Phone: +91 90825 87137</p>
    </div>
  </div>

  <!-- Dark Featured Strip (from B1) -->"""
    
    html = html.replace("<!-- Dark Featured Strip (from B1) -->", visit_us_html)

    # Let's replace the link for the bottom CTA to point to the bakery's WhatsApp
    html = html.replace('href="https://wa.me/918828022624" class="btn-primary"', 'href="https://wa.me/919082587137" class="btn-primary"')

    # Include Google Font 'Inter' in head
    font_links = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">"""
    
    html = html.replace("<head>", f"<head>\n{font_links}")
    
    # Change font-family in body style
    html = html.replace("font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;", "font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;")

    # Remove all em-dashes and exclamation marks and any left-over {{}} from the entire text.
    # Note: DOCTYPE needs to keep <!
    # But let's check for any general '!' or '—'.
    # We will replace em-dash '—' with a simple hyphen '-'
    html = html.replace("—", "-")
    
    # Replace other stylized comments dashes like '──' with '--' to be completely clean
    html = html.replace("──", "--")

    # Double check if there are any remaining {{ or }} placeholders
    matches = re.findall(r"\{\{[A-Za-z0-9_]+\}\}", html)
    if matches:
        print(f"Warning: Found remaining placeholders: {matches}")
        for m in matches:
            html = html.replace(m, "")

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully generated website at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
