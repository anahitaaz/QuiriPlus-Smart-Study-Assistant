# 🪄 Quiri+ — Smart Study Assistant

**Quiri+** helps students summarize their notes and ask direct questions from them.
Upload your notes (PDF or text), generate a concise summary, and ask any question — Quiri+ finds the answer instantly.

## 🧠 Features
- Upload `.pdf` or `.txt` notes
- Summarize long documents
- Ask questions about the content
- Highlights answers within the text
- Beautiful Streamlit UI

## ⚙️ Tech Stack
- Streamlit
- HuggingFace Transformers (`facebook/bart-large-cnn`, `deepset/roberta-base-squad2`)
- PyPDF2
- Python 3.10+

## 🚀 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
