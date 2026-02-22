# rag.py
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

DB_FOLDER = "db"

def load_db():
    index = faiss.read_index(os.path.join(DB_FOLDER, "index.faiss"))
    with open(os.path.join(DB_FOLDER, "texts.pkl"), "rb") as f:
        data = pickle.load(f)
    return index, data["texts"], data["metadatas"]

def search(question, index, texts, k=7):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    question_embedding = model.encode([question])
    distances, indices = index.search(np.array(question_embedding), k)
    results = [texts[i] for i in indices[0]]
    return results

def ask(question):
    index, texts, metadatas = load_db()
    chunks = search(question, index, texts)
    context = "\n\n".join(chunks)

    prompt = f"""Tu es un assistant qui répond aux questions en te basant uniquement sur le contexte fourni.

Contexte :
{context}

Question : {question}

Réponds en français de manière précise et concise."""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extraire les noms de fichiers uniques
    sources = list(set([
        m.get("source", "inconnu").split("\\")[-1]
        for m in metadatas
    ]))

    return response["message"]["content"], sources

if __name__ == "__main__":
    print("Chatbot RAG - tape 'quit' pour quitter\n")
    index, texts, metadatas = load_db()
    while True:
        question = input("Ta question : ")
        if question.lower() == "quit":
            break
        reponse = ask(question)
        print(f"\nReponse : {reponse}\n") 