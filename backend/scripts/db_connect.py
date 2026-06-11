import psycopg2
import pandas as pd

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="invoice_db",
    user="postgres",
    password="root"
)

print("Connected to database successfully!")

# Read the CSV
df = pd.read_csv("invoices.csv")

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Insert each row into the database
for index, row in df.iterrows():
    # Check if invoice already exists
    cursor.execute("""
        SELECT COUNT(*) FROM invoices
        WHERE invoice_number = %s AND vendor_name = %s
    """, (row['invoice_number'], row['vendor_name']))

    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
            INSERT INTO invoices (invoice_number, vendor_name, amount, invoice_date, is_blocked_vendor)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row['invoice_number'],
            row['vendor_name'],
            row['amount'],
            row['date'],
            row['is_blocked_vendor']
        ))
    else:
        print(f"Skipping {row['invoice_number']} - already exists!")

# Save the changes
conn.commit()
print("Done inserting invoices!")

# Fetch all invoices from database
cursor.execute("SELECT * FROM invoices;")
rows = cursor.fetchall()

print("\n========== Invoices in Database ==========")
for row in rows:
    print(row)
print(f"\nTotal records in database: {len(rows)}")

# Close connection
cursor.close()
conn.close()