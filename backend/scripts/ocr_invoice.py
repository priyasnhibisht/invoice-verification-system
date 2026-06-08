import pytesseract 
from PIL import Image

#Location of Tesseract 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Opening Image
image = Image.open('invoice-image.jpg')

#Extracting text from image
text = pytesseract.image_to_string(image)

print(text)
