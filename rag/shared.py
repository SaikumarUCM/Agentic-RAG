import os

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

load_dotenv()

COLLECTION_NAME = "documents"
VECTOR_DIM = 768  # intfloat/e5-base output dimension

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

# Loaded once at module import — shared across ingestor and retriever_tool
embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-base")
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
