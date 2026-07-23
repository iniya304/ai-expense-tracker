# Week 3 - Field Extraction

## Approach
Used regex (pattern matching) to extract 3 structured fields from raw OCR
text: store name, date, total amount. Built and tested incrementally on
individual files before scaling to all 626, same approach as Week 2.

## Extraction logic
- **Date:** tried multiple regex patterns in order (DD Mon YYYY, DD/MM/YYYY,
  DD-MM-YYYY, YYYY-MM-DD) to cover different receipt formats
- **Total:** searched line-by-line for lines containing "total", excluding
  lines with "sub", "saving", "discount", "qty", "change", "tax", "item" to
  avoid false matches (e.g. "Total Savings", "Sub-total")
- **Store name:** searched for a line containing "SDN BHD" (common Malaysian
  company suffix), also checking the line above in case the name is split
  across two lines. Falls back to the first "valid-looking" line (min length,
  mostly letters) if no SDN BHD line is found.

## Accuracy (15 randomly sampled receipts, same sample as Week 2, seed=42)
| Field        | Correct | Accuracy |
|--------------|---------|----------|
| Store name   | 14/15   | 93%      |
| Date         | 12/15   | 80%      |
| Total amount | 12/15   | 80%      |

## Known limitations
- **OCR-destroyed source text:** some dates/totals are unreadable even to a
  human because OCR corrupted the underlying characters. No regex fix is
  possible here - the information is simply gone.
- **Person name vs. store name ambiguity:** some receipts print a
  cashier/staff name above the actual store name (e.g. "tan woon yann").
  Regex has no way to distinguish these - this requires semantic
  understanding, which is what NER (Named Entity Recognition) is designed
  for. Flagged as a future upgrade if time allows.
- **Duplicate "total" mentions:** some receipts repeat the word "total" in
  a GST summary section further down, which can override the correct
  earlier total. A rare edge case affecting a small number of receipts.

## Files
- `extract_fields.py` - single-file test/debug script
- `extract_all.py` - batch script, runs on all 626 files, saves to
  `data/extracted_fields.csv`
- `sample_check_fields.py` - generates a random 15-file sample for manual
  accuracy verification

## Decision
Proceeding to Week 4 (categorization) with current regex-based extraction.
NER upgrade considered a stretch goal for later, once the full pipeline is
working end-to-end.