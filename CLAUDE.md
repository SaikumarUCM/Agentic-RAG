# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Install dependencies (local dev)
pip install -r requirements.txt

# Run the FastAPI chat server
uvicorn app.main:app --reload --port 8000

# Run Streamlit UI locally
streamlit run streamlit_app/app.py

# Run the full stack (Airflow + Qdrant + Streamlit)
docker-compose up --build
```

## Services & Ports

| Service           | Port  | Notes                        |
|-------------------|-------|------------------------------|
| FastAPI chat API  | 8000  | `uvicorn app.main:app`       |
| Airflow webserver | 8080  | user/pass: `airflow/airflow` |
| Qdrant REST API   | 6333  |                              |
| Streamlit UI      | 8501  |                              |

## Environment Variables (`.env`)

```
OPENAI_API_KEY=...
QDRANT_HOST=localhost   # use "qdrant" inside Docker Compose
QDRANT_PORT=6333
```

## Project Structure

```
├── app/                    # FastAPI application
│   ├── main.py             # routes: GET /, POST /chat
│   └── schemas.py          # PromptRequest pydantic model
│
├── rag/                    # URL-based ingestion + retrieval (OpenAI + Qdrant)
│   ├── ingestor.py         # ingest_url / ingest_urls → Qdrant "articles" collection
│   ├── text_splitter.py    # SeleniumURLLoader + RecursiveCharacterTextSplitter
│   └── retriever_tool.py   # LangChain retriever tool wrapping Qdrant
│
├── agent/
│   └── rag_agent.py        # LangGraph StateGraph (assistant ⇌ tools loop)
│
├── pipeline/               # File-based Airflow ingestion (SentenceTransformers + Qdrant)
│   ├── loader.py           # PDF / TXT / DOCX loaders
│   ├── chunker.py          # RecursiveCharacterTextSplitter (chunk=500, overlap=100)
│   ├── embedder.py         # intfloat/e5-base (dim=768, no API key needed)
│   ├── vector_store.py     # Qdrant upsert → "documents" collection
│   └── build_index.py      # Airflow callable: load → chunk → embed → store
│
├── dags/
│   └── rag_ingest_dag.py   # Airflow DAG (no schedule, triggered via REST API)
│
├── streamlit_app/
│   └── app.py              # Upload UI → saves file → triggers Airflow DAG
│
└── storage/uploads/        # Drop folder for uploaded documents
```

## Architecture

There are two ingestion paths, both backed by **Qdrant**:

### Path 1 — URL ingestion (chat API)
```
POST /chat (app/main.py)
  → ingest_url (rag/ingestor.py)          [if url provided]
      → SeleniumURLLoader + splitter
      → OpenAI text-embedding-3-small (dim=1536)
      → Qdrant collection: "articles"
  → agent() (agent/rag_agent.py)
      → GPT-4o-mini + retriever_tool
      → retriever_tool queries "articles" collection (k=2)
```

### Path 2 — File ingestion (Airflow pipeline)
```
Streamlit upload → storage/uploads/
  → Airflow REST API → rag_ingest_dag
      → pipeline/build_index.py
          → loader (PDF/TXT/DOCX)
          → chunker (chunk=500, overlap=100)
          → intfloat/e5-base embeddings (dim=768)
          → Qdrant collection: "documents"
```

**Two separate Qdrant collections** because the embedding models differ (OpenAI 1536-dim vs e5-base 768-dim).

**LangGraph agent loop:** `START → assistant → (tool call?) → tools → assistant → … → END`
Uses `MessagesState` to carry the full message history through the loop.
