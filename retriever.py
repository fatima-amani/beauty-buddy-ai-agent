import faiss
import pickle
import numpy as np
from langchain_core.prompt_values import ChatPromptValue
from sentence_transformers import SentenceTransformer

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index and documents
index = faiss.read_index("faiss_index.idx")
with open("doc_store.pkl", "rb") as f:
    documents = pickle.load(f)


def retrieve_top_k(query, k=3):
    """Retrieve top-k relevant documents based on query."""
    if isinstance(query, ChatPromptValue):
        query = query.to_string()  # Convert ChatPromptValue to string
    query_embedding = embedder.encode([query])
    distances, indices = index.search(query_embedding, k)
    results = [documents[i] for i in indices[0]]
    return results


# print(retrieve_top_k("foundation"))
