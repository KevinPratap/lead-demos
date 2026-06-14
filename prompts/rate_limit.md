# Task: Add Rate Limiting to WhatsApp Sender

## Goal
Rewrite send_whatsapp.js to be bulletproof against WhatsApp spam detection. We got banned for 176 messages in rapid bursts. Never again.

## File to modify
/home/prata/leads/scripts/send_whatsapp.js

## Required Features

### 1. Rate Limit File
Create /home/prata/leads/data/rate_limit.json to track:
```json
{
  "last_send": "2026-06-13T10:00:00Z",
  "today_count": 5,
  "today_date": "2026-06-13",
  "hour_counts": {"9": 2, "10": 3}
}
```

### 2. Before ANY send, enforce:
- MINIMUM 90 seconds since last send (read from rate_limit.json)
- If less than 90s, sleep until 90s has passed (don't just fail)
- MAXIMUM 20 sends per day
- If over 20, exit with error: "Daily limit reached (20/20). Try again tomorrow."
- MAXIMUM 5 sends per hour
- If over 5 this hour, exit with error: "Hourly limit reached (5/5). Wait until next hour."

### 3. After each successful send:
- Update rate_limit.json with new last_send time
- Increment today_count
- Increment this hour's count
- Add 2-8 seconds of random jitter after the send to look human

### 4. Update wa_sent.json logging to include:
- sent_at timestamp (already exists)
- batch_id (identify which batch this was part of)
- message_hash (so we can detect identical messages)

### 5. Keep ALL existing functionality
- QR code generation
- Lead lookup from SQLite
- Message composition with structure variations
- --list flag
- All CLI args

## Important
- The user's WhatsApp WILL get restricted again if we don't fix this
- 176 messages blasted = ban. 20/day spread across hours = safe
- Vary message structure (already done in composeWhatsAppMessage)
- The rate limiting must be enforced at the SCRIPT level, not just documentation
- Add a --force flag that bypasses rate limits (for emergencies only)

## Test
After building, test: node scripts/send_whatsapp.js --list (should still work, no rate limit check needed for reads)
