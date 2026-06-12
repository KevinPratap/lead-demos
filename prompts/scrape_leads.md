# Task: Scrape Mumbai business leads via SerpAPI

## Goal
Scrape business names, phone numbers, and addresses from Google local search results for Mumbai businesses across multiple niches. Save results as JSON.

## API Key
SerpAPI key: `7e8fbacc1bfa5d0a1b162f596e734999342199bb11a1c0472771adf210e500e6`
Free tier: 100 searches/month. Use ~18 searches (one per query below).

## Search Queries (niche, query)
1. dental, "dental clinic in Andheri West Mumbai"
2. dental, "dentist in Vile Parle Mumbai"
3. salon, "beauty salon in Bandra Mumbai"
4. salon, "hair salon in Juhu Mumbai"
5. gym, "gym in Juhu Mumbai"
6. gym, "fitness center in Andheri Mumbai"
7. barber, "barber shop in Andheri Mumbai"
8. barber, "mens salon in Bandra Mumbai"
9. skin, "skin clinic in Bandra Mumbai"
10. skin, "dermatologist in Andheri Mumbai"
11. cafe, "cafe in Bandra Mumbai"
12. cafe, "coffee shop in Andheri Mumbai"
13. yoga, "yoga studio in Andheri Mumbai"
14. physio, "physiotherapy in Vile Parle Mumbai"
15. bakery, "bakery in Bandra Mumbai"
16. spa, "spa in Juhu Mumbai"
17. spa, "massage in Andheri Mumbai"
18. eyelash, "eyelash extension in Bandra Mumbai"

## What to extract per lead
- Business name
- Phone numbers (Indian format: +91XXXXXXXXXX, XXXXXXXXXX, etc.)
- Address (if available)
- Website URL (if available)
- Rating (if available)
- Source: "organic" (from search results) or "local" (from Google Maps local results)
- Niche tag
- Timestamp

## Skip/filter out
Aggregator sites: justdial, asklaila, practo, lybrate, magicpin, 5bestincity, cybo, yelp, tripadvisor, wikipedia, facebook, instagram, linkedin, youtube, reddit, quora, indiamart, tradeindia, exportersindia

## Output
Save to: `/home/prata/leads/data/serpapi_leads.json`
Format: JSON array of lead objects

## Deduplication
Deduplicate by business name (first 40 chars, case-insensitive) across all searches.

## Rate limiting
1.5 second delay between searches.

## Print progress
Show each niche query, leads found, and final summary with counts by niche.
