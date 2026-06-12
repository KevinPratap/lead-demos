import sqlite3

db_path = "/home/prata/leads/data/leads.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT category FROM leads;")
categories = [c[0] for c in cursor.fetchall() if c[0]]

print("Unique categories in leads.db:")
for cat in sorted(categories):
    print("-", cat)

conn.close()
