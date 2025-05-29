import os
import json
import chromadb
from pathlib import Path
from sentence_transformers import SentenceTransformer
import streamlit as st
from chromadb.api.types import EmbeddingFunction

# --- Chroma-compatible EmbeddingFunction ---
class ClinicalBERTEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = None
        self.dimensions = 768

    def _load_model(self):
        if self.model is None:
            self.model = SentenceTransformer("pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb")

    def __call__(self, input):
        self._load_model()
        return self.model.encode(input, show_progress_bar=False).tolist()

    @property
    def name(self):
        return "Bio_ClinicalBERT"

    def name(self):
        return "Bio_ClinicalBERT"

# --- Initialization Wrapper to Avoid Premature Streamlit Calls ---
def initialize_embeddings():
    with st.spinner("🔄 Loading BioBERT model and embedding patients..."):
        with open("patients.json", "r") as f:
            patient_options = json.load(f)

        embedding_function = ClinicalBERTEmbeddingFunction()
        client = chromadb.PersistentClient(path="./chroma_clinical_notes")
        collection = client.get_or_create_collection(
            name="clinical_notes",
            embedding_function=embedding_function
        )

        for patient_name, history in patient_options.items():
            history_text = "\n".join([f"{k}: {v}" for k, v in history.items()])
            collection.add(
                documents=[history_text],
                ids=[f"patient_{patient_name.replace(' ', '_')}"],
                metadatas=[{"patient": patient_name}]
            )
        return collection

# --- Retrieval Function ---
def retrieve_similar_patients(collection, history_input, top_k=3):
    results = collection.query(query_texts=[history_input], n_results=top_k)
    return [
        {
            "patient_id": result_id,
            "score": round(score, 4),
            "matched_note": doc
        }
        for result_id, score, doc in zip(
            results["ids"][0],
            results["distances"][0],
            results["documents"][0]
        )
    ]

# --- Optional Standalone Streamlit Interface ---
if __name__ == "__main__":
    st.set_page_config(page_title="Similar Patient Retriever")
    st.title("🔍 Similar Patient Retriever")
    collection = initialize_embeddings()
    input_text = st.text_area("Enter patient complaint / history")

    if st.button("Retrieve Similar Patients") and input_text.strip():
        matches = retrieve_similar_patients(collection, input_text)
        st.markdown("### 🔁 Top Similar Patients (Before Doctor Reasoning)")
        for match in matches:
            st.markdown(f"**Patient ID:** {match['patient_id']}")
            st.markdown(f"**Similarity Score:** {match['score']}")
            st.markdown(f"**Matched Note:**\n{match['matched_note']}")
            st.markdown("---")
        st.markdown("### 🧠 Proceeding to Doctor Reasoning...")
        st.markdown("### 🔁 Top Similar Patients (After Doctor Reasoning)")
        for match in matches:
            st.markdown(f"**Patient ID:** {match['patient_id']}")
            st.markdown(f"**Similarity Score:** {match['score']}")
            st.markdown(f"**Matched Note:**\n{match['matched_note']}")
            st.markdown("---")
