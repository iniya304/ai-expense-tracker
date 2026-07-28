import csv
import chromadb
from sentence_transformers import SentenceTransformer

input_csv = 'data/categorized_expenses.csv'

print("Loading embedding model (first run downloads it, ~80MB)...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Set up ChromaDB - stores data in a local folder, persists between runs
client = chromadb.PersistentClient(path='data/chroma_db')
collection = client.get_or_create_collection(name='receipts')

# Read your categorized data
with open(input_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Found {len(rows)} receipts. Building embeddings...")

documents = []
ids = []
metadatas = []

for row in rows:
    # Combine fields into one descriptive text summary
    summary = f"{row['store_name']}, category: {row['category']}, date: {row['date']}, total: RM{row['total']}"
    documents.append(summary)
    ids.append(row['filename'])
    metadatas.append({
        'store_name': row['store_name'] or '',
        'category': row['category'] or '',
        'date': row['date'] or '',
        'total': row['total'] or ''
    })

# Add everything to ChromaDB in one batch (it handles the embedding internally)
collection.add(
    documents=documents,
    ids=ids,
    metadatas=metadatas
)

print(f"Done. {len(documents)} receipts embedded and stored in ChromaDB.")