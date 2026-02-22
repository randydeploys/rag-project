# ingest.py
import os
import pickle
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Dossiers
DOCS_FOLDER = "docs"
DB_FOLDER = "db"

def ingest():
    # 1. Charger tous les PDFs
    documents = []
    for file in os.listdir(DOCS_FOLDER):
        if file.endswith(".pdf"):
            print(f"Chargement : {file}")
            loader = PyMuPDFLoader(os.path.join(DOCS_FOLDER, file))
            documents.extend(loader.load())

    if not documents:
        print("Aucun PDF trouve dans le dossier docs/")
        return

    print(f"{len(documents)} pages chargees")

    # 2. Découper en chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"{len(chunks)} chunks créés")

    # 3. Créer les embeddings
    print("Chargement du modèle d'embeddings...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    print("Création des embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    # 4. Stocker dans FAISS
    print("Stockage dans FAISS...")
    os.makedirs(DB_FOLDER, exist_ok=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    faiss.write_index(index, os.path.join(DB_FOLDER, "index.faiss"))

    with open(os.path.join(DB_FOLDER, "texts.pkl"), "wb") as f:
        pickle.dump({"texts": texts, "metadatas": metadatas}, f)

    print(f"Termine ! {len(chunks)} chunks stockes dans FAISS")

if __name__ == "__main__":
    ingest()