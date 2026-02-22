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
markdown
# RAG Chatbot - Question sur vos documents

Chatbot local et gratuit capable de repondre a des questions sur vos propres documents PDF,
en utilisant la technique RAG (Retrieval-Augmented Generation).
Aucune donnee ne quitte votre machine.

## Fonctionnalites

- Chargement de plusieurs PDFs simultanement
- Recherche semantique par le sens, pas seulement par mots-cles
- Reponses generees localement sans API payante
- Interface web simple via Streamlit
- Sources citees dans chaque reponse

## Stack technique

| Outil | Role |
|---|---|
| LangChain | Orchestration du pipeline RAG |
| sentence-transformers | Generation des embeddings (100% local) |
| ChromaDB | Base de donnees vectorielle |
| Ollama + Mistral | LLM local et gratuit |
| PyMuPDF | Lecture et extraction des PDFs |
| Streamlit | Interface utilisateur |

## Prerequis

- Python 3.10+
- 8 Go de RAM minimum (16 Go recommande)
- Ollama installe sur votre machine

## Installation

### 1. Cloner le repo

```bash
git clone https://github.com/randydeploys/rag-project.git
cd rag-project
```

### 2. Créer et activer l'environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate
```


### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Installer Ollama
Télécharger sur https://ollama.com puis lancer :
```bash
ollama pull mistral
```

## Utilisation

## Structure du projet

```
rag-project/
├── docs/               -> vos PDFs
├── db/                 -> base ChromaDB (generee automatiquement)
├── app.py              -> interface Streamlit
├── ingest.py           -> indexation des documents
├── rag.py              -> pipeline de recherche et reponse
└── requirements.txt    -> dependances du projet
```

## Auteur

Randy - [GitHub](https://github.com/randydeploys)
