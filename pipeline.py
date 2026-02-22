# pipeline.py
import os
import pickle
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

DB_FOLDER = "db"


def ingest_documents(pdf_paths: list[str]) -> int:
    """Load PDFs, chunk, embed, and store in FAISS. Returns number of chunks indexed."""
    # Load PDFs
    documents = []
    for path in pdf_paths:
        loader = PyMuPDFLoader(path)
        documents.extend(loader.load())

    if not documents:
        return 0

    # Chunk
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)

    # Embed
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=False)

    # Store in FAISS
    os.makedirs(DB_FOLDER, exist_ok=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    faiss.write_index(index, os.path.join(DB_FOLDER, "index.faiss"))

    with open(os.path.join(DB_FOLDER, "texts.pkl"), "wb") as f:
        pickle.dump({"texts": texts, "metadatas": metadatas}, f)

    return len(chunks)
