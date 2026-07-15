# AI-Powered Expense Tracker (OCR + Document Intelligence)

An AI-powered expense tracker that extracts data from receipt images using
OCR and document intelligence, with plans for semantic search and a
natural-language query layer.

## Tech Stack (planned, full pipeline)
OpenCV (preprocessing) → Tesseract/EasyOCR → Donut/LayoutLMv3 (OCR) →
Regex/NER (field extraction) → rule-based/ML (categorization) →
sentence-transformers + FAISS/ChromaDB (embeddings) →
Claude/Groq API (query layer) → FastAPI + SQLite + Streamlit → deployed on
HF Spaces/Render

## Project Status
- ✅ **Week 1:** Image preprocessing pipeline (OpenCV: deskew, denoise, CLAHE
  contrast enhancement, binarization). Ran on 626 receipt images from the
  SROIE2019 dataset — all succeeded.
- ✅ **Week 2:** OCR pipeline built and evaluated.
  - Tested Tesseract vs EasyOCR on sample receipts
  - Chose **Tesseract** — comparable accuracy, better line structure
    preservation, lighter/faster
  - Measured accuracy on 15 randomly sampled receipts:
    - Store name: 80%
    - Date: 93%
    - Total amount: 87%
    - Item lines: 67%
  - Full findings in [`Week 2 - OCR Evaluation.md`](./Week%202%20-%20OCR%20Evaluation.md)

## Dataset
This project uses the [SROIE2019](https://www.kaggle.com/datasets/urbikn/sroie-datasetv2)
receipt dataset from Kaggle. The dataset itself is **not included** in this
repo (see `.gitignore`) due to size — download it separately from Kaggle if
you want to reproduce results.

## Reproducing the pipeline
1. Download the SROIE2019 dataset and place images in `data/raw/kaggle`
2. Run preprocessing: