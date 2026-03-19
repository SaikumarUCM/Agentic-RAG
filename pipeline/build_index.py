from pipeline.loader import load_docs
from pipeline.chunker import chunk_docs
from pipeline.embedder import embed_chunks
from pipeline.vector_store import store_vectors


def run_build_index(**context):
    file_path = context["dag_run"].conf["file_path"]
    print(f"Building index for: {file_path}")

    docs = load_docs(file_path)
    print(f"Loaded {len(docs)} document(s)")

    chunks = chunk_docs(docs)
    print(f"Split into {len(chunks)} chunks")

    embeddings = embed_chunks(chunks)
    print(f"Generated {len(embeddings)} embeddings")

    store_vectors(chunks, embeddings)
    print("Indexing complete")
