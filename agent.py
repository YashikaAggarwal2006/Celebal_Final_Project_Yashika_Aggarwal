# agent.py
#
# WHAT THIS FILE DOES:
# This is the main "agent" that ties all three services together:
#   1. document_service   -> splits text into chunks
#   2. embedding_service   -> stores/searches chunks using AI embeddings + FAISS
#   3. answer_service       -> asks Gemini to write the final answer
#
# routes.py calls the two functions below; it never talks to the services directly.
# This keeps the "thinking" logic separate from the "web server" logic.

from services.document_service import chunk_text, extract_text_from_pdf
from services.embedding_service import build_index, search_index, has_document_loaded
from services.answer_service import generate_answer


def upload_document(text):
    """
    Called when the user saves pasted notes.
    Chunks the text, then builds the searchable AI index from those chunks.
    Returns how many chunks were created.
    """
    chunks = chunk_text(text)
    num_chunks = build_index(chunks)
    return num_chunks


def upload_pdf(pdf_file):
    """
    Called when the user uploads a PDF instead of pasting text.
    Extracts the text from the PDF first, then reuses the same chunking + indexing steps.
    """
    text = extract_text_from_pdf(pdf_file)

    if not text.strip():
        raise ValueError("Could not extract any text from this PDF. It may be a scanned image without selectable text.")

    return upload_document(text)


def ask_question(question):
    """
    Called when the user asks a question.
    Retrieves the most relevant chunks, then asks Gemini to generate an answer.
    Returns a dictionary describing what happened, so the frontend can react to it.
    """
    if not has_document_loaded():
        return {
            "type": "error",
            "answer": "Please upload a document first.",
            "source": ""
        }

    matched_chunks = search_index(question)

    if not matched_chunks:
        return {
            "type": "not_found",
            "answer": "Sorry, I could not find anything related to that in the document.",
            "source": ""
        }

    answer_text = generate_answer(question, matched_chunks)
    source_preview = " | ".join(chunk[:100] + "..." for chunk in matched_chunks)

    return {
        "type": "answer",
        "answer": answer_text,
        "source": source_preview
    }
