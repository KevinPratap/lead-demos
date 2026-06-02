"""scripts/sheets_sync.py — Google Sheets sync (OAuth-based, deferred to v2).

For v1, we use scripts/export_local.py (writes CSV + Markdown).
When you're ready for live Sheets sync:

  1. https://console.cloud.google.com/  → new project "hermes-leads"
  2. Enable "Google Sheets API"
  3. APIs & Services → Credentials → Create OAuth client ID → Desktop app
  4. Download JSON → save as ~/.config/hermes/leads/google_creds.json
  5. First run:  python scripts/sheets_sync.py --auth
  6. Then:       python scripts/sheets_sync.py   (will push the 5 new leads)

See README.md → "Google Sheets sync" for the full walkthrough.
"""
import sys

def main():
    print("Google Sheets sync is not enabled in v1.", file=sys.stderr)
    print("Use scripts/export_local.py instead — it writes data/exports/pitch_sheet.md", file=sys.stderr)
    print("which you can copy-paste into any Google Sheet you create.", file=sys.stderr)
    return 1

if __name__ == "__main__":
    sys.exit(main())
