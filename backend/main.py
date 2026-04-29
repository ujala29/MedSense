from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import json
from backend.ingestion.pdf_parser import extract_from_pdf
from backend.ingestion.image_processor import preprocess_image
from backend.ingestion.chunker import chunk_text
from backend.vectorstore.chroma_client import add_report, get_collection
from backend.agents.graph import compiled_graph, AgentState

class AnalyzeRequest(BaseModel):
    report_id: str
    patient_id: str
    language: str = "en"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    patient_id: str = Form(...),
    language: str = Form("en"),
    age: int = Form(...),
    gender: str = Form(...),
):
    report_id = str(uuid.uuid4())
    file_bytes = await file.read()
    if file.filename.endswith('.pdf'):
        data = extract_from_pdf(file_bytes)
    else:
        data = {"text": preprocess_image(file_bytes), "tables": [], "metadata": {}, "page_count": 1}
    chunks = chunk_text(data["text"])
    metadata = {"report_id": report_id, "patient_id": patient_id, "age": age, "gender": gender, "language": language}
    add_report(report_id, chunks, metadata)
    return {"report_id": report_id, "page_count": data["page_count"], "status": "processed"}

@app.post("/analyze")
async def analyze(request_body: dict):
    report_id = request_body.get("report_id")
    patient_id = request_body.get("patient_id")
    language = request_body.get("language", "en")
    
    collection = get_collection()
    results = collection.get(where={"report_id": report_id})
    report_text = " ".join(results['documents']) if results.get('documents') else ""
    # Assume patient_profile from metadata
    metas = results['metadatas']
    if metas:
        meta = metas[0]
        patient_profile = {"patient_id": patient_id, "age": meta["age"], "gender": meta["gender"]}
    else:
        patient_profile = {"patient_id": patient_id, "age": 0, "gender": "unknown"}
    initial_state = AgentState(
        report_text=report_text,
        report_id=report_id,
        patient_profile=patient_profile,
        language=language,
        retrieved_chunks=[],
        analysis_result=None,
        diet_result=None,
        comparison_result=None,
        final_response=None,
        sources=[],
        errors=[],
    )
    async def generate():
        try:
            async for event in compiled_graph.astream(initial_state):
                for node, state in event.items():
                    if node == "analyzer" and state.get("analysis_result"):
                        print(f"[SSE] Emitting analysis: {len(state['analysis_result'])} chars")
                        yield f"data: {json.dumps({'type': 'analysis', 'content': state['analysis_result']})}\n\n"
                    elif node == "diet":
                        diet_text = state.get("diet_result") or ""
                        print(f"[SSE] Emitting diet: {len(diet_text)} chars")
                        yield f"data: {json.dumps({'type': 'diet', 'content': diet_text})}\n\n"
                    elif node == "comparator":
                        comparison_text = state.get("comparison_result") or ""
                        print(f"[SSE] Emitting comparison: {len(comparison_text)} chars")
                        yield f"data: {json.dumps({'type': 'comparison', 'content': comparison_text})}\n\n"
                    elif node == "synthesizer":
                        yield f"data: {json.dumps({'type': 'sources', 'sources': state.get('sources', [])})}\n\n"
                        yield f"data: {json.dumps({'type': 'done'})}\n\n"
        except Exception as e:
            print(f"[SSE ERROR] {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/reports/{patient_id}")
async def get_reports(patient_id: str):
    collection = get_collection()
    results = collection.get(where={"patient_id": patient_id})
    reports = []
    for meta in results['metadatas']:
        reports.append({"report_id": meta["report_id"], "date": meta.get("date", "unknown")})
    return reports