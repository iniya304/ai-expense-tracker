import re

# Load one OCR text file to test with
file_path = r'data\ocr_output\X51006350763.txt'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

print("----- ORIGINAL TEXT -----")
print(text)

# ---------- DATE ----------
# Pattern: 2-digit day, space, 3-letter month, space, 4-digit year
# Example match target: "03 Mar 2018"
date_pattern = r'\d{2}\s[A-Za-z]{3}\s\d{4}'
date_match = re.search(date_pattern, text)

print("\n----- DATE FOUND -----")
if date_match:
    print(date_match.group())
else:
    print("No date found")

# ---------- TOTAL AMOUNT ----------
# Find lines mentioning "total" (but not "sub total"), then grab a number from that line
# Dollar sign is now OPTIONAL, since some receipts don't use "$"
total_matches = []
for line in text.split('\n'):
    if re.search(r'total', line, re.IGNORECASE) and not re.search(r'sub\s*total', line, re.IGNORECASE):
        amount = re.search(r'\$?\d+\.\d{2}', line)
        if amount:
            total_matches.append(amount.group())

print("\n----- TOTAL-LABELED AMOUNTS FOUND -----")
print(total_matches)

print("\n----- FINAL TOTAL (last match) -----")
if total_matches:
    print(total_matches[-1])
else:
    print("No total found")

# ---------- STORE NAME ----------
# First try: a line containing "SDN BHD"
store_pattern = r'.*SDN\s*BHD.*'
store_match = re.search(store_pattern, text, re.IGNORECASE)

if store_match:
    store_name = store_match.group().strip()
else:
    # Fallback: no "SDN BHD" found, so just use the first non-empty line
    # (store name is usually printed at the very top of a receipt)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    store_name = lines[0] if lines else None

print("\n----- STORE NAME FOUND -----")
if store_name:
    print(store_name)
else:
    print("No store name found")