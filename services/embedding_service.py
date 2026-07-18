
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME, EMBEDDING_DIMENSIONS, TOP_K_CHUNKS, MIN_SIMILARITY_SCORE


embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


all_chunks = []
faiss_index = None


def build_index(chunks):
    """
    Converts every chunk of text into a vector, then stores all those
    vectors in a FAISS index so we can search them later.
    """
    global all_chunks, faiss_index

    all_chunks = chunks

 
    vectors = embedding_model.encode(chunks)
    vectors = np.array(vectors).astype("float32")


    faiss.normalize_L2(vectors)

  
    faiss_index = faiss.IndexFlatIP(EMBEDDING_DIMENSIONS)
    faiss_index.add(vectors)

    return len(chunks)


def search_index(question):
    """
    Turns the question into a vector the same way, then asks FAISS
    which stored chunks are the closest match.
    Returns a list of matching text chunks (empty list if nothing matches well).
    """
    if faiss_index is None:
        return []

    query_vector = embedding_model.encode([question]).astype("float32")
    faiss.normalize_L2(query_vector)

    scores, indices = faiss_index.search(query_vector, TOP_K_CHUNKS)

    matched_chunks = []
    for score, idx in zip(scores[0], indices[0]):
        if idx != -1 and score >= MIN_SIMILARITY_SCORE:
            matched_chunks.append(all_chunks[idx])

    return matched_chunks


def has_document_loaded():
    """Simple check used by the agent to know if a document was uploaded yet."""
    return faiss_index is not None
