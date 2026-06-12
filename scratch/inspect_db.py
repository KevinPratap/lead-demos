import sqlite3

db_path = "/home/prata/leads/data/leads.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"Tables in leads.db: {tables}")

for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name});")
    info = cursor.fetchall()
    print(f"\nTable '{table_name}' columns:")
    for col in info:
        print(f"  {col[1]} ({col[2]})")

# Let's count rows in each table
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    count = cursor.fetchone()[0]
    print(f"Row count in '{table_name}': {count}")

conn.close()
