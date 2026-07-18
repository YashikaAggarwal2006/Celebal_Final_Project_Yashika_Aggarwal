
import os
from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


GEMINI_MODEL_NAME = "gemini-3.5-flash"


EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384


CHUNK_SIZE = 40


TOP_K_CHUNKS = 3
MIN_SIMILARITY_SCORE = 0.2
