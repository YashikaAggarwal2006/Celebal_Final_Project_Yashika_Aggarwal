
from config import CHUNK_SIZE
from pypdf import PdfReader


def extract_text_from_pdf(pdf_file):
    """
    Reads a PDF file (sent from the browser) and pulls out all its text.
    pdf_file is a file-like object -- pypdf can read directly from it,
    no need to save it to disk first.
    """
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def chunk_text(text):
    """
    Splits a big block of text into a list of smaller chunks.
    Example: 120 words with CHUNK_SIZE=40 -> 3 chunks of ~40 words each.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), CHUNK_SIZE):
        chunk = " ".join(words[i:i + CHUNK_SIZE])
        chunks.append(chunk)

    return chunks
