import chromadb

# Connect to the same database folder we created earlier
client = chromadb.PersistentClient(path='data/chroma_db')

# Try to get the collection we created
try:
    collection = client.get_collection(name='receipts')
    count = collection.count()
    print(f"SUCCESS: Collection 'receipts' exists with {count} items.")

    if count > 0:
        # Peek at one item to confirm data looks right
        sample = collection.peek(limit=1)
        print("\nSample entry:")
        print("ID:", sample['ids'][0])
        print("Document text:", sample['documents'][0])
        print("Metadata:", sample['metadatas'][0])
except Exception as e:
    print(f"FAILED: Could not find collection. Error: {e}")
    