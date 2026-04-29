import chromadb
from backend.config import settings
from backend.vectorstore.embedder import get_embeddings

client = chromadb.PersistentClient(path=settings.chroma_persist_dir)

def get_collection(name: str = "medical_reports"):
    return client.get_or_create_collection(name=name)

def add_report(report_id: str, chunks: list[str], metadata: dict):
    collection = get_collection()
    ids = [f"{report_id}_{i}" for i in range(len(chunks))]
    metadatas = [metadata] * len(chunks)
    embeddings = get_embeddings(chunks)
    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=chunks)