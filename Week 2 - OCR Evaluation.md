# Week 2 - OCR Evaluation

## Engines tested
- Tesseract (via pytesseract)
- EasyOCR

## Comparison (single receipt test)
Both engines struggled equally on item tables and cash/change fields.
Tesseract preserved line structure better, making it easier to extract
fields later with regex. EasyOCR broke text into fragmented single-word
lines, losing row structure. EasyOCR is also heavier (PyTorch-based) and
slower per image.

**Decision: proceeding with Tesseract** as the primary OCR engine.

## Accuracy sample (15 randomly selected receipts, seed=42)
| Field        | Correct | Accuracy |
|--------------|---------|----------|
| Store name   | 12/15   | 80%      |
| Date         | 14/15   | 93%      |
| Total amount | 13/15   | 87%      |
| Item lines   | 10/15   | 67%      |

## Takeaway
Tesseract is reliable enough for dates and totals (core expense-tracking
fields). Item-level detail is the weakest area — tightly packed
columns (qty/price/description) are hardest to read. Flagged as a
possible future upgrade (Donut/LayoutLMv3) if item-level accuracy
becomes important later.    