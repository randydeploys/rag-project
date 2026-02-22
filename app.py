# app.py
import streamlit as st
import os
from pipeline import ingest_documents
from rag import ask, load_db

DOCS_FOLDER = "docs"
DB_FOLDER = "db"

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="robot",
    layout="centered"
)

st.title("RAG Chatbot")
st.caption("Posez vos questions sur vos documents PDF")

# Sidebar
with st.sidebar:
    st.header("Vos documents")

    # Upload de PDFs
    uploaded_files = st.file_uploader(
        "Ajouter des PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Indexer les documents"):
        with st.spinner("Indexation en cours..."):
            os.makedirs(DOCS_FOLDER, exist_ok=True)
            pdf_paths = []
            for file in uploaded_files:
                path = os.path.join(DOCS_FOLDER, file.name)
                with open(path, "wb") as f:
                    f.write(file.read())
                pdf_paths.append(path)

            num_chunks = ingest_documents(pdf_paths)
            st.cache_resource.clear()

        st.success(f"{num_chunks} chunks indexés !")

    # Liste des PDFs indexés
    if os.path.exists(DOCS_FOLDER):
        pdfs = [f for f in os.listdir(DOCS_FOLDER) if f.endswith(".pdf")]
        if pdfs:
            st.subheader("Documents indexés")
            for pdf in pdfs:
                st.write(f"- {pdf}")

            # Supprimer un PDF
            st.subheader("Supprimer un document")
            pdf_to_delete = st.selectbox("Choisir un PDF", pdfs)
            if st.button("Supprimer"):
                os.remove(os.path.join(DOCS_FOLDER, pdf_to_delete))
                st.success(f"{pdf_to_delete} supprimé !")
                st.rerun()

# Charger la base
@st.cache_resource
def init_db():
    return load_db()

# Vérifier si des documents sont indexés
docs_vides = not os.path.exists(DOCS_FOLDER) or not any(
    f.endswith(".pdf") for f in os.listdir(DOCS_FOLDER)
)
db_vide = not os.path.exists(os.path.join(DB_FOLDER, "index.faiss"))

if docs_vides or db_vide:
    st.info("Aucun document indexé. Ajoutez des PDFs dans le panneau de gauche et cliquez sur 'Indexer les documents'.")
    st.stop()

try:
    index, texts, metadatas = init_db()
except Exception as e:
    st.error(f"Erreur lors du chargement de la base : {e}")
    st.stop()

# Historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Bouton vider historique
if st.button("Vider l'historique"):
    st.session_state.messages = []
    st.rerun()

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if question := st.chat_input("Posez votre question..."):
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            reponse, sources = ask(question)
        st.markdown(reponse)

        if sources:
            with st.expander("Sources utilisees"):
                for source in sources:
                    st.write(f"- {source}")

    st.session_state.messages.append({"role": "assistant", "content": reponse})