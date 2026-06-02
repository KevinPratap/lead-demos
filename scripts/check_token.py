"""Quick token check: GET /v2/users/me with the APIFY_TOKEN. Prints 200 + username if good."""
import os, sys, requests
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/hermes/leads/.env"))
token = os.environ.get("APIFY_TOKEN", "")
if not token or token == "apify_...":
    print("FAIL: APIFY_TOKEN is missing or placeholder in ~/.config/hermes/leads/.env")
    sys.exit(1)

r = requests.get(
    "https://api.apify.com/v2/users/me",
    headers={"Authorization": f"Bearer {token}"},
    timeout=15,
)
print(f"HTTP {r.status_code}")
print(r.text[:500])
if r.status_code == 200:
    data = r.json().get("data", {})
    print(f"\nOK: username={data.get('username')}  email={data.get('email')}")
    print(f"plan={data.get('plan', {}).get('id')}  trialed={data.get('trialedWithFreeCredit')}")
    sys.exit(0)
sys.exit(2)
