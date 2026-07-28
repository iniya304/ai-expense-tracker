# Week 5 - Embeddings & Vector Search

## Approach
Used sentence-transformers (`all-MiniLM-L6-v2`) to convert each receipt's
summary (store name, category, date, total) into an embedding, stored in
ChromaDB (persisted locally at `data/chroma_db`). Enables semantic search:
finding relevant receipts by meaning, not just exact keyword matches.

## Results - what works well
Tested across 7 queries spanning different categories and difficulty:
- **Category-based queries** (e.g. "hardware store purchase", "food and
  restaurants", "books and stationery", "pharmacy and medicine", "grocery
  shopping") all returned highly relevant, correctly-categorized results -
  including matching OCR-garbled store name variants (e.g. "buardian
  Health And Heauty" correctly matched "pharmacy") without any manual
  keyword rules, unlike Week 4's categorization approach.
- Worked well even on a small category (Pharmacy, only 11 total receipts).

## Results - known limitation
- **Numeric/quantitative queries fail:** questions like "where did I spend
  the most money" or "cheap purchases under 10 ringgit" did NOT correctly
  filter or sort by amount. Results were topically similar in wording but
  not numerically accurate.
- **Why:** embeddings capture semantic/textual meaning, not numeric
  reasoning. Semantic search can find *which* receipts relate to a topic,
  but cannot perform sorting, filtering, or math over the `total` field.

## Implication for Week 6
The natural-language query layer (Claude/Groq API) will need to combine
semantic search with actual code-level computation:
- Use embeddings to retrieve topically relevant receipts (e.g. "groceries")
- Use real arithmetic (sum/sort/filter in Python) for anything involving
  amounts, totals, or rankings ("most", "least", "under X")
This mirrors how real-world RAG (Retrieval-Augmented Generation) systems
are typically built.

## Files
- `build_embeddings.py` - generates embeddings for all 626 receipts, stores
  in ChromaDB
- `check_embeddings.py` - verifies the embeddings database was built
  correctly
- `search_receipts.py` - semantic search test script with example queries