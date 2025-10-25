import PyPDF2, re, streamlit as st
from html import escape

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        st.error("Error reading PDF: " + str(e))
        return ""

def highlight_answer(context, answer):
    if not answer:
        return escape(context).replace("\n", "<br/>")
    ctx = escape(context)
    try:
        pattern = re.compile(re.escape(answer), re.IGNORECASE)
        highlighted = pattern.sub(
            f"<mark style='background:linear-gradient(90deg,#fff59d,#ffd2ea);padding:2px;border-radius:4px'>{escape(answer)}</mark>",
            ctx, count=1)
        return highlighted.replace("\n","<br/>")
    except Exception:
        return ctx.replace("\n","<br/>")
