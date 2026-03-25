from pipeline.loader import loader
from pipeline.chunker import chunker
from pipeline.embedder import embedder
from pipeline.vector_store import store_vectors


def run_build_index(**context):
    file_path = context["dag_run"].conf["file_path"]
    print(f"Building index for: {file_path}")

    docs = loader(file_path)
    print(f"Loaded {len(docs)} document(s)")
    print(docs)

    chunks = chunker(docs)
    print(f"Split into {len(chunks)} chunks")

    embeddings = embedder(chunks)
    print(f"Generated {len(embeddings)} embeddings")

    store_vectors(chunks, embeddings)
    print("Indexing complete")
