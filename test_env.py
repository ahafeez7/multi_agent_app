# test_env.py

import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st

try:
    import chromadb
    from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

    st.success("✅ chromadb and protobuf loaded successfully!")
except Exception as e:
    st.error(f"❌ Failed to load chromadb: {e}")