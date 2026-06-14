#!/usr/bin/env python3
import os
import re
import sqlite3
import json
import subprocess
import time
import datetime
import argparse

# Root and data directories
BASE_DIR = '/home/prata/leads'
DB_PATH = os.path.join(BASE_DIR, 'data/leads.db')
SENT_LOG_PATH = os.path.join(BASE_DIR, 'data/wa_sent.json')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'scripts/template.html')

def clean_phone(phone):
    if not phone:
        return ""
    digits = re.sub(r'[^0-9]', '', phone)
    if digits.startswith('0'):
        digits = digits[1:]
    if digits.startswith('91') and len(digits) > 10:
        return digits
    elif len(digits) == 10:
        return '91' + digits
    return digits

def classify_category(name, category):
    text = f"{name or ''} {category or ''}".lower()
    if any(w in text for w in ['dental', 'dentist', 'smile', 'tooth', 'oral', 'braces', 'orthodont', 'teeth']):
        return 'dental'
    if any(w in text for w in ['salon', 'parlour', 'parlor', 'hair', 'makeup', 'eyelash', 'barber', 'wig', 'beauty', 'dresser', 'nails']):
        return 'salon'
    if any(w in text for w in ['spa', 'massage', 'wellness', 'therap', 'aroma']):
        return 'spa'
    if any(w in text for w in ['gym', 'fitness', 'crossfit', 'workout', 'training center', 'club']):
        return 'gym'
    if any(w in text for w in ['yoga', 'meditation', 'aum', 'spirit']):
        return 'yoga'
    if any(w in text for w in ['physio', 'physiotherapy', 'chiropract', 'rehab', 'back pain', 'orthopedic', 'sports medicine']):
        return 'physio'
    # Default fallback
    if any(w in text for w in ['clinic', 'doctor', 'medical', 'health']):
        return 'dental'
    return 'salon'

def main():
    parser = argparse.ArgumentParser(description="Build and send web previews to leads.")
    parser.add_argument("--limit", type=int, default=200, help="Max number of leads to process.")
    args = parser.parse_args()
    max_leads = args.limit

    # Load template
    if not os.path.exists(TEMPLATE_PATH):
        print(f"Error: Template not found at {TEMPLATE_PATH}")
        return
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()

    # Load already sent leads from wa_sent.json
    sent_phones = set()
    sent_leads = set()
    if os.path.exists(SENT_LOG_PATH):
        try:
            with open(SENT_LOG_PATH, 'r', encoding='utf-8') as f:
                sent_data = json.load(f)
                for entry in sent_data:
                    p = clean_phone(entry.get('phone', ''))
                    if p:
                        sent_phones.add(p)
                    lead = entry.get('lead') or entry.get('business_name')
                    if lead:
                        sent_leads.add(lead.strip().lower())
        except Exception as e:
            print(f"Warning: could not parse wa_sent.json: {e}")

    # Fetch leads from leads.db
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    rows = cursor.execute("""
        SELECT name, phone, address, rating, reviews, category, image_url, image_urls, first_seen_at
        FROM leads
        WHERE (website IS NULL OR website = '')
        AND phone IS NOT NULL AND phone != ''
    """).fetchall()
    conn.close()

    # Filter out sent leads
    unsent_leads = []
    for row in rows:
        name = row['name']
        phone = row['phone']
        cleaned = clean_phone(phone)
        if cleaned in sent_phones or name.strip().lower() in sent_leads:
            continue
        unsent_leads.append(row)

    print(f"Found {len(unsent_leads)} unsent no-website leads.")

    # Premium theme colors and gradients for each category
    accents = {
        "dental": "#2563eb",
        "salon": "#db2777",
        "spa": "#c2410c",
        "gym": "#e11d48",
        "yoga": "#16a34a",
        "physio": "#0d9488"
    }
    accent_lights = {
        "dental": "#dbeafe",
        "salon": "#fce7f3",
        "spa": "#ffedd5",
        "gym": "#ffe4e6",
        "yoga": "#dcfce7",
        "physio": "#ccfbf1"
    }
    hero_gradients = {
        "dental": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
        "salon": "linear-gradient(135deg, #ec4899 0%, #be185d 100%)",
        "spa": "linear-gradient(135deg, #ea580c 0%, #b45309 100%)",
        "gym": "linear-gradient(135deg, #f43f5e 0%, #be123c 100%)",
        "yoga": "linear-gradient(135deg, #22c55e 0%, #15803d 100%)",
        "physio": "linear-gradient(135deg, #14b8a6 0%, #0f766e 100%)"
    }
    
    gradient_placeholders = {
        "dental": [
            "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1557683316-973673baf926?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=600&h=800&fit=crop"
        ],
        "salon": [
            "https://images.unsplash.com/photo-1528459801416-a9e53bbf4e17?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=600&h=800&fit=crop"
        ],
        "spa": [
            "https://images.unsplash.com/photo-1604871000636-074fa5117945?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600&h=800&fit=crop"
        ],
        "gym": [
            "https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1504198453319-5ce911bafcde?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&h=800&fit=crop"
        ],
        "yoga": [
            "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1618005198143-d5182384-a83a8bd57fbe?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=600&h=800&fit=crop"
        ],
        "physio": [
            "https://images.unsplash.com/photo-1554034483-04fda0d3507b?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1557683311-eac922347aa1?w=600&h=800&fit=crop",
            "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&h=800&fit=crop"
        ]
    }

    services_data = {
        "dental": [
            ("🦷", "General Dentistry", "Comprehensive checkups, cleanings, and fillings to keep your smile healthy."),
            ("✨", "Cosmetic Dentistry", "Transform your smile with professional whitening, veneers, and bonding."),
            ("😬", "Orthodontics", "Align your teeth beautifully with modern braces and clear Invisalign aligners."),
            ("🏥", "Dental Implants", "Permanent, natural-looking tooth replacements to restore your confidence."),
            ("⚡", "Emergency Care", "Same-day appointments for quick relief from sudden dental pain."),
            ("👶", "Pediatric Dentistry", "Gentle and friendly dental care designed specifically for children.")
        ],
        "salon": [
            ("✂️", "Hair Styling & Cuts", "Expert cuts, blowouts, and styling tailored to your unique look."),
            ("🎨", "Color & Highlights", "Transform your hair with balayage, highlights, or full color treatments."),
            ("💆‍♀️", "Hair Spa & Treatments", "Deep conditioning, keratin, and nourishing therapies for shiny hair."),
            ("💅", "Manicure & Pedicure", "Premium nail grooming, shaping, and gel polish application."),
            ("✨", "Facial & Skincare", "Rejuvenating facials and cleanups for a glowing, radiant complexion."),
            ("💄", "Professional Makeup", "Bridal, party, and event makeup by experienced artists.")
        ],
        "spa": [
            ("💆‍♂️", "Signature Massages", "Relaxing Swedish, deep tissue, or hot stone massage therapies."),
            ("🌿", "Aromatherapy", "Therapeutic massages using essential oils to soothe the mind and body."),
            ("🧖‍♀️", "Steam & Sauna", "Detoxify and refresh with our premium steam rooms and saunas."),
            ("🍯", "Body Scrubs & Wraps", "Exfoliating scrubs and hydrating wraps for soft, glowing skin."),
            ("🌸", "Ayurvedic Therapies", "Traditional wellness treatments to restore balance and vitality."),
            ("🕊️", "Couple's Retreat", "A shared wellness experience with side-by-side massage packages.")
        ],
        "gym": [
            ("🏋️‍♂️", "Strength Training", "Modern free weights, resistance machines, and dedicated lifting areas."),
            ("🏃‍♂️", "Cardio Zone", "Premium treadmills, ellipticals, and stationary bikes for endurance."),
            ("👥", "Personal Training", "One-on-one coaching and custom workout plans with certified trainers."),
            ("🔥", "HIIT & Functional", "High-intensity circuit training to maximize calorie burn and agility."),
            ("🥗", "Nutritional Guidance", "Personalized diet plans and expert advice to fuel your progress."),
            ("🚿", "Locker Rooms & Showers", "Clean, modern changing facilities with secure storage.")
        ],
        "yoga": [
            ("🧘‍♀️", "Hatha Yoga", "Classic, slow-paced physical postures and breathing exercises."),
            ("⚡", "Vinyasa Flow", "Dynamic, fluid classes synchronizing breath with movement."),
            ("🌸", "Yin & Restorative", "Gentle, deeply relaxing poses held longer to target deep tissues."),
            ("🌬️", "Pranayama & Breathwork", "Deep breathing techniques to reduce stress and boost energy."),
            ("🧠", "Mindfulness Meditation", "Guided sessions to cultivate mental clarity and inner peace."),
            ("🤰", "Prenatal Yoga", "Gentle, safe movements tailored to support expectant mothers.")
        ],
        "physio": [
            ("🏥", "Sports Physiotherapy", "Recovery, rehabilitation, and performance training for athletes."),
            ("🦴", "Orthopedic Rehab", "Post-surgery recovery and therapy for joint, bone, and muscle issues."),
            ("⚡", "Pain Management", "Focused treatments for chronic back pain, neck pain, and arthritis."),
            ("💆‍♂️", "Manual Therapy", "Hands-on joint and soft tissue mobilization to restore movement."),
            ("📈", "Posture Correction", "Assessment and exercises to correct alignment and prevent pain."),
            ("🏠", "Geriatric Care", "Specialized physical therapy to improve balance and mobility in seniors.")
        ]
    }

    featured_titles = {
        "dental": "Ready for a Healthier, Brighter Smile?",
        "salon": "Ready to Book Your Next Look?",
        "spa": "Ready to Escape and Unwind?",
        "gym": "Ready to Transform Your Fitness?",
        "yoga": "Ready to Begin Your Yoga Journey?",
        "physio": "Ready to Move Pain-Free Again?"
    }

    featured_texts = {
        "dental": "Get expert care from our friendly dental team. We offer comfortable treatments, modern facilities, and flexible scheduling.",
        "salon": "Experience premium styling, color, and nail care from our expert beauty professionals. Let us pamper you.",
        "spa": "Relax your mind and restore your body with our premium massage and aromatherapy packages. Book your wellness escape.",
        "gym": "Get access to premium workout equipment, custom training programs, and a supportive community. Start today.",
        "yoga": "Find balance and serenity. Our classes are open to all experience levels, from beginners to advanced practitioners.",
        "physio": "Receive customized, evidence-based therapy to relieve pain, restore mobility, and prevent future injuries."
    }

    cta_texts = {
        "dental": "Call or message us today to schedule your dental checkup.",
        "salon": "Slots fill fast! Message us on WhatsApp to book your styling slot.",
        "spa": "Reserve your massage or treatment today. Walk-ins subject to availability.",
        "gym": "Start your training program now. Contact us for membership details.",
        "yoga": "Reserve your mat space in our next session. We look forward to seeing you.",
        "physio": "Book your initial physical assessment and start your recovery today."
    }

    count = 0
    for row in unsent_leads:
        if count >= max_leads:
            break

        name = row['name']
        phone = row['phone']
        address = row['address']
        rating = row['rating']
        reviews = row['reviews']
        category = row['category']
        image_url = row['image_url']
        image_urls = row['image_urls']
        first_seen_at = row['first_seen_at']

        phone_val = clean_phone(phone)
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

        print(f"\n[{count + 1}/{min(len(unsent_leads), max_leads)}] Processing: {name} ({phone_val})")

        # Classify the category
        category_key = classify_category(name, category)

        # 1. Fill all template variables
        clinic_name_short = ' '.join(name.split()[:3])
        clinic_address = address if address else "Mumbai"
        rating_val = f"{rating:.1f}" if (rating is not None and rating != '') else "4.5"
        reviews_val = str(reviews) if (reviews is not None and reviews != '') else "100+"

        # Calculate years active
        years_active = '5'
        if first_seen_at:
            try:
                match = re.search(r'^(\d{4})', str(first_seen_at))
                if match:
                    year = int(match.group(1))
                    current_year = datetime.datetime.now().year
                    diff = current_year - year
                    years_active = str(diff) if diff > 0 else '5'
            except Exception:
                pass

        hero_label = category if (category and category.strip()) else {
            "dental": "Dental Clinic",
            "salon": "Beauty Salon",
            "spa": "Luxury Spa",
            "gym": "Fitness Center",
            "yoga": "Yoga Studio",
            "physio": "Physiotherapy Clinic"
        }.get(category_key, "Premium Service")

        # Dynamic compelling headline
        if category_key == 'dental':
            hero_title = f"Your Smile is Our Passion at {name}"
        elif category_key == 'salon':
            hero_title = f"Unlock Your Signature Look at {name}"
        elif category_key == 'spa':
            hero_title = f"Rejuvenate Your Mind & Body at {name}"
        elif category_key == 'gym':
            hero_title = f"Crush Your Fitness Goals at {name}"
        elif category_key == 'yoga':
            hero_title = f"Find Your Inner Peace and Strength at {name}"
        elif category_key == 'physio':
            hero_title = f"Live Pain-Free and Restore Movement at {name}"
        else:
            hero_title = f"Premium Professional Services at {name}"

        # Dynamic compelling description
        rating_str = f"{rating_val} ★"
        reviews_str = f"{reviews_val} reviews"
        if category_key == 'dental':
            hero_text = f"We provide top-rated dental care to help you achieve a healthy, beautiful smile. Trusted by local patients with {rating_str} from {reviews_str}."
        elif category_key == 'salon':
            hero_text = f"Indulge in premium hair, skin, and beauty services tailored just for you. Highly recommended with {rating_str} from {reviews_str}."
        elif category_key == 'spa':
            hero_text = f"Escape the stress of daily life with our soothing therapies and wellness treatments. Peaceful relaxation rated {rating_str} by {reviews_str} clients."
        elif category_key == 'gym':
            hero_text = f"Join our vibrant community and state-of-the-art facility to achieve your ultimate fitness goals. Rated {rating_str} by {reviews_str} active members."
        elif category_key == 'yoga':
            hero_text = f"Discover harmony, flexibility, and strength through our expert-led yoga and meditation classes. Highly rated with {rating_str} from {reviews_str} practitioners."
        elif category_key == 'physio':
            hero_text = f"Get back to doing what you love with our specialized physical rehabilitation and therapy programs. Rated {rating_str} based on {reviews_str} recoveries."
        else:
            hero_text = f"We deliver high-quality professional services tailored to your needs. Highly recommended by clients with {rating_str} from {reviews_str}."

        services_heading = 'Our Services'

        # Generate service cards HTML
        cards = services_data.get(category_key, services_data['salon'])
        services_html_parts = []
        for icon, s_name, s_desc in cards:
            card_html = f"""    <div class="service-card">
      <div class="service-icon">{icon}</div>
      <h3>{s_name}</h3>
      <p>{s_desc}</p>
    </div>"""
            services_html_parts.append(card_html)
        services_html = "\n".join(services_html_parts)

        gallery_heading = 'Gallery'

        # Featured details
        featured_title = featured_titles.get(category_key, "Ready to Take the Next Step?")
        featured_text = featured_texts.get(category_key, f"Experience premium service tailored to your needs. Connect with our team of experts today.")
        featured_cta = 'Call Now'

        # Bottom CTA details
        cta_title = 'Ready to get started?'
        cta_text = cta_texts.get(category_key, "Get in touch with us to schedule an appointment or ask any questions.")
        cta_button = 'Book Appointment'

        accent = accents.get(category_key, "#db2777")
        accent_light = accent_lights.get(category_key, "#fce7f3")
        hero_gradient = hero_gradients.get(category_key, "linear-gradient(135deg, #ec4899 0%, #be185d 100%)")

        # Compile gallery images
        fallbacks = gradient_placeholders.get(category_key, gradient_placeholders["salon"])
        db_imgs = []
        if image_url:
            db_imgs.append(image_url)
        if image_urls:
            try:
                urls = [u.strip() for u in image_urls.split(',') if u.strip()]
                for u in urls:
                    if u not in db_imgs:
                        db_imgs.append(u)
            except Exception:
                pass

        gallery_imgs = []
        for u in db_imgs:
            if len(gallery_imgs) < 3:
                gallery_imgs.append(f"url('{u}')")
        for fb in fallbacks:
            if len(gallery_imgs) < 3:
                gallery_imgs.append(f"url('{fb}')")

        gallery_img1 = gallery_imgs[0]
        gallery_img2 = gallery_imgs[1]
        gallery_img3 = gallery_imgs[2]

        # Substitute in template
        html = template
        html = html.replace('{{CLINIC_NAME_SHORT}}', clinic_name_short)
        html = html.replace('{{CLINIC_ADDRESS}}', clinic_address)
        html = html.replace('{{RATING}}', rating_val)
        html = html.replace('{{REVIEWS}}', reviews_val)
        html = html.replace('{{YEARS_ACTIVE}}', years_active)
        html = html.replace('{{HERO_LABEL}}', hero_label)
        html = html.replace('{{HERO_TITLE}}', hero_title)
        html = html.replace('{{HERO_TEXT}}', hero_text)
        html = html.replace('{{SERVICES_HEADING}}', services_heading)
        html = html.replace('{{SERVICES_HTML}}', services_html)
        html = html.replace('{{GALLERY_HEADING}}', gallery_heading)
        html = html.replace('{{FEATURED_TITLE}}', featured_title)
        html = html.replace('{{FEATURED_TEXT}}', featured_text)
        html = html.replace('{{FEATURED_CTA}}', featured_cta)
        html = html.replace('{{CTA_TITLE}}', cta_title)
        html = html.replace('{{CTA_TEXT}}', cta_text)
        html = html.replace('{{CTA_BUTTON}}', cta_button)
        html = html.replace('{{CLINIC_NAME}}', name)
        html = html.replace('{{ACCENT}}', accent)
        html = html.replace('{{ACCENT_LIGHT}}', accent_light)
        html = html.replace('{{HERO_GRADIENT}}', hero_gradient)
        html = html.replace('{{GALLERY_IMG1}}', gallery_img1)
        html = html.replace('{{GALLERY_IMG2}}', gallery_img2)
        html = html.replace('{{GALLERY_IMG3}}', gallery_img3)
        html = html.replace('{{PHONE}}', phone_val)
        html = html.replace('{{SLUG}}', slug)
        html = html.replace('{{NAME}}', name)

        # Defensive replacement: strip any remaining placeholder tags to guarantee compliance
        remaining = re.findall(r'\{\{[A-Za-z0-9_]+\}\}', html)
        if remaining:
            print(f"Warning: Cleaning remaining placeholders {remaining}")
            for p in remaining:
                html = html.replace(p, "")

        # 2. Write the filled HTML to demos/{slug}/index.html
        demo_dir = os.path.join(BASE_DIR, 'demos', slug)
        os.makedirs(demo_dir, exist_ok=True)
        index_path = os.path.join(demo_dir, 'index.html')
        try:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Wrote demo to {index_path}")
        except Exception as e:
            print(f"Error writing index.html for {name}: {e}")
            continue

        # 3. Git add, commit, push
        git_success = False
        try:
            # git add
            subprocess.run(['git', 'add', f'demos/{slug}/index.html'], check=True, cwd=BASE_DIR, capture_output=True)
            # git commit
            subprocess.run(['git', 'commit', '-m', f"Add demo for {name}"], check=True, cwd=BASE_DIR, capture_output=True)
            # git push
            subprocess.run(['git', 'push'], check=True, cwd=BASE_DIR, capture_output=True)
            git_success = True
            print("Git add, commit, push completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Git operation failed for {name}: {e.stderr.decode('utf-8', errors='ignore').strip()}")
        except Exception as e:
            print(f"Git operation threw exception: {e}")

        # 4. Wait 20 seconds for GitHub Pages
        print("Waiting 20 seconds for GitHub Pages deployment...")
        time.sleep(20)

        # 5. Send WhatsApp message with the demo URL using node scripts/send_whatsapp.js
        demo_url = f"https://kevinpratap.github.io/lead-demos/{slug}/"
        cmd = ['node', 'scripts/send_whatsapp.js', '--lead', name, '--url', demo_url]
        print(f"Sending WhatsApp message...")
        success = False
        try:
            res = subprocess.run(cmd, timeout=60, cwd=BASE_DIR, capture_output=True, text=True)
            print(res.stdout)
            if res.stderr:
                print(res.stderr)
            success = (res.returncode == 0) and ("✅ Message sent!" in res.stdout)
        except subprocess.TimeoutExpired:
            print("Error: WhatsApp sending timed out after 60s.")
        except Exception as e:
            print(f"Error executing send_whatsapp.js: {e}")

        # Log to wa_sent.json
        try:
            log_entries = []
            if os.path.exists(SENT_LOG_PATH):
                with open(SENT_LOG_PATH, 'r', encoding='utf-8') as f:
                    log_entries = json.load(f)

            already_logged = False
            for entry in reversed(log_entries[-3:]):
                if clean_phone(entry.get('phone')) == phone_val:
                    already_logged = True
                    break

            if not already_logged:
                new_entry = {
                    "phone": phone_val,
                    "lead": name,
                    "message": f"Demo url: {demo_url}",
                    "sent_at": datetime.datetime.utcnow().isoformat() + "Z",
                    "success": success
                }
                log_entries.append(new_entry)
                with open(SENT_LOG_PATH, 'w', encoding='utf-8') as f:
                    json.dump(log_entries, f, indent=2)
                print("Appended log entry to wa_sent.json")
        except Exception as e:
            print(f"Error updating wa_sent.json: {e}")

        count += 1

if __name__ == '__main__':
    main()
