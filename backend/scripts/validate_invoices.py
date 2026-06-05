import pandas as pd
from datetime import date

#Read CSV file
df = pd.read_csv('invoices.csv')

#Set Maximum amount for invoice and date validation
Max_Amount = 50000
today = date.today()

#Add a new column to store flag for invalid invoices
df['flags'] = ''

print("File loaded successfully!")
print(f"Total invoices found: {len(df)}")
print(f"Today's date: {today}")

#Convert date columns to actual date format
df['date'] = pd.to_datetime(df['date']).dt.date

#Iterate through each invoice and validate
for index,row in df.iterrows():
    errors = []

    #Check if amount is ZERO
    if row['amount'] ==0:
        errors.append('Amount is Zero')
    
    #Check is amount is negative
    if row['amount'] <0:
        errors.append('Amount is negative')

    #Check is amount exceeds maximum limit
    if row['amount'] >Max_Amount:
        errors.append('Amount exceeds maximum limit')
    
    #Check if future date
    if row['date'] >today:
        errors.append('Invoice date is in the future')

    #Check is vendor is blocked
    if row['is_blocked_vendor'] == 1:
        errors.append('Vendor is blocked')
    
    #Add errors to flags column
    df.at[index,'flags'] = ', '.join(errors)

#Check for duplicates

duplicate_mask = df.duplicated(subset=['vendor_name','amount','date'],keep=False)
for index,is_duplicate in duplicate_mask.items():
    if is_duplicate:
        if df.at[index,'flags']:
            df.at[index,'flags'] += ', Duplicate invoice'
        else:
            df.at[index,'flags'] = 'Duplicate invoice'

print(df)

#Summary Report

flagged = df[df['flags']!='']
valid  = df[df['flags']=='']

print("\n========== Summary Report ==========")
print(f"Total invoices : {len(df)}")
print(f"Flagged invoices : {len(flagged)}")
print(f"Valid invoices : {len(valid)}")
print("\nFlagged Invoices:")
for index,row in flagged.iterrows():
    print(f"Invoice Number: {row['invoice_number']}, Vendor: {row['vendor_name']}, Amount: {row['amount']}, Date: {row['date']}, Flags: {row['flags']}")
print("==================================")