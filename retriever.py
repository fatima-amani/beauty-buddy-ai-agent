import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index and documents
index = faiss.read_index("faiss_index.idx")
with open("doc_store.pkl", "rb") as f:
    documents = pickle.load(f)


def retrieve_top_k(query, k=3):
    """Retrieve top-k relevant documents based on query."""
    query_embedding = embedder.encode([query])
    distances, indices = index.search(query_embedding, k)
    results = [documents[i] for i in indices[0]]
    return results


# print(retrieve_top_k("foundation"))


def generate_response(query):
    """Retrieve relevant content and generate response."""
    retrieved_docs = retrieve_top_k(query)
    context = "\n".join(retrieved_docs)

    # Send to Mistral LLM
    prompt = f"Here are some beauty tips:\n{context}\n\nUser Query: {query}\nAnswer: "
    response = mistral.generate(prompt=prompt, model="mistral")

    return response["choices"][0]["text"]
