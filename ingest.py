# ingest.py
import os
from pipeline import ingest_documents

DOCS_FOLDER = "docs"


def ingest():
    pdf_paths = [
        os.path.join(DOCS_FOLDER, f)
        for f in os.listdir(DOCS_FOLDER)
        if f.endswith(".pdf")
    ]

    if not pdf_paths:
        print("Aucun PDF trouve dans le dossier docs/")
        return

    print(f"Indexation de {len(pdf_paths)} PDF(s)...")
    num_chunks = ingest_documents(pdf_paths)
    print(f"Termine ! {num_chunks} chunks stockes dans FAISS")


if __name__ == "__main__":
    ingest()
