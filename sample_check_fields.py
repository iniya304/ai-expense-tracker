import csv
import random

input_csv = 'data/extracted_fields.csv'

with open(input_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

random.seed(42)  # same seed style as Week 2, so results are reproducible
sample = random.sample(rows, 15)

print("Review these 15 rows:\n")
for row in sample:
    print(f"{row['filename']}: store='{row['store_name']}', date='{row['date']}', total='{row['total']}'")
    