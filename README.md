# Study Buddy — AI-Powered Study Assistant (RAG + Gemini 2.5)

A Retrieval-Augmented Generation (RAG) app. Paste your notes, ask a question,
and get a real AI-generated answer, grounded in your own material and written by Google's Gemini 2.5.

## Tech stack

- **Backend:** Python + Flask (organized into small, single-purpose modules)
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`) — real semantic vectors
- **Vector database:** FAISS — fast similarity search over those vectors
- **Generation (LLM):** Gemini 2.5 Flash (Google `google-genai` SDK)
- **Frontend:** HTML, CSS, vanilla JavaScript

## Folder structure

```
study_assistant_gemini/
├── main.py                     # Entry point — creates and runs the Flask app
├── config.py                    # All settings in one place (API key, model names, chunk size)
├── agent.py                      # Orchestrator — connects document/embedding/answer services
├── routes.py                      # Flask routes — handles web requests only, no AI logic
├── services/
│   ├── document_service.py         # Splits raw text into chunks
│   ├── embedding_service.py         # Embeds chunks + builds/searches the FAISS index
│   └── answer_service.py             # Calls Gemini to generate the final answer
├── templates/
│   └── index.html                    # Frontend page structure
├── static/
│   ├── style.css                      # Frontend styling (chalkboard theme)
│   └── script.js                       # Frontend behavior (talks to the backend)
└── requirements.txt
```

**Why split into so many files?** Each file has exactly one job, so it's easy to find and change things:
- Want to change how chunking works? → only touch `document_service.py`
- Want to swap the embedding model? → only touch `embedding_service.py` / `config.py`
- Want to swap Gemini for a different LLM? → only touch `answer_service.py`
- Want to add a new webpage/route? → only touch `routes.py`

## How the pieces connect

```
Browser (index.html + script.js)
      │  fetch() calls
      ▼
routes.py            <-- receives web requests, has NO AI logic itself
      │  calls
      ▼
agent.py              <-- decides what steps to run, in what order
      │  calls
      ▼
services/document_service.py    -> chunk_text()
services/embedding_service.py    -> build_index(), search_index()
services/answer_service.py        -> generate_answer()
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get a free Gemini API key from **https://aistudio.google.com/apikey**

3. Set up your `.env` file:
```bash
cp .env.example .env
```
Then open `.env` in any text editor and paste your real key in:
```
GEMINI_API_KEY=your-actual-key-here
```
The app loads this automatically every time it starts — no need to `export` it manually.

4. Run the app:
```bash
python main.py
```

5. Open your browser to **http://127.0.0.1:5000**

> **Note:** the first run downloads the embedding model (~90MB) from Hugging Face —
> this needs internet just for that one-time download. After that, embedding works offline;
> only the Gemini call needs internet each time you ask a question.

## Usage

1. Paste your notes into the left panel and click **Save Notes**
2. Type a question in the right panel and click **Ask**
3. Gemini generates a real answer using only your notes, plus a preview of which chunks it used

## What each file does (quick reference)

| File | Job |
|---|---|
| `main.py` | Starts the Flask web server |
| `config.py` | Stores API keys, model names, and settings (loads `.env` automatically) |
| `.env` | Your real, secret API key — never share or commit this file |
| `.env.example` | A template showing what `.env` should contain |
| `routes.py` | Defines `/`, `/upload`, `/ask` — talks to the browser |
| `agent.py` | Decides the RAG steps: chunk → embed → search → generate |
| `services/document_service.py` | Breaks text into chunks |
| `services/embedding_service.py` | Turns chunks into vectors, stores/searches them with FAISS |
| `services/answer_service.py` | Sends the question + matched notes to Gemini, returns the answer |
| `templates/index.html` | The webpage layout |
| `static/style.css` | The webpage's visual styling |
| `static/script.js` | Connects buttons/inputs to the backend routes |
