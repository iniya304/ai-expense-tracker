import csv
from collections import Counter
from rapidfuzz import fuzz

input_csv = 'data/extracted_fields.csv'
output_csv = 'data/categorized_expenses.csv'

# Category rules: category -> list of keywords to match
category_rules = {
    'Dining': ['restoran', 'restaurant', 'cafe', 'kitchen', 'grill', 'bar',
               'sushi', 'rice', 'noodle', 'seafood', 'bistro', 'kopitiam',
               'papa', 'unihakka', 'thai', 'coffee', 'roasted', 'taste',
               'brewery', 'stooges', 'pub', 'chicken', 'food', 'snack'],
    'Groceries': ['pasar', 'mart', 'market', 'bakeries', 'bakery', 'fresh',
                  'grocer', 'supermarket'],
    'Hardware': ['hardware', 'papan', 'tools', 'diy', 'timber', 'electrical'],
    'Stationery': ['stationery', 'book', 'printing', 'print'],
    'Pharmacy': ['pharmacy', 'farmasi', 'health', 'beauty', 'care'],
    'Retail': ['trading', 'enterprise', 'marketing', 'shop', 'store', 'gallery'],
}

# Similarity threshold: 0-100, higher = stricter match required
FUZZY_THRESHOLD = 75

def categorize(store_name):
    if not store_name:
        return 'Uncategorized'
    name_lower = store_name.lower()
    words = name_lower.replace('.', ' ').replace(',', ' ').split()

    best_category = 'Uncategorized'
    best_score = 0

    for category, keywords in category_rules.items():
        for keyword in keywords:
            # Check each word in the store name against each keyword
            for word in words:
                score = fuzz.ratio(word, keyword)
                if score > best_score and score >= FUZZY_THRESHOLD:
                    best_score = score
                    best_category = category

    return best_category

with open(input_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for row in rows:
    row['category'] = categorize(row['store_name'])

with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['filename', 'store_name', 'date', 'total', 'category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

counts = Counter(row['category'] for row in rows)
print("Category breakdown:")
for category, count in counts.most_common():
    print(f"  {category}: {count}")

print("\nSample of Uncategorized store names:")
uncategorized_samples = [row['store_name'] for row in rows if row['category'] == 'Uncategorized'][:30]
for name in uncategorized_samples:
    print(f"  {name}")