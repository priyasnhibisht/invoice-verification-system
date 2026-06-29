from fastapi import APIRouter, UploadFile, File
import shutil, os, pandas as pd
from datetime import datetime

router = APIRouter()

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    _, extension = os.path.splitext(file.filename)
    extension = extension.lower()

    if extension in [".xlsx", ".xls"]:
        result = validate_excel(temp_path)
    else:
        result = {"error": "Only Excel supported right now"}

    try:
        os.remove(temp_path)
    except:
        pass

    return result


def validate_excel(filepath):
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

            all_results.append({
                "sheet": sheet_name,
                "invoice_number": invoice_num,
                "telephone": str(row.get("TELEPHONE_NUMBER", "")),
                "total_payable": total,
                "status": "FLAGGED" if errors else "VALID",
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