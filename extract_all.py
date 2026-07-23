import re
import os
import csv

input_folder = 'data/ocr_output'
output_csv = 'data/extracted_fields.csv'

# ---------- DATE PATTERNS ----------
date_patterns = [
    r'\d{2}\s[A-Za-z]{3}\s\d{4}',      # 03 Mar 2018
    r'\d{1,2}/\d{1,2}/\d{2,4}',         # 25/12/2018
    r'\d{1,2}-\d{1,2}-\d{2,4}',         # 03-03-2018
    r'\d{4}-\d{1,2}-\d{1,2}',           # 2018-03-05
]

def extract_date(text):
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return None

# ---------- TOTAL AMOUNT ----------
def extract_total(text):
    # Words that mean "this total-looking line is NOT the real total"
    exclude_keywords = ['sub', 'saving', 'discount', 'qty', 'change', 'tax', 'item']
    matches = []
    for line in text.split('\n'):
        line_lower = line.lower()
        if 'total' in line_lower and not any(kw in line_lower for kw in exclude_keywords):
            amount = re.search(r'\$?\d+\.\d{2}', line)
            if amount:
                matches.append(amount.group())
    return matches[-1] if matches else None

# ---------- STORE NAME ----------
def is_valid_store_line(line):
    line = line.strip()
    if len(line) < 5:
        return False
    letters = sum(c.isalpha() for c in line)
    if letters < 3:
        return False
    if letters / len(line) < 0.5:
        return False
    return True

def extract_store(text):
    lines = text.split('\n')

    # First choice: find the "SDN BHD" line, and check if the line above
    # is a continuation of the same name (common when it's split in two)
    for i, line in enumerate(lines):
        if re.search(r'SDN\s*BHD', line, re.IGNORECASE):
            store_line = line.strip()
            if i > 0:
                prev_line = lines[i - 1].strip()
                if prev_line and is_valid_store_line(prev_line) and 'SDN' not in prev_line.upper():
                    store_line = prev_line + ' ' + store_line
            return store_line

    # Fallback: first line that looks like a real name
    for line in lines:
        stripped = line.strip()
        if stripped and is_valid_store_line(stripped):
            return stripped

    return None

# ---------- RUN ON ALL FILES ----------
files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
print(f"Found {len(files)} files to process.")

results = []

for filename in files:
    file_path = os.path.join(input_folder, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    results.append({
        'filename': filename.replace('.txt', ''),
        'store_name': extract_store(text),
        'date': extract_date(text),
        'total': extract_total(text)
    })

with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['filename', 'store_name', 'date', 'total'])
    writer.writeheader()
    writer.writerows(results)

total_files = len(results)
date_found = sum(1 for r in results if r['date'])
total_found = sum(1 for r in results if r['total'])
store_found = sum(1 for r in results if r['store_name'])

print(f"\nDone. Results saved to {output_csv}")
print(f"Date found: {date_found}/{total_files} ({date_found/total_files*100:.1f}%)")
print(f"Total found: {total_found}/{total_files} ({total_found/total_files*100:.1f}%)")
print(f"Store name found: {store_found}/{total_files} ({store_found/total_files*100:.1f}%)")