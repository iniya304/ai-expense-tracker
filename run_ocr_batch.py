import pytesseract
from PIL import Image
import os

# Tell pytesseract where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Folders
input_folder = 'data/processed'
output_folder = 'data/ocr_output'

# Create the output folder if it doesn't exist yet
os.makedirs(output_folder, exist_ok=True)

# Get all files that end with "_processed.png" (skip the "_enhanced" ones for now)
files = [f for f in os.listdir(input_folder) if f.endswith('_processed.png')]

print(f"Found {len(files)} images to process.")

success_count = 0
fail_count = 0

for filename in files:
    image_path = os.path.join(input_folder, filename)
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        # Save the text output with a matching name
        output_name = filename.replace('_processed.png', '.txt')
        output_path = os.path.join(output_folder, output_name)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)

        success_count += 1
    except Exception as e:
        print(f"FAILED on {filename}: {e}")
        fail_count += 1

print(f"Done. {success_count} succeeded, {fail_count} failed.")