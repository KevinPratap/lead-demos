import re

pitch_sheet_path = "/home/prata/leads/data/exports/pitch_sheet.md"

with open(pitch_sheet_path, 'r') as f:
    content = f.read()

# Let's see all headers of level 3 (###) to see what businesses are in it
businesses = re.findall(r'^###\s+(.+)$', content, re.MULTILINE)
print(f"Number of businesses in pitch_sheet.md: {len(businesses)}")
print("First 15 businesses in pitch_sheet.md:")
for b in businesses[:15]:
    print("-", b)
