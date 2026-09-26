# Infera — Document Intelligence Platform

Infera is a document-based question-answering platform that lets users
interact with their own PDF, TXT, and Markdown documents.

Instead of relying only on semantic vector search, Infera combines
vector retrieval with keyword-based retrieval, reranking, and a
grounded generation pipeline to improve the relevance and reliability
of answers.

The system retrieves supporting passages from the uploaded documents,
generates answers using the retrieved context, and provides citations
so that users can trace an answer back to its source.

---

## Overview

Traditional RAG applications often depend entirely on vector similarity.
While semantic retrieval works well for conceptual questions, it can
struggle with exact terms, names, identifiers, acronyms, and other
important keywords.

Infera addresses this using a hybrid retrieval pipeline:

- **FAISS** for semantic/vector retrieval
- **BM25** for lexical/keyword retrieval
- **Reciprocal Rank Fusion (RRF)** to combine retrieval results
- **Cross-encoder reranking** to refine the most relevant chunks
- **Gemini** for query processing and answer generation
- **LangGraph** for orchestrating the RAG workflow
- **Citation-based responses** for better traceability
- **Groundedness checking** to identify unsupported answers

The project also includes an evaluation pipeline to compare different
retrieval strategies rather than assuming that hybrid retrieval is
automatically better.

---

## System Architecture

### Document Ingestion

```text
File Upload
     ↓
Document Parsing
     ↓
Text Extraction
     ↓
Chunking
     ↓
Gemini Embeddings
     ↓
SQLite + FAISS