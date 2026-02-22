# rag.py
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama

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
    # 1. Charger la base
    index, texts, metadatas = load_db()

    # 2. Chercher les chunks pertinents
    chunks = search(question, index, texts)
    context = "\n\n".join(chunks)

    # 3. Construire le prompt
    prompt = f"""Tu es un assistant qui répond aux questions en te basant uniquement sur le contexte fourni.

Contexte :
{context}

Question : {question}

Réponds en français de manière précise et concise."""

    # 4. Appeler Mistral via Ollama
    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

if __name__ == "__main__":
    print("Chatbot RAG - tape 'quit' pour quitter\n")
    index, texts, metadatas = load_db()
    while True:
        question = input("Ta question : ")
        if question.lower() == "quit":
            break
        reponse = ask(question)
        print(f"\nReponse : {reponse}\n") 