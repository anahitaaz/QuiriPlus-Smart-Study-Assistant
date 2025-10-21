import PyPDF2
import streamlit as st
import re
from html import escape

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = [page.extract_text() for page in reader.pages if page.extract_text()]
        return "\n\n".join(text)
    except Exception as e:
        st.error("PDF parsing failed: " + str(e))
        return ""

def highlight_answer(context, answer):
    if not answer:
        return escape(context).replace("\n", "<br/>")
    ctx = escape(context)
    try:
        pattern = re.compile(re.escape(answer), re.IGNORECASE)
        highlighted = pattern.sub(
            f"<mark style='background:linear-gradient(90deg,#fff59d,#ffd2ea); padding:2px;border-radius:4px'>{escape(answer)}</mark>",
            ctx,
            count=1
        )
        return highlighted.replace("\n", "<br/>")
    except Exception:
        return ctx.replace("\n", "<br/>")
