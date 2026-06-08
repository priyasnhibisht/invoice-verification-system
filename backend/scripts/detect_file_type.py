import os
import pdfplumber
import pandas as pd
import pytesseract
from PIL import Image

file_name = input("Enter file name (with extension):")

#Checking if the file actually exists
if not os.path.isfile(file_name):
    print(f"{file_name} does not exist.")
else:
    #Getting the extension 
    _,extension = os.path.splitext(file_name)
    extension = extension.lower()  # Convert to lowercase for case-insensitive comparison

   #PDF
    if extension == ".pdf":
        print(f"Reading {file_name}")
        with pdfplumber.open(file_name) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                print(f"Page {i+1}")
                print(text)
    #Excel
    elif extension in [".xls", ".xlsx"]:
        print(f"Reading {file_name}")
        if extension == ".xlsx":
            df=pd.read_excel(file_name, engine='openpyxl')
        elif extension == ".xls":
            df = pd.read_excel(file_name,engine='xlrd')
        print(df)
    #Images
    elif extension in [".jpg", ".jpeg", ".png"]:
        print(f"{file_name} is an image file.")
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        image=Image.open(file_name)
        text=pytesseract.image_to_string(image)
        print(text)
    #Unknown
    else:
        print(f"Unknown file type: {extension}")