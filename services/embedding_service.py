# services/embedding_service.py
#
# WHAT THIS FILE DOES:
# This is the "Retrieval" part of RAG (Retrieval-Augmented Generation).
# It turns text chunks into number vectors ("embeddings") using an AI model,
# stores them in a FAISS vector database, and can search that database to
# find which chunks are most relevant to a question.

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL_NAME, EMBEDDING_DIMENSIONS, TOP_K_CHUNKS, MIN_SIMILARITY_SCORE

# Loads the embedding model once, when this file is first imported
# (loading it inside every function call would be slow and wasteful)
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# These hold our "database" in memory. They get filled in by build_index().
all_chunks = []
faiss_index = None


def build_index(chunks):
    """
    Converts every chunk of text into a vector, then stores all those
    vectors in a FAISS index so we can search them later.
    """
    global all_chunks, faiss_index

    all_chunks = chunks

    # turn each text chunk into a list of numbers (a vector)
    vectors = embedding_model.encode(chunks)
    vectors = np.array(vectors).astype("float32")

    # normalizing lets us use "inner product" search to mean "cosine similarity"
    faiss.normalize_L2(vectors)

    # IndexFlatIP = a simple FAISS index that compares vectors by inner product
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
