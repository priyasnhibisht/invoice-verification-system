# Invoice Dataset Notes

INV004 - amount is 0 (should be flagged)
INV005 - date in future (should be flagged)
INV007 - amount is negative (should be flagged)
INV008 - vendor is blocked (should be flagged)
INV009 - amount exceeds limit of 50000 (should be flagged)
INV010 - duplicate of INV001 (should be flagged)
INV011 - vendor blocked AND future date (should be flagged)

## Output - validate_invoices.py

```
========== Summary Report ==========
Total invoices : 11
Flagged invoices : 8
Valid invoices : 3

Flagged Invoices:
INV001 | Tata Consultancy Services | Duplicate invoice
INV004 | Bharat Petroleum | Amount is Zero
INV005 | Hindustan Unilever | Invoice date is in the future
INV007 | HDFC Bank Supplies | Amount is negative
INV008 | Mahindra Logistics | Vendor is blocked
INV009 | Sun Pharma Vendors | Amount exceeds maximum limit
INV010 | Tata Consultancy Services | Duplicate invoice
INV011 | Fake Vendor Ltd | Invoice date is in the future, Vendor is blocked
=====================================
```

## File Type Detection and Reading

### PDF Output - ASSIGNMENT-4.pdf
```
Reading ASSIGNMENT-4.pdf
Page 1
TCS-662(MACHINE LEARNING)
ASSIGNMENT-4
Q1. Explain the K-means clustering...
(text extracted successfully)
```

### Excel Output - invoices_sample.xlsx
```
Reading invoices_sample.xlsx
   invoice_number        vendor_name  amount       date  is_blocked_vendor
0          INV001  Tata Consultancy   15000 2025-03-15                  0
...
(all 11 rows printed successfully)
```

### Image
- Detection added, OCR to be implemented.