# config.py
#
# WHAT THIS FILE DOES:
# Holds all the settings for the whole project in one place, so if you
# need to change a model name or chunk size later, you only edit it here.

import os
from dotenv import load_dotenv

# reads the .env file (if it exists) and loads its values as environment variables
load_dotenv()

# ---- Gemini API settings ----
# Your API key must be set as an environment variable before running the app.
# Get a free key at: https://aistudio.google.com/apikey
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Which Gemini model to use for generating answers
# Note: Google frequently updates which models are available to new API keys/projects.
# gemini-3.5-flash is the current stable, fast, cost-efficient model as of mid-2026.
# If you get a 404 "model not found" error, check https://ai.google.dev/gemini-api/docs/models
# for the latest available model name and update this one line.
GEMINI_MODEL_NAME = "gemini-3.5-flash"

# ---- Embedding settings ----
# Small, fast model that turns text into 384-number vectors ("embeddings")
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384

# ---- Chunking settings ----
# How many words go into each chunk of the document
CHUNK_SIZE = 40

# ---- Retrieval settings ----
# How many chunks to retrieve per question, and the minimum similarity score to count as a "match"
TOP_K_CHUNKS = 3
MIN_SIMILARITY_SCORE = 0.2
