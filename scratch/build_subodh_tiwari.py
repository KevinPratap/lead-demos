import os
import re

TEMPLATE_PATH = "/home/prata/leads/scripts/template.html"
OUTPUT_PATH = "/home/prata/leads/demos/subodh-tiwari/index.html"

def main():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Font Inter replacement:
    # Add Google Fonts link in head
    font_links = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">"""
    
    content = content.replace("</head>", f"{font_links}\n</head>")
    
    # Change body font-family to Inter
    content = content.replace(
        "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;",
        "font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;"
    )

    # 2. Layout adjustments:
    # change services-grid to 3 columns on desktop
    content = content.replace(
        "grid-template-columns: repeat(2, 1fr);",
        "grid-template-columns: repeat(3, 1fr);"
    )
    # change mobile services-grid to 1 column for better layout of 6 services on narrow screens
    content = content.replace(
        ".services-grid { grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 36px; }",
        ".services-grid { grid-template-columns: 1fr; gap: 12px; margin-bottom: 36px; }"
    )

    # 3. Replace all placeholders
    replacements = {
        "{{CLINIC_NAME}}": "Subodh Tiwari",
        "{{CLINIC_NAME_SHORT}}": "Subodh Tiwari",
        "{{CLINIC_ADDRESS}}": "Premium salon &amp; grooming in Mumbai",
        "{{ACCENT}}": "#2c3e50",
        "{{ACCENT_LIGHT}}": "#d5dce5",
        "{{HERO_GRADIENT}}": "linear-gradient(135deg, rgba(44, 62, 80, 0.55) 0%, rgba(74, 98, 120, 0.55) 100%), url('https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=800&q=80') center/cover no-repeat",
        "{{GALLERY_IMG1}}": "url('https://images.unsplash.com/photo-1599351431202-1e0f0137899a?w=400&q=80') center/cover no-repeat",
        "{{GALLERY_IMG2}}": "url('https://images.unsplash.com/photo-1562322140-8baeececf3df?w=400&q=80') center/cover no-repeat",
        "{{GALLERY_IMG3}}": "url('https://images.unsplash.com/photo-1560750588-73207b1ef5b8?w=400&q=80') center/cover no-repeat",
        "{{RATING}}": "5.0",
        "{{REVIEWS}}": "621",
        "{{YEARS_ACTIVE}}": "5",
        "{{HERO_LABEL}}": "Premium Grooming",
        "{{HERO_TITLE}}": "Subodh Tiwari",
        "{{HERO_TEXT}}": "5-star rated salon. Great haircuts, proper grooming, and service that keeps people coming back. Book your slot today.",
        "{{SERVICES_HEADING}}": "Our Premium Services",
        "{{SERVICES_HTML}}": """<div class="service-card">
      <div class="service-icon">✂️</div>
      <h3>Haircuts &amp; Styling</h3>
      <p>Precision haircuts, classic trims, and modern styling tailored to your look.</p>
    </div>
    <div class="service-card">
      <div class="service-icon">🧔</div>
      <h3>Beard Grooming</h3>
      <p>Expert beard trimming, shaping, and hot towel shaves for a sharp appearance.</p>
    </div>
    <div class="service-card">
      <div class="service-icon">🎨</div>
      <h3>Hair Color</h3>
      <p>Premium hair coloring and highlights using safe, long-lasting products.</p>
    </div>
    <div class="service-card">
      <div class="service-icon">💆</div>
      <h3>Facial &amp; Cleanup</h3>
      <p>Rejuvenating skin treatments, facials, and cleanups to refresh your face.</p>
    </div>
    <div class="service-card">
      <div class="service-icon">👦</div>
      <h3>Kids Haircut</h3>
      <p>Friendly and gentle haircuts for kids in a comfortable, patient environment.</p>
    </div>
    <div class="service-card">
      <div class="service-icon">🏠</div>
      <h3>Home Visits</h3>
      <p>Enjoy our premium grooming services from the comfort of your own home.</p>
    </div>""",
        "{{GALLERY_HEADING}}": "Our Work",
        "{{FEATURED_TITLE}}": "Experience Premium Grooming",
        "{{FEATURED_TEXT}}": "Top-rated haircuts, styling, and grooming services in Mumbai. Book your visit or contact us today.",
        "{{PHONE}}": "+919318388531",
        "{{FEATURED_CTA}}": "Call +91 93183 88531",
        "{{CTA_TITLE}}": "Book Your Appointment",
        "{{CTA_TEXT}}": "Located in Mumbai, Maharashtra. Open Mon-Sat: 9am-8pm | Sun: 10am-6pm.",
        "{{CTA_BUTTON}}": "Book via WhatsApp"
    }

    for placeholder, replacement in replacements.items():
        content = content.replace(placeholder, replacement)

    # 4. Clean up comments that might have em-dashes
    content = content.replace("B4 — secondary CTA", "B4 secondary CTA")
    content = content.replace("Mobile: 428px and below", "Mobile 428px and below")
    content = content.replace("Header ──", "Header")
    content = content.replace("Stats row ──", "Stats row")
    content = content.replace("Hero Banner ──", "Hero Banner")
    content = content.replace("Hero ──", "Hero")
    content = content.replace("Gallery Strip ──", "Gallery Strip")
    content = content.replace("Services Grid ──", "Services Grid")
    content = content.replace("Featured Strip (dark) ──", "Featured Strip (dark)")
    content = content.replace("CTA ──", "CTA")
    content = content.replace("Footer ──", "Footer")
    content = content.replace("Tiny phones: 374px and below", "Tiny phones 374px and below")

    # Remove all HTML comments (e.g., <!-- comment -->)
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)

    # Clean up multiple consecutive newlines / blank lines
    content = re.sub(r"\n\s*\n", "\n\n", content)

    # Replace any other em-dashes (— or –) or en-dashes
    content = content.replace("—", "-")
    content = content.replace("–", "-")
    
    if "{{" in content or "}}" in content:
        raise ValueError("Double curly braces remain in the output!")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Successfully built subodh-tiwari website preview.")

if __name__ == "__main__":
    main()
