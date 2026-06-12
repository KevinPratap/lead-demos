#!/usr/bin/env python3
import os
import re
import sqlite3

TEMPLATE_PATH = "/home/prata/leads/scripts/template.html"
DB_PATH = "/home/prata/leads/data/leads.db"
OUTPUT_DIR = "/home/prata/leads/demos"

def generate_slug(name):
    if not name:
        return "unnamed"
    slug = name.lower()
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Strip leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def main():
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        return

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template_content = f.read()

    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query for leads matching the criteria
    query = """
        SELECT name, address, rating, reviews, phone 
        FROM leads 
        WHERE (website IS NULL OR website = '') 
          AND (phone IS NOT NULL AND phone != '')
    """
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.close()
        return

    generated_slugs = []

    for row in rows:
        name = row['name'] or ""
        address = row['address'] or ""
        rating = row['rating']
        reviews = row['reviews']
        phone = row['phone'] or ""

        # 1. Generate slug
        slug = generate_slug(name)
        if not slug:
            continue

        # 2. Compute placeholders
        # CLINIC_NAME_SHORT: first 2-3 words of name
        words = name.split()
        clinic_name_short = " ".join(words[:min(3, len(words))])

        # CLINIC_ADDRESS: address or empty
        clinic_address = address

        # RATING: rating or "5.0"
        rating_str = str(rating) if rating is not None and str(rating).strip() != "" else "5.0"

        # REVIEWS: reviews or "50"
        reviews_str = str(reviews) if reviews is not None and str(reviews).strip() != "" else "50"

        # AREA: first part of address before comma (or empty if address is empty)
        area = address.split(',')[0].strip() if address else ""

        # PHONE: raw phone digits only
        raw_phone = "".join(c for c in phone if c.isdigit())

        # PHONE_DISPLAY: phone with +91 formatting
        if len(raw_phone) >= 10:
            last_10 = raw_phone[-10:]
            phone_display = f"+91 {last_10}"
        else:
            phone_display = f"+91 {raw_phone}" if raw_phone else ""

        # Replace placeholders
        rendered = template_content
        rendered = rendered.replace("{{CLINIC_NAME}}", name)
        rendered = rendered.replace("{{CLINIC_NAME_SHORT}}", clinic_name_short)
        rendered = rendered.replace("{{CLINIC_ADDRESS}}", clinic_address)
        rendered = rendered.replace("{{RATING}}", rating_str)
        rendered = rendered.replace("{{REVIEWS}}", reviews_str)
        rendered = rendered.replace("{{AREA}}", area)
        rendered = rendered.replace("{{PHONE}}", raw_phone)
        rendered = rendered.replace("{{PHONE_DISPLAY}}", phone_display)
        rendered = rendered.replace("{{YEARS_ACTIVE}}", "3")

        # Write to output file
        lead_dir = os.path.join(OUTPUT_DIR, slug)
        os.makedirs(lead_dir, exist_ok=True)
        output_file = os.path.join(lead_dir, "index.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered)

        generated_slugs.append(slug)

    conn.close()

    # Print summary
    print(f"Generated {len(generated_slugs)} sites.")
    print("Slugs:")
    for slug in generated_slugs:
        print(f"  - {slug}")

if __name__ == "__main__":
    main()
