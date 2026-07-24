# Week 4 - Categorization

## Approach
Rule-based categorization using keyword matching, per the original tech
stack plan (rule-based first, ML/NER later if needed). Built and measured
in two stages:

1. **Exact keyword matching** - checked if any category keyword appeared as
   a substring in the store name (case-insensitive)
2. **Fuzzy matching upgrade** - since OCR garbles store names differently
   each time (e.g. "unihakka" appearing as "unthakica", "unikakka",
   "unirakka"), switched to fuzzy string similarity (rapidfuzz,
   threshold=75) so near-matches are still caught, without needing to
   manually list every possible misspelling

## Categories
Dining, Groceries, Hardware, Stationery, Pharmacy, Retail, Uncategorized

## Results (626 total receipts)
| Stage | Uncategorized | Categorized |
|-------|---------------|-------------|
| Exact keyword matching | 356 (57%) | 270 (43%) |
| + Fuzzy matching | 307 (49%) | 319 (51%) |

## Category breakdown (final)
| Category | Count |
|----------|-------|
| Uncategorized | 307 |
| Dining | 146 |
| Groceries | 60 |
| Hardware | 37 |
| Stationery | 34 |
| Retail | 31 |
| Pharmacy | 11 |

## Known limitations
- **Person names instead of store names:** some receipts extracted a
  cashier/staff name (e.g. "tan woon yann") rather than the actual business
  name (a carryover limitation from Week 3's store-name extraction). No
  keyword-based approach can categorize a person's name into a business
  type.
- **Pure OCR garbage:** some store name extractions are unrecognizable
  noise (e.g. "Bs ay lS") with no real signal to categorize from.
- **Addresses extracted as store names:** a few rows contain address
  fragments instead of business names, another carryover from Week 3.
- **Threshold trade-off:** fuzzy matching threshold (75) balances catching
  OCR variants vs. avoiding false-positive matches on unrelated words.
  Lowering it further could catch more variants but risks miscategorizing
  unrelated stores.

## Decision
Rule-based + fuzzy matching adopted as the categorization baseline (~51%
coverage). Remaining uncategorized receipts are attributable to upstream
Week 3 extraction issues (garbled/wrong store names), not a categorization
logic gap. A full ML/NER-based approach is flagged as a future upgrade,
consistent with the original tech stack plan, if time allows revisiting
store-name extraction quality first.

## Files
- `categorize.py` - categorization script, reads `extracted_fields.csv`,
  outputs `data/categorized_expenses.csv` with an added `category` column