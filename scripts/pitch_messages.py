"""Generate per-lead WhatsApp and Call scripts.

These are baked into the pitch sheet so Kevin opens one file,
grabs the script, and goes — no thinking required.
"""

from __future__ import annotations


def whatsapp(lead: dict) -> str:
    """WhatsApp message — copy-paste ready. {demo_url} = fill after building."""
    name = lead.get("name", "[Business Name]")
    phone = lead.get("phone") or ""
    rating = lead.get("rating") or 0
    address = lead.get("address") or ""
    category = lead.get("category", "business")

    stars = "⭐" * min(5, round(rating)) if rating else ""

    return (
        f"Hi, this is Kevin — web developer based in Mumbai. "
        f"I came across {name} on Google Maps "
        f"({' '.join(address.split()[:3])}...) and noticed you don't have a website. "
        f"You've got great reviews ({rating}★ {stars}) so I built a quick preview website "
        f"using your Google profile details. No commitment — just wanted to show you what's possible. "
        f"30 seconds to look: {{demo_url}}"
    )


def call_script(lead: dict) -> str:
    """Condensed call script — read from this while dialing."""
    name = lead.get("name", "the business")
    rating = lead.get("rating") or 0
    phone = lead.get("phone") or "their number"
    address = lead.get("address") or "their area"
    category = lead.get("category", "business")

    # Pick a service verb based on category
    service_verb = _service_verb(category)

    return (
        f"📞 CALL {name} — {phone}\n"
        f"\n"
        f"OPENING: Hi, is this {name}? Can I speak with the owner/doctor?\n"
        f"\n"
        f"HOOK: I'm Kevin, web developer. Found you on Google Maps — "
        f"{rating}★, {address.split(',')[0] if address else 'great reviews'}. "
        f"Noticed you don't have a website. I actually built a preview for {name} "
        f"already — can I send the link? Takes 10 seconds to look.\n"
        f"\n"
        f"[SEND WHATSAPP WITH DEMO LINK NOW]\n"
        f"\n"
        f"AFTER THEY LOOK: I can finish this properly — custom photos of your "
        f"actual {category}, your real {service_verb}, your own domain. "
        f"If you like it, I can have it live within a week.\n"
        f"\n"
        f"PRICING (only if asked): ₹10,000 flat for the complete site — "
        f"custom design, domain, hosting included for first year.\n"
        f"\n"
        f"OBJECTIONS:\n"
        f"• 'No need / word of mouth' → That's WHY you should have one. "
        f"When they Google you, they find {rating}★ but no site. "
        f"This turns searches into booked appointments.\n"
        f"• 'Too expensive' → 2 new patients from this site covers it. "
        f"Can split into 2 payments.\n"
        f"• 'Let me think' → Of course. Link stays live — share with staff. "
        f"I'll follow up in 3 days."
    )


def _slug(lead: dict) -> str:
    """Generate a folder-safe slug from business name."""
    name = lead.get("name", "business")
    slug = name.lower().replace("'", "").replace(".", "").replace(",", "")
    return slug.replace(" ", "-").replace("--", "-").replace("(", "").replace(")", "").strip("-")


def antigravity(lead: dict) -> str:
    """Generate a copy-paste Antigravity prompt that builds the demo site from Maps data."""
    name = lead.get("name", "[Business]")
    maps = lead.get("google_url", "")
    category = lead.get("category", "business")
    slug = _slug(lead)

    return (
        f"Build a single-page website for this business. Folder name: leads/{slug}\n\n"
        f"Business name: {name}\n"
        f"Google Maps profile: {maps}\n\n"
        f"Requirements:\n"
        f"1. Read the Google Maps profile and extract: phone, address, hours, rating, "
        f"reviews count, category ({category}), services, photos.\n"
        f"2. Create leads/{slug}/index.html with embedded CSS. Pure HTML+CSS, "
        f"fully responsive. No JS frameworks.\n"
        f"3. Structure: Top nav with business name + phone (clickable tel: link) + "
        f"\"Get Directions\" linking to the Maps URL above. Hero with H1, "
        f"rating badge, tagline. About section with 2-3 paragraphs. "
        f"Services grid. Why choose us section. Hours table. Contact section "
        f"with embedded Maps iframe. Footer with \"Demo by Kevin\" credit.\n"
        f"4. Use photos from their Maps profile if available. Fallback: gradients.\n"
        f"5. Premium clean design — system font stack, generous whitespace, single accent "
        f"color. Think Stripe/Linear aesthetic, NOT generic AI slop.\n"
        f"6. No git commit. Just the file."
    )


def _service_verb(category: str) -> str:
    cat = category.lower()
    if "dent" in cat:
        return "services and pricing"
    if "cafe" in cat or "restaurant" in cat:
        return "menu and hours"
    if "salon" in cat or "spa" in cat:
        return "treatments and pricing"
    if "gym" in cat or "fitness" in cat:
        return "classes and membership"
    if "clinic" in cat or "hospital" in cat or "doctor" in cat:
        return "treatments and hours"
    return "services and contact details"
