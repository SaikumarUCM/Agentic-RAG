from sentence_transformers import SentenceTransformer

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("intfloat/e5-base")
    return _model


def embedder(chunks) -> list:
    model = _get_model()
    texts = [c.page_content for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings.tolist()
