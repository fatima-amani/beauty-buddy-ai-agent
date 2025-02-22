# Install dependencies
# !pip install faiss-cpu sentence-transformers pymupdf

import faiss
import pickle
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# List of PDF file paths
pdf_paths = ["C:/Users/Fatima/Downloads/makeup_tutorial.pdf"]  # Add your PDF paths here

# Extract text from PDFs using fitz
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Load beauty tips from PDFs
documents = []
for pdf_path in pdf_paths:
    text = extract_text_from_pdf(pdf_path)
    documents.append(text)

# Generate embeddings
doc_embeddings = embedder.encode(documents)

# Store in FAISS
index = faiss.IndexFlatL2(doc_embeddings.shape[1])
index.add(doc_embeddings)

# Save FAISS index
faiss.write_index(index, "faiss_index.idx")

# Save documents for retrieval mapping
with open("doc_store.pkl", "wb") as f:
    pickle.dump(documents, f)

# print("FAISS index and document store created!")

