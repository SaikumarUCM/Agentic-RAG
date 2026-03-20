# Agentic RAG Application

An intelligent Retrieval-Augmented Generation (RAG) application powered by LangGraph, OpenAI, and Qdrant. Features a FastAPI chat backend, a Streamlit upload UI, and an Apache Airflow pipeline for automated document ingestion — all orchestrated via Docker Compose.

## Features

- **Agentic Workflow**: LangGraph `StateGraph` orchestrates a multi-step assistant ↔ tools reasoning loop
- **Dual Ingestion Paths**: URL-based ingestion (OpenAI embeddings) and file-based ingestion (Airflow + SentenceTransformers)
- **Vector Search**: Qdrant for efficient semantic search across two collections (`articles` and `documents`)
- **FastAPI Chat API**: REST endpoint (`POST /chat`) that accepts a prompt and optional URL, then returns an AI-generated response
- **Streamlit UI**: Drag-and-drop document upload that triggers an Airflow DAG for processing
- **Airflow Pipeline**: Automated PDF / TXT / DOCX ingestion with chunking and embedding — no API key required
- **OpenAI Integration**: GPT-4o-mini for response generation; `text-embedding-3-small` for URL-based embeddings
- **Message History**: Full conversation context preserved through LangGraph `MessagesState`

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
├── storage/uploads/        # Drop folder for uploaded documents
├── docker-compose.yml
├── requirements.txt
└── .env                    # OPENAI_API_KEY, QDRANT_HOST, QDRANT_PORT
```

## Architecture

Two ingestion paths share **Qdrant** as the vector store but use separate collections because the embedding dimensions differ.

### Path 1 — URL ingestion (chat API)

```
POST /chat (app/main.py)
  → ingest_url (rag/ingestor.py)          [if url provided]
      → SeleniumURLLoader + text splitter
      → OpenAI text-embedding-3-small (dim=1536)
      → Qdrant collection: "articles"
  → agent() (agent/rag_agent.py)
      → GPT-4o-mini + retriever_tool
      → retriever_tool queries "articles" (k=2)
```

### Path 2 — File ingestion (Airflow pipeline)

```
Streamlit upload → storage/uploads/
  → Airflow REST API → rag_ingest_dag
      → pipeline/build_index.py
          → loader (PDF / TXT / DOCX)
          → chunker (chunk=500, overlap=100)
          → intfloat/e5-base embeddings (dim=768)
          → Qdrant collection: "documents"
```

## Services & Ports

| Service           | Port | Notes                        |
| ----------------- | ---- | ---------------------------- |
| FastAPI chat API  | 8000 | `uvicorn app.main:app`       |
| Airflow webserver | 8080 | user/pass: `airflow/airflow` |
| Qdrant REST API   | 6333 |                              |
| Streamlit UI      | 8501 |                              |

## Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- OpenAI API key

### Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-api-key-here
QDRANT_HOST=qdrant        # use "localhost" for local dev outside Docker
QDRANT_PORT=6333
```

### Run with Docker Compose (recommended)

```bash
docker-compose up --build
```

This starts Qdrant, Airflow (webserver + scheduler), and the Streamlit UI together.

### Run locally (development)

```bash
# Install dependencies
pip install -r requirements.txt

# Start the FastAPI chat server
uvicorn app.main:app --reload --port 8000

# Start the Streamlit UI (separate terminal)
streamlit run streamlit_app/app.py
```

> Airflow and Qdrant still need to be running (via Docker or locally) for full functionality.

## Usage

### Chat API

```bash
# Simple prompt
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is retrieval-augmented generation?"}'

# Prompt with URL ingestion
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Summarise this article", "url": "https://example.com/article"}'
```

### Document Upload (Streamlit)

1. Open `http://localhost:8501`
2. Upload a PDF, TXT, or DOCX file
3. The UI saves it to `storage/uploads/` and triggers the Airflow DAG
4. Monitor progress at `http://localhost:8080` (airflow / airflow)

## Configuration

| Setting         | Value                               | Location                |
| --------------- | ----------------------------------- | ----------------------- |
| LLM             | `gpt-4o-mini`                       | `agent/rag_agent.py`    |
| URL embeddings  | `text-embedding-3-small` (1536-dim) | `rag/ingestor.py`       |
| File embeddings | `intfloat/e5-base` (768-dim)        | `pipeline/embedder.py`  |
| Chunk size      | 500 tokens (file), variable (URL)   | `pipeline/chunker.py`   |
| Chunk overlap   | 100 tokens                          | `pipeline/chunker.py`   |
| Retriever top-k | 2                                   | `rag/retriever_tool.py` |

## Key Dependencies

- **langgraph** — agent orchestration and state management
- **langchain / langchain-community** — LLM framework and loaders
- **langchain-openai** — OpenAI LLM + embeddings
- **qdrant-client** — Qdrant vector store client
- **apache-airflow** — pipeline scheduling and orchestration
- **sentence-transformers** — local embeddings for file ingestion (`e5-base`)
- **fastapi / uvicorn** — chat REST API
- **streamlit** — document upload UI
- **python-dotenv** — environment variable management

## Security

**Never commit your `.env` file.** It is listed in `.gitignore`. Keep your `OPENAI_API_KEY` out of version control.

## Troubleshooting

**ModuleNotFoundError** — activate the virtual environment and install dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Qdrant connection error** — ensure Qdrant is running. With Docker Compose use `QDRANT_HOST=qdrant`; for local dev use `QDRANT_HOST=localhost`.

**Airflow DAG not triggering** — check that the Airflow webserver and scheduler are both running and that `storage/uploads/` is accessible.

**Selenium / URL ingestion errors** — a compatible ChromeDriver must be installed and on your `PATH`.

## Contributing

Feel free to fork this project and submit pull requests for improvements.

## License

This project is open source. See LICENSE file for details.

---

**Built with LangChain + LangGraph + OpenAI + Qdrant + Airflow**
