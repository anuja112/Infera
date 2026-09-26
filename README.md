# Infera - A Retrieval-First Document Intelligence Platform

A document question-answering system that turns PDF, TXT, and Markdown
files into a searchable knowledge base. Infera combines dense retrieval,
lexical search, rank fusion, reranking, and LLM-based generation to
produce answers that are tied back to the source documents.

Built with FastAPI, Gemini, FAISS, BM25, a cross-encoder reranker,
LangGraph, and Streamlit.

## What makes it different

Infera is designed around the retrieval and verification stages of RAG,
rather than treating vector search and generation as a single black box:

- **Dense + lexical retrieval.** FAISS handles semantic similarity while
  BM25 captures exact terms and keyword matches. Their ranked results are
  merged using **Reciprocal Rank Fusion (RRF)** before reranking.

- **Two-stage retrieval.** Retrieval is optimized for candidate coverage,
  while the cross-encoder performs a second relevance pass to improve the
  ordering of the final context.

- **Evidence-based generation.** Gemini receives the retrieved chunks as
  context and generates citation-backed responses. When the available
  evidence is insufficient, the system is designed to avoid inventing an
  answer.

- **Post-generation validation.** A separate LLM verification step checks
  whether the generated response is actually supported by the retrieved
  evidence.

- **Rebuildable indexing.** SQLite stores the canonical document and chunk
  data, while FAISS acts as a derived vector index. Chunk IDs are reused
  as vector IDs to maintain a deterministic link between stored text and
  embeddings.

- **Resilient execution.** Temporary Gemini/API failures are handled with
  retries and backoff, while optional reranking can be skipped if the
  reranker is unavailable.

- **Fresh results after updates.** Response caching is invalidated when
  the document collection changes, preventing previously generated
  answers from becoming stale.

## Architecture

```text
DOCUMENT INGESTION

PDF / TXT / MD
      │
      ▼
   Parser
      │
      ▼
 Text Extraction
      │
      ▼
 Chunking
      │
      ▼
 Gemini Embedding
      │
      ├──────────────► SQLite
      │                 (source of truth)
      │
      └──────────────► FAISS
                        (vector index)


QUESTION ANSWERING

User Question
      │
      ▼
Query Rewriting
      │
      ├──────────────► FAISS ──► Semantic Results
      │
      └──────────────► BM25  ──► Keyword Results
                              │
                              ▼
                         RRF Fusion
                              │
                              ▼
                       Candidate Chunks
                              │
                              ▼
                    Cross-Encoder Reranking
                              │
                              ▼
                      Selected Context
                              │
                              ▼
                       Gemini Generation
                              │
                              ▼
                    Citation-backed Answer
                              │
                              ▼
                    Groundedness Verification
```

## Tech stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| Data layer | SQLite + SQLModel |
| LLM / Embeddings | Google Gemini |
| Dense retrieval | FAISS (`IndexFlatIP`) |
| Sparse retrieval | BM25 (`rank_bm25`) |
| Fusion | Reciprocal Rank Fusion (RRF) |
| Reranking | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| Workflow | LangGraph |
| UI | Streamlit |
| Deployment | Docker Compose |

## Getting started

### Docker

```bash
git clone <your-repo-url>
cd Infera

cp .env.example .env        # add your Gemini API key

docker compose up --build
```

Once the services are running:

- Frontend: `http://localhost:8501`
- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

### Local development

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
```

In a separate terminal:

```bash
# Frontend
cd frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

streamlit run app.py
```

For Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Add your Gemini API key to `.env` before starting the application.

## Evaluation

The evaluation module is used to compare retrieval strategies on
questions defined in `eval/eval_dataset.json`.

```bash
cd eval
pip install -r requirements.txt
python run_eval.py
```

The experiment compares:

```text
Vector Search
Keyword Search
Hybrid Retrieval
Hybrid + Reranking
```

The evaluation reports **Recall@5**, along with end-to-end answer
accuracy, groundedness, and latency across the pipeline stages.

Add the results from your own evaluation run here:

```text
<PASTE YOUR run_eval.py OUTPUT HERE>
```

## API reference

The complete API can be explored through `/docs`.

| Endpoint | Description |
|---|---|
| `POST /ingest` | Accept a document and start ingestion |
| `GET /jobs/{id}` | Track an ingestion job |
| `GET /documents` | Retrieve indexed document information |
| `DELETE /documents/{id}` | Remove an indexed document |
| `POST /search` | Execute retrieval using a selected mode |
| `POST /query` | Execute the complete RAG workflow |

## Project structure

```text
Infera/
├── backend/
│   └── app/
│       ├── api/           # ingestion, documents, search, query routes
│       ├── ingestion/     # parsers, chunking, ingestion workflow
│       ├── retrieval/     # embeddings, FAISS, BM25, fusion, reranking
│       ├── graph/         # LangGraph state and pipeline nodes
│       ├── cache/         # response cache and invalidation
│       ├── db/            # SQLModel models and database session
│       ├── schemas/       # API schemas
│       ├── config.py
│       ├── gemini_client.py
│       └── main.py
├── frontend/
│   └── app.py             # Streamlit interface
├── eval/
│   ├── eval_dataset.json  # evaluation questions
│   ├── run_eval.py        # retrieval/e2e evaluation
│   └── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```
