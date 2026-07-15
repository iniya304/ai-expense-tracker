import easyocr

# Create the EasyOCR reader (English only, no GPU needed)
# This line downloads the language model the FIRST time you run it - normal, one-time thing
reader = easyocr.Reader(['en'], gpu=False)

# Same image we tested with Tesseract
image_path = r'data\processed\X51008164525_processed.png'

# Run OCR - detail=0 means "just give me the text, not bounding boxes"
result = reader.readtext(image_path, detail=0)

print("----- EASYOCR OUTPUT -----")
for line in result:
    print(line)