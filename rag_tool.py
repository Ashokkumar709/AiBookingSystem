from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_rag(pdf_paths):
    docs = []

    for path in pdf_paths:
        try:
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        except Exception as e:
            print(f"⚠ Skipping invalid PDF: {path} | Error: {e}")

    if not docs:
        raise ValueError("No valid PDF content found.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.from_documents(chunks, embeddings)
