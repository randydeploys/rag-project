# Design: Deduplicate Ingestion Logic via pipeline.py

## Problem

The ingestion logic (load PDFs, chunk, embed, write to FAISS) is duplicated between `ingest.py` and `app.py` (sidebar upload). Changes to chunking or embedding must be made in two places.

## Approach

Create a new `pipeline.py` module with a shared `ingest_documents()` function. Both `ingest.py` and `app.py` call it instead of reimplementing the logic.

## New file: pipeline.py

Single function:

```python
def ingest_documents(pdf_paths: list[str]) -> int
```

- Takes a list of PDF file paths
- Loads with PyMuPDFLoader
- Splits into chunks (RecursiveCharacterTextSplitter, 500 chars, 50 overlap)
- Generates embeddings with sentence-transformers/all-MiniLM-L6-v2
- Writes db/index.faiss and db/texts.pkl
- Returns the number of chunks indexed

## Changes to ingest.py

- Remove duplicated ingestion logic from `ingest()`
- Replace with: collect PDF paths from `docs/`, call `pipeline.ingest_documents(pdf_paths)`
- Keep `if __name__ == "__main__"` entry point and print statements
- `DOCS_FOLDER` stays in ingest.py (only it scans the folder)

## Changes to app.py

- Remove inline ingestion logic in sidebar upload block (~lines 42-64)
- Replace with: save uploaded files to `docs/`, collect their paths, call `pipeline.ingest_documents(pdf_paths)`
- UI, chat, DB loading, and all other behavior unchanged

## What doesn't change

- `rag.py` — untouched
- DB format (index.faiss + texts.pkl) — unchanged
- User-facing behavior — identical
- `python ingest.py` CLI — still works
