from fastapi import FastAPI

app = FastAPI(
    title="Infera - Document Intelligence & Retrieval Platform",
    description="A grounded, citation-backed RAG API powered by Gemini.",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}