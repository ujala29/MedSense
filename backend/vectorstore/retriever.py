from backend.vectorstore.chroma_client import get_collection
from backend.vectorstore.embedder import get_embeddings

def retrieve_context(query: str, report_id: str, n_results: int = 5) -> list[str]:
    collection = get_collection()
    query_embedding = get_embeddings([query])[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results, where={"report_id": report_id})
    return results['documents'][0] if results['documents'] else []

def retrieve_historical(patient_id: str, n_results: int = 10) -> list[str]:
    collection = get_collection()
    results = collection.get(where={"patient_id": patient_id})
    docs = results.get('documents') or []
    return docs[:n_results] if docs else []