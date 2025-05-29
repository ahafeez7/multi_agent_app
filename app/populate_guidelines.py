# populate_guidelines.py
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os
from dotenv import load_dotenv

load_dotenv()

# Sample guideline chunks (realistic but paraphrased)
GUIDELINE_SNIPPETS = [
    "Trigeminal neuralgia is characterized by sudden, severe, brief stabbing pain in the distribution of one or more branches of the trigeminal nerve.",
    "The pain of trigeminal neuralgia is typically unilateral and triggered by light touch, chewing, or talking.",
    "MRI with a trigeminal nerve protocol is recommended to evaluate for secondary causes such as multiple sclerosis or neurovascular compression.",
    "Differentiating dental pain from trigeminal neuralgia involves identifying absence of inflammation, swelling, or persistent aching.",
    "First-line treatment includes carbamazepine or oxcarbazepine. Referral to neurology is advised when diagnosis is uncertain or treatment fails."
]

def populate_guideline_chroma():
    embedding_fn = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))
    client = chromadb.PersistentClient(path="./chroma_guidelines")
    collection = client.get_or_create_collection("clinical_guidelines", embedding_function=embedding_fn)

    for i, snippet in enumerate(GUIDELINE_SNIPPETS):
        collection.add(
            documents=[snippet],
            ids=[f"guideline_{i}"],
            metadatas=[{"source": "TN_guideline"}]
        )

    print("✅ Clinical guideline snippets added to Chroma.")

if __name__ == "__main__":
    populate_guideline_chroma()