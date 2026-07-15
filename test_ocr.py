import pytesseract
from PIL import Image

# Tell pytesseract where Tesseract is installed on your machine
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load one processed receipt image
image_path = r'data\processed\X51008164525_processed.png'
image = Image.open(image_path)

# Run OCR on it
text = pytesseract.image_to_string(image)

print("----- OCR OUTPUT -----")
print(text)


