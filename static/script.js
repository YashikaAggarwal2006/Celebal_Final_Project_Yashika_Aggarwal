// script.js
// This is the "glue" between what the user does in the browser
// and the Flask backend (app.py).

const uploadBtn = document.getElementById("uploadBtn");
const notesInput = document.getElementById("notesInput");
const uploadStatus = document.getElementById("uploadStatus");

const uploadPdfBtn = document.getElementById("uploadPdfBtn");
const pdfInput = document.getElementById("pdfInput");

const askForm = document.getElementById("askForm");
const questionInput = document.getElementById("questionInput");
const chatWindow = document.getElementById("chatWindow");

let documentUploaded = false;

// ---- Step 1a: Upload / save pasted notes ----
uploadBtn.addEventListener("click", async () => {
  const text = notesInput.value.trim();

  if (!text) {
    uploadStatus.textContent = "Please paste some notes first.";
    return;
  }

  uploadStatus.textContent = "Saving your notes...";

  const response = await fetch("/upload", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: text })
  });

  const data = await response.json();
  uploadStatus.textContent = data.message;

  if (data.success) {
    documentUploaded = true;
  }
});

// ---- Step 1b: Upload a PDF file instead ----
uploadPdfBtn.addEventListener("click", async () => {
  const file = pdfInput.files[0];

  if (!file) {
    uploadStatus.textContent = "Please choose a PDF file first.";
    return;
  }

  uploadStatus.textContent = "Reading your PDF...";

  // FormData is used (instead of JSON) because we're sending a real file, not just text
  const formData = new FormData();
  formData.append("pdf", file);

  const response = await fetch("/upload-pdf", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  uploadStatus.textContent = data.message;

  if (data.success) {
    documentUploaded = true;
  }
});

// ---- Step 2: Ask a question ----
askForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = questionInput.value.trim();
  if (!question) return;

  if (!documentUploaded) {
    addChatEntry(question, "Please save some notes before asking a question.", "");
    questionInput.value = "";
    return;
  }

  const response = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question })
  });

  const data = await response.json();

  if (data.success) {
    addChatEntry(question, data.result.answer, data.result.source);
  } else {
    addChatEntry(question, data.message, "");
  }

  questionInput.value = "";
});

// ---- Helper: add a question/answer pair to the chat window ----
function addChatEntry(question, answer, source) {
  // remove the "empty state" message the first time a question is asked
  const emptyMsg = chatWindow.querySelector(".chat-empty");
  if (emptyMsg) emptyMsg.remove();

  const pair = document.createElement("div");
  pair.className = "qa-pair";

  const sourceHtml = source
    ? `<span class="source-label">from: "${source.slice(0, 90)}..."</span>`
    : "";

  pair.innerHTML = `
    <div class="question-bubble">${escapeHtml(question)}</div>
    <div class="answer-card">${escapeHtml(answer)} ${sourceHtml}</div>
  `;

  chatWindow.appendChild(pair);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// ---- Helper: avoid rendering raw HTML typed by the user ----
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
