# services/answer_service.py
#
# WHAT THIS FILE DOES:
# This is the "Generation" part of RAG (Retrieval-Augmented Generation).
# It takes the chunks of text that embedding_service.py found, hands them
# to Google's Gemini model as context, and asks Gemini to write a real,
# human-readable answer using only that context.

from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME

# Create the Gemini client once, using the API key from config.py
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(question, matched_chunks):
    """
    Sends the question + matched notes to Gemini and returns its written answer.
    """
    context = "\n\n".join(matched_chunks)

    prompt = f"""You are a helpful study assistant. Answer the student's question using ONLY the notes below.
If the notes don't contain the answer, say so honestly instead of guessing.

Notes:
{context}

Question: {question}

Answer clearly and simply, in 2-4 sentences."""

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=prompt
    )

    return response.text
