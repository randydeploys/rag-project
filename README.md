# RAG Chatbot - Question sur vos documents

Un chatbot intelligent capable de répondre à des questions sur vos propres documents PDF,
en utilisant la technique RAG (Retrieval-Augmented Generation).

## Stack technique
- **LangChain** — orchestration du pipeline RAG
- **sentence-transformers** — génération des embeddings (100% local)
- **ChromaDB** — base de données vectorielle
- **Ollama + Mistral** — LLM local et gratuit
- **PyMuPDF** — lecture des PDFs
- **Streamlit** — interface utilisateur

## Installation

### 1. Cloner le repo
git clone https://github.com/randydeploys/rag-project.git
cd rag-project

### 2. Créer et activer l'environnement virtuel
python -m venv venv
venv\Scripts\activate

### 3. Installer les dépendances
pip install -r requirements.txt

### 4. Installer Ollama
Télécharger sur https://ollama.com puis lancer :
ollama pull mistral

## Utilisation

## Structure du projet
rag-project/
├── docs/          → vos PDFs
├── db/            → base ChromaDB (générée automatiquement)
├── app.py         → interface Streamlit
├── ingest.py      → indexation des documents
├── rag.py         → pipeline de recherche et réponse
└── requirements.txt
