from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import os


def simple_text_splitter(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


class SimpleVectorStore:
    def __init__(self, texts, embeddings, index):
        self.texts = texts
        self.embeddings = embeddings
        self.index = index

    def similarity_search(self, query, k=3):
        query_emb = self.embeddings.encode([query])
        distances, indices = self.index.search(query_emb, k)
        return [self.texts[i] for i in indices[0]]


def build_rag(pdf_paths):
    all_text = ""

    for path in pdf_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            all_text += page.extract_text() or ""

    chunks = simple_text_splitter(all_text)

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return SimpleVectorStore(chunks, model, index)
