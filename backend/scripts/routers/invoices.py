from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil, os, pandas as pd, pdfplumber, re
from datetime import datetime
from db import get_db
from models import Invoice

router = APIRouter()

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    _, extension = os.path.splitext(file.filename)
    extension = extension.lower()

    if extension in [".xlsx", ".xls"]:
        result = validate_excel(temp_path, file.filename, db)
    elif extension == ".pdf":
        result = validate_pdf(temp_path, file.filename, db)
    else:
        result = {"error": "Only Excel and PDF supported right now"}

    try:
        os.remove(temp_path)
    except:
        pass

    return result


def validate_excel(filepath, original_filename, db: Session):
    all_results = []
    seen_invoices = set()

    xl = pd.ExcelFile(filepath, engine="openpyxl")

    for sheet_name in xl.sheet_names:
        df = None
        for header_row in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            temp_df = pd.read_excel(filepath, sheet_name=sheet_name,
                                   engine="openpyxl", header=header_row)
            if "INVOICE_NUMBER" in temp_df.columns:
                df = temp_df
                break

        if df is None or df.empty:
            continue

        df = df.dropna(how="all")

        for _, row in df.iterrows():
            errors = []
            invoice_num = str(row.get("INVOICE_NUMBER", "")).strip()

            if not invoice_num or invoice_num == "nan":
                continue

            if invoice_num in seen_invoices:
                errors.append("Duplicate invoice number")
            else:
                seen_invoices.add(invoice_num)

            try:
                from_date = pd.to_datetime(row["FROM_DATE"], dayfirst=True)
                to_date = pd.to_datetime(row["TO_DATE"], dayfirst=True)
                if from_date > to_date:
                    errors.append("FROM_DATE is after TO_DATE")
                if to_date > datetime.now():
                    errors.append("TO_DATE is in the future")
            except:
                errors.append("Invalid date format")

            try:
                fixed = float(row.get("FIXED_RENT_CHARGES", 0) or 0)
                cgst = float(row.get("CGST", 0) or 0)
                sgst = float(row.get("SGST", 0) or 0)
                disc = float(row.get("20% Disc", 0) or 0)
                total = float(row.get("TOTAL_PAYABLE", 0) or 0)

                expected = round(fixed + cgst + sgst + disc, 2)
                actual = round(total, 2)

                if abs(expected - actual) > 1:
                    errors.append(f"Amount mismatch: expected {expected}, got {actual}")

                if total <= 0:
                    errors.append("Total payable is zero or negative")
            except:
                errors.append("Invalid amount values")

            status = "FLAGGED" if errors else "VALID"
            flags_text = ", ".join(errors)
            telephone = str(row.get("TELEPHONE_NUMBER", ""))

            existing = db.query(Invoice).filter(
                Invoice.invoice_number == invoice_num
            ).first()

            if existing:
                existing.status = status
                existing.flags = flags_text
                existing.total_payable = total
            else:
                new_invoice = Invoice(
                    invoice_number=invoice_num,
                    telephone=telephone,
                    sheet_name=sheet_name,
                    total_payable=total,
                    status=status,
                    flags=flags_text,
                    source_file=original_filename
                )
                db.add(new_invoice)

            all_results.append({
                "sheet": sheet_name,
                "invoice_number": invoice_num,
                "telephone": telephone,
                "total_payable": total,
                "status": status,
                "errors": errors
            })

    db.commit()

    flagged = [r for r in all_results if r["status"] == "FLAGGED"]
    valid = [r for r in all_results if r["status"] == "VALID"]

    return {
        "total_invoices": len(all_results),
        "valid": len(valid),
        "flagged": len(flagged),
        "results": all_results
    }


def validate_pdf(filepath, original_filename, db: Session):
    all_results = []
    errors = []

    with pdfplumber.open(filepath) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # Extract bill number
    bill_number = "UNKNOWN"
    bill_match = re.search(r"Bill number\s+(\S+)", full_text)
    if bill_match:
        bill_number = bill_match.group(1)

    # Extract bill date
    date_match = re.search(r"Bill date\s+(\d{2}-\w+-\d{4})", full_text)
    if date_match:
        try:
            bill_date = datetime.strptime(date_match.group(1), "%d-%b-%Y")
            if bill_date > datetime.now():
                errors.append("Bill date is in the future")
        except:
            errors.append("Invalid bill date format")
    else:
        errors.append("Bill date not found")

    # Extract totals from text
    amounts = re.findall(r"\d+\.\d{2}", full_text)
    amounts = [float(a) for a in amounts]

    # Extract grand total
    total_match = re.search(r"Total\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", full_text)
    if total_match:
        try:
            fixed_total = float(total_match.group(1))
            sgst_total = float(total_match.group(2))
            cgst_total = float(total_match.group(3))
            grand_total = float(total_match.group(4))

            expected = round(fixed_total + sgst_total + cgst_total, 2)
            actual = round(grand_total, 2)

            if abs(expected - actual) > 1:
                errors.append(f"Grand total mismatch: expected {expected}, got {actual}")
        except:
            errors.append("Could not validate grand total")

    status = "FLAGGED" if errors else "VALID"
    flags_text = ", ".join(errors)

    # Save to database
    existing = db.query(Invoice).filter(
        Invoice.invoice_number == bill_number
    ).first()

    if existing:
        existing.status = status
        existing.flags = flags_text
    else:
        new_invoice = Invoice(
            invoice_number=bill_number,
            telephone="N/A",
            sheet_name="PDF",
            total_payable=grand_total if total_match else 0,
            status=status,
            flags=flags_text,
            source_file=original_filename
        )
        db.add(new_invoice)

    db.commit()

    all_results.append({
        "sheet": "PDF",
        "invoice_number": bill_number,
        "telephone": "N/A",
        "total_payable": grand_total if total_match else 0,
        "status": status,
        "errors": errors
    })

    flagged = [r for r in all_results if r["status"] == "FLAGGED"]
    valid = [r for r in all_results if r["status"] == "VALID"]

    return {
        "total_invoices": len(all_results),
        "valid": len(valid),
        "flagged": len(flagged),
        "results": all_results
    }


@router.get("/")
def get_all_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).all()
    return invoices


@router.get("/flagged")
def get_flagged_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).filter(Invoice.status == "FLAGGED").all()
    return invoices


@router.get("/valid")
def get_valid_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).filter(Invoice.status == "VALID").all()
    return invoices