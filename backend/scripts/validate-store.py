import psycopg2
import pandas as pd
from datetime import date

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="invoice_db",
    user="postgres",
    password="root"
)
cursor = conn.cursor()

# Read CSV
df = pd.read_csv("invoices.csv")

# Settings
MAX_AMOUNT = 50000
today = date.today()

# Convert date column
df["date"] = pd.to_datetime(df["date"]).dt.date

# Add flags column
df["flags"] = ""

# Validation loop
for index, row in df.iterrows():
    errors = []

    if row["amount"] == 0:
        errors.append("Amount is Zero")
    if row["amount"] < 0:
        errors.append("Amount is Negative")
    if row["amount"] > MAX_AMOUNT:
        errors.append("Amount exceeds maximum limit")
    if row["date"] > today:
        errors.append("Invoice date is in the future")
    if row["is_blocked_vendor"] == 1:
        errors.append("Vendor is blocked")

    df.at[index, "flags"] = ", ".join(errors)

# Duplicate detection
duplicate_mask = df.duplicated(subset=["vendor_name", "amount", "date"], keep=False)
for index, is_duplicate in duplicate_mask.items():
    if is_duplicate:
        if df.at[index, "flags"]:
            df.at[index, "flags"] += ", Duplicate invoice"
        else:
            df.at[index, "flags"] = "Duplicate invoice"

# Update flags in database
for index, row in df.iterrows():
    cursor.execute("""
        UPDATE invoices
        SET flags = %s
        WHERE invoice_number = %s AND vendor_name = %s
    """, (
        row["flags"],
        row["invoice_number"],
        row["vendor_name"]
    ))

conn.commit()
print("Validation complete! Flags updated in database.")

cursor.close()
conn.close()