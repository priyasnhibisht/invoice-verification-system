from pydantic import BaseModel
from datetime import date
from typing import Optional

class InvoiceBase(BaseModel):
    invoice_number: str
    vendor_name: str
    amount: float
    invoice_date: date
    is_blocked_vendor: int

class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    vendor_name: str
    amount: float
    invoice_date: date
    is_blocked_vendor: int
    flags: Optional[str] = None

    class Config:
        from_attributes = True