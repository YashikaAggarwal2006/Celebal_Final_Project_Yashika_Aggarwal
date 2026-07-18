

from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME


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
