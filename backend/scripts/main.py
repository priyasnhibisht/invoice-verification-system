from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine
from models import Base

# Create FastAPI app
app = FastAPI(title="Invoice Verification System")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables in database on startup
Base.metadata.create_all(bind=engine)

# Basic route to test if server is running
@app.get("/")
def home():
    return {"message": "Invoice Verification System is running!"}

from routers import invoices

app.include_router(invoices.router, prefix="/invoices")