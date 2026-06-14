# Task: Build Instagram Theme Page Automation System

## Goal
Build a fully automated system that runs Instagram theme pages. Content is scraped from Reddit daily, processed, and posted automatically. System runs via cron jobs with minimal human input.

## Architecture

### Phase 1: Content Scraper
- Scrape Reddit for trending posts in specific niches
- Download images from posts
- Clean filenames, resize if needed
- Store in organized folders

### Phase 2: Caption Generator  
- AI-generated captions using the post title as input
- Hashtag research (scrape trending hashtags)
- Different caption styles per niche (funny, motivational, informative)

### Phase 3: Post Scheduler
- Queue system for posts
- Post 1-3 times per day at optimal hours (9AM, 1PM, 7PM IST)
- Don't post duplicate content
- Keep a log of what's been posted

### Phase 4: Instagram Posting
- Meta Graph API integration
- Facebook App + Instagram Business account required
- Auto-post images with captions

## Niches to Set Up (start with 2)
1. **Mumbai Food** (@mumbaifoodcravers) — restaurant pics, street food
2. **Student Motivation** (@thegrindset.in) — quotes, study tips, grind culture

## Directory Structure
```
/home/prata/instagram-automation/
├── config.yaml           # API keys, niches, posting schedule
├── content/
│   ├── mumbai-food/      # Downloaded images
│   └── student-motivation/
├── posted/               # Log of posted content (avoid duplicates)
├── queue/                # Posts queued for tomorrow
├── scripts/
│   ├── scrape_reddit.py  # Fetch + download from Reddit
│   ├── generate_captions.py  # AI captions + hashtags
│   ├── post_to_ig.py     # Post via Meta Graph API
│   └── daily_run.py      # Orchestrator
└── data/
    ├── posted_log.json   # Tracking
    └── queue.json        # Tomorrow's posts
```

## Reddit Scraper
- Use Reddit's public JSON API (no auth needed for read-only)
- URL format: https://www.reddit.com/r/<subreddit>/top/.json?t=day&limit=10
- Subreddits:
  - Mumbai food: r/mumbai, r/IndianFoodPhotos, r/streeteats
  - Student motivation: r/GetMotivated, r/study, r/productivity
- Download top 5 images per niche per day
- Skip NSFW, pinned posts, text-only posts
- Save to /home/prata/instagram-automation/content/<niche>/

## Caption Generator
- Use SerpAPI or free LLM (Ollama local) to generate captions
- Format: catchy one-liner + 2-3 hashtag groups
- Example: "Best vada pav in Mumbai and nobody can change my mind 🫓\n.\n.\n#MumbaiFood #StreetFood #VadaPav #MumbaiDiaries"
- Save captions alongside images in queue

## Instagram Posting (Meta Graph API)
- Requirements (user must set up once):
  1. Facebook Developer account
  2. Facebook App (free)
  3. Instagram Business account connected to Facebook Page
  4. Generate long-lived access token
- API endpoint: POST https://graph.facebook.com/v19.0/{ig-user-id}/media
- First upload image, then publish with caption
- Rate limit: 25 posts/day (more than enough)

## Daily Cron Job
- Run daily at 8AM IST
- 1. Scrape Reddit for new content
- 2. Generate captions
- 3. Queue for tomorrow
- 4. Post today's queued content at scheduled times

## What to Build Now
1. Create the directory structure
2. Build the Reddit scraper that downloads images + titles
3. Build the caption generator
4. Build the queue system
5. Test end-to-end with 1 niche
6. Set up cron job for daily run
7. Document what the user needs to do for Instagram API (Facebook App setup)

## Output
Save everything to /home/prata/instagram-automation/
Print clear instructions for the Meta API setup the user needs to do
