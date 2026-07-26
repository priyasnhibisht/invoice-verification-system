# Invoice Verification System
Automated invoice verification system built during internship at ONGC, Dehradun.

## What it does
- Accepts invoice files in Excel (.xlsx), PDF, and scanned image formats
- Automatically extracts data from uploaded files
- Validates invoices against business rules
- Detects errors and flags suspicious invoices
- Stores all results in a PostgreSQL database
- Displays results on a React dashboard

## Validation checks
- Amount mismatch (Fixed Rent + CGST + SGST ≠ Total)
- Duplicate invoice numbers
- Future dates
- Zero or negative amounts
- Grand total verification for PDFs

## Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| PDF Parsing | pdfplumber |
| Excel Parsing | pandas, openpyxl |
| OCR | Tesseract, pytesseract |
| Frontend | React |

## Project Structure
```
invoice-verification-system/
├── backend/
│   └── scripts/
│       ├── main.py          # FastAPI app entry point
│       ├── db.py            # Database connection
│       ├── models.py        # Database table models
│       ├── schemas.py       # Data validation schemas
│       ├── .env             # Environment variables
│       └── routers/
│           └── invoices.py  # API endpoints + validation logic
└── frontend/
    └── src/
        └── App.js           # React dashboard
```

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| POST | /invoices/upload | Upload and validate invoice file |
| GET | /invoices/ | Get all invoices |
| GET | /invoices/valid | Get valid invoices only |
| GET | /invoices/flagged | Get flagged invoices only |

## Setup Instructions

### Backend
```bash
cd backend/scripts
pip install fastapi uvicorn sqlalchemy psycopg2-binary pandas openpyxl pdfplumber pytesseract pillow python-dotenv python-multipart
```

Create `.env` file:
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5433/invoice_db
```

Run the server:
```bash
python -m uvicorn main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

### Frontend
```bash
cd frontend
npm install
npm start
```

Dashboard available at: `http://localhost:3002`

## Developed by
Priya Bisht — B.Tech Computer Science, Graphic Era University  
Internship at ONGC, Dehradun — Summer 2026
