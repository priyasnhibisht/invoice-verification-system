from sqlalchemy import Column, Integer, String, Numeric, Date, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class InvoiceStatus(str, enum.Enum):
    VALID = "VALID"
    FLAGGED = "FLAGGED"
    PENDING = "PENDING"

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_number = Column(String(100), unique=True)
    telephone = Column(String(50))
    sheet_name = Column(String(50))
    total_payable = Column(Numeric(10, 2))
    status = Column(String(20), default="PENDING")
    flags = Column(Text)
    source_file = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)