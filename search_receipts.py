import chromadb

# Connect to your existing embeddings database
client = chromadb.PersistentClient(path='data/chroma_db')
collection = client.get_collection(name='receipts')

def search(query, num_results=5):
    results = collection.query(
        query_texts=[query],
        n_results=num_results
    )

    print(f"\nTop {num_results} results for: '{query}'\n")
    for i in range(len(results['ids'][0])):
        filename = results['ids'][0][i]
        metadata = results['metadatas'][0][i]
        distance = results['distances'][0][i]

        print(f"{i+1}. {metadata['store_name']}")
        print(f"   Category: {metadata['category']} | Date: {metadata['date']} | Total: RM{metadata['total']}")
        print(f"   (similarity distance: {distance:.3f})")
        print()

# Try a few test searches - mix of easy and harder cases
search("hardware store purchase")
search("food and restaurants")
search("books and stationery")
search("pharmacy and medicine")
search("where did I spend the most money")
search("grocery shopping")
search("cheap purchases under 10 ringgit")