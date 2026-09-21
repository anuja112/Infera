from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import init_db
from app.api import ingest, documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database connection and create tables if they don't exist.
    init_db()
    yield
    
app = FastAPI(
    title="Infera - Document Intelligence & Retrieval Platform",
    description="A grounded, citation-backed RAG API powered by Gemini.",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(ingest.router)
app.include_router(documents.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}