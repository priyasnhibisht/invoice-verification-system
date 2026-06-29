from sqlalchemy import Column, Integer, String, Numeric, Date, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_number = Column(String(50))
    vendor_name = Column(String(100))
    amount = Column(Numeric(10, 2))
    invoice_date = Column(Date)
    is_blocked_vendor = Column(Integer)
    flags = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)