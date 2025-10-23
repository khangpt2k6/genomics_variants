import sqlite3

conn = sqlite3.connect(r'c:\Users\2006t\Documents\Moffitt\backend\db.sqlite3')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Available tables:")
for table in tables:
    print(f"  - {table[0]}")

# Count records
cursor.execute("SELECT COUNT(*) FROM variants_variant")
variants = cursor.fetchone()[0]
print(f"\nTotal Variants: {variants}")

cursor.execute("SELECT COUNT(*) FROM variants_clinicalsignificance")
clinical = cursor.fetchone()[0]
print(f"Clinical Significance Records: {clinical}")

cursor.execute("SELECT COUNT(*) FROM variants_drugresponse")
drugs = cursor.fetchone()[0]
print(f"Drug Response Records: {drugs}")

conn.close()