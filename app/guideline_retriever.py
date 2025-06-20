# guideline_retriever.py
import os
import streamlit as st
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from chromadb.config import Settings

# Get API key from secrets
api_key = st.secrets.get("CHROMA_OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))
if not api_key:
    raise ValueError("OPENAI_API_KEY or CHROMA_OPENAI_API_KEY must be set in ../.streamlit/secrets.toml")

# Set it in os.environ for Chroma internals
os.environ["CHROMA_OPENAI_API_KEY"] = api_key

# Initialize Chroma with OpenAI embeddings
def load_guideline_collection():
    embedding_fn = OpenAIEmbeddingFunction(api_key=os.getenv("CHROMA_OPENAI_API_KEY"))
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./chroma_guidelines"
    ))
    collection = client.get_or_create_collection(name="clinical_guidelines", embedding_function=embedding_fn)

    # ✅ Add sample documents if collection is empty
    if collection.count() == 0:
        documents = [
            "Trigeminal neuralgia typically causes unilateral facial pain.",
            "Facial numbness is atypical for trigeminal neuralgia and may suggest another cause.",
            "A dental workup is recommended if pain is localized to the jaw with no neurological findings.",
            "MRI is advised when pain persists or neurological symptoms are present.",
            "Neurologist referral is warranted for sensory loss or motor deficits."
        ]
        ids = [f"guideline-{i}" for i in range(len(documents))]
        collection.add(documents=documents, ids=ids)

    return collection

def retrieve_guideline_snippet(history_text, top_k=1):
    collection = load_guideline_collection()
    results = collection.query(query_texts=[history_text], n_results=top_k)

    if results["documents"] and len(results["documents"][0]) > 0:
        return results["documents"][0]
    else:
        return ["No guideline match found."]
