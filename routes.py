# routes.py
#
# WHAT THIS FILE DOES:
# Defines the web addresses ("routes") the frontend can talk to.
# It does NOT contain any AI logic itself -- it just receives requests,
# passes them to agent.py, and sends back the result as JSON.

from flask import Blueprint, request, jsonify, render_template
import agent

# a Blueprint lets us define routes in a separate file from the main app
routes = Blueprint("routes", __name__)


@routes.route("/")
def home():
    """Shows the frontend page."""
    return render_template("index.html")


@routes.route("/upload", methods=["POST"])
def upload():
    """Receives the user's pasted notes and builds the searchable index."""
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"success": False, "message": "No text was provided."}), 400

    try:
        num_chunks = agent.upload_document(text)
        return jsonify({
            "success": True,
            "message": f"Document uploaded successfully! Stored as {num_chunks} chunks."
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Error processing document: {str(e)}"}), 500


@routes.route("/upload-pdf", methods=["POST"])
def upload_pdf():
    """Receives an uploaded PDF file, extracts its text, and builds the searchable index."""
    if "pdf" not in request.files:
        return jsonify({"success": False, "message": "No PDF file was uploaded."}), 400

    pdf_file = request.files["pdf"]

    if pdf_file.filename == "":
        return jsonify({"success": False, "message": "No file was selected."}), 400

    if not pdf_file.filename.lower().endswith(".pdf"):
        return jsonify({"success": False, "message": "Please upload a .pdf file."}), 400

    try:
        num_chunks = agent.upload_pdf(pdf_file)
        return jsonify({
            "success": True,
            "message": f"PDF uploaded successfully! Stored as {num_chunks} chunks."
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"Error processing PDF: {str(e)}"}), 500


@routes.route("/ask", methods=["POST"])
def ask():
    """Receives a question and returns Gemini's answer, grounded in the uploaded notes."""
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"success": False, "message": "Please type a question."}), 400

    try:
        result = agent.ask_question(question)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        # catches things like a missing/invalid GEMINI_API_KEY
        return jsonify({"success": False, "message": f"Something went wrong calling Gemini: {str(e)}"}), 500
