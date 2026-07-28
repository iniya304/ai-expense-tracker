# Week 6 - Natural Language Query Layer

## Approach
Built a RAG (Retrieval-Augmented Generation) system using the Groq API
(llama-3.3-70b-versatile model):
1. **Retrieve/Compute** - real Python code calculates totals, counts, and
   averages per category directly from `categorized_expenses.csv`
2. **Generate** - the computed facts are passed to the AI, which phrases
   a natural-language answer. The AI never calculates numbers itself,
   avoiding hallucination risk.

## Key design decisions
- API key stored securely in `.env` (excluded from Git via `.gitignore`)
- System prompt explicitly instructs the AI to answer only from provided
  data and to honestly decline if data is insufficient - critical for
  avoiding made-up numbers
- Category matching handles: exact names, case-insensitivity, common
  synonyms (e.g. "food" -> Dining + Groceries), singular/plural variants
  (e.g. "Grocery" -> "Groceries"), and multiple categories per question
  (e.g. "compare Dining and Hardware")

## Testing results
Tested 5 question types after initial fixes:
| Question type | Result |
|---|---|
| Synonym ("food") | Correctly summed Dining + Groceries |
| Case variation | Correct |
| Nonexistent category | Honestly declined, no hallucination |
| Multi-category comparison | Correctly computed and compared both |
| Average calculation | Correct (after singular/plural fix) |

All 5 questions verified correct after two rounds of debugging (added
synonym mapping, multi-category support, and singular/plural handling).

## Known limitations
- Synonym list is manually curated (not exhaustive) - unmapped synonyms
  fall back to an overall summary rather than a specific category
- Cannot answer time-based questions yet (e.g. "this month") - no date
  filtering logic implemented
- Cannot combine semantic search (Week 5) with numeric computation in a
  single query yet - currently category-matching is done via keyword/
  synonym lookup, not embeddings

## Files
- `test_groq.py` - initial API connection test
- `ask_expenses.py` - main query logic: category matching, computation,
  and AI-generated natural language answers