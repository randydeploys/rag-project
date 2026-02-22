# app.py
import streamlit as st
from rag import ask, load_db

# Configuration de la page
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="robot",
    layout="centered"
)

st.title("RAG Chatbot")
st.caption("Posez vos questions sur vos documents PDF")

# Charger la base une seule fois
@st.cache_resource
def init_db():
    return load_db()

index, texts, metadatas = init_db()

# Historique de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if question := st.chat_input("Posez votre question..."):

    # Afficher la question
    with st.chat_message("user"):
        st.markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Générer la réponse
    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            reponse = ask(question)
        st.markdown(reponse)
    st.session_state.messages.append({"role": "assistant", "content": reponse})