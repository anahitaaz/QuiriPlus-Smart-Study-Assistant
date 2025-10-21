import streamlit as st
from qa_model import answer_question, summarize_text
from utils import extract_text_from_pdf, highlight_answer

st.set_page_config(page_title="Quiri+ — Smart Study Assistant", page_icon="🪄", layout="wide")

# --- Custom CSS ---
st.markdown(
    """
    <style>
    :root{
      --accent1: #ff7ab6;
      --accent2: #3ee0c9;
      --bg: linear-gradient(135deg, #7b6df6 0%, #ff7ab6 40%, #3ee0c9 100%);
    }
    .main-container {
      border-radius: 18px;
      padding: 18px;
      background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(255,245,250,0.9));
      box-shadow: 0 6px 24px rgba(0,0,0,0.15);
      border: 6px solid rgba(255,255,255,0.6);
    }
    .app-header{
      background: linear-gradient(90deg, #ff7ab6, #c86dd7, #3ee0c9);
      color: white;
      padding: 18px;
      border-radius: 18px;
      text-align: center;
      font-weight: 700;
      font-size: 28px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.15);
      margin-bottom: 14px;
      border: 4px solid rgba(255,255,255,0.7);
    }
    .feature-card{
      background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,245,250,0.95));
      border-radius: 14px;
      padding: 14px;
      margin-bottom: 12px;
      border: 2px solid rgba(200,150,245,0.35);
      box-shadow: 0 6px 20px rgba(200,150,245,0.08);
    }
    .feature-icon{
      width:48px;height:48px;border-radius:12px;display:inline-block;margin-right:12px;
      vertical-align:middle;
      background: linear-gradient(135deg, #ff7ab6, #c86dd7);
      color:white;padding:8px;text-align:center;font-weight:700;
    }
    .summary-box{
      background: rgba(255,255,255,0.92);
      padding:12px;border-radius:12px;border:1px solid rgba(200,150,245,0.15);
    }
    .answer-box{
      background: linear-gradient(90deg, rgba(254,246,236,0.7), rgba(255,243,254,0.7));
      padding:12px;border-radius:12px;border:1px solid rgba(200,150,245,0.15);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="app-header">Quiri+ — Smart Study Assistant</div>', unsafe_allow_html=True)

with st.container():
    cols = st.columns([3, 1])
    main_col, side_col = cols[0], cols[1]

    with side_col:
        st.markdown('<h4 style="text-align:right;color:#8a2be2">Tools & Features</h4>', unsafe_allow_html=True)
        features = [
            ("📄", "Upload PDF", "Import your study materials"),
            ("💬", "Q&A Assistant", "Ask questions about your content"),
            ("📝", "PDF Summarizer", "Get quick summaries"),
            ("📚", "Study Notes", "Generate smart notes"),
            ("🧠", "Quiz Generator", "Test your knowledge"),
            ("🔖", "Smart Flashcards", "AI-powered memorization")
        ]
        for icon, title, desc in features:
            st.markdown(f"""
                <div class="feature-card">
                    <span class="feature-icon">{icon}</span>
                    <span style="font-weight:700;font-size:16px">{title}</span><br/>
                    <span style="color:#9b59b6">{desc}</span>
                </div>
            """, unsafe_allow_html=True)

    with main_col:
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.subheader("Upload your notes (PDF or paste text) — summarize and ask questions.")

        uploaded = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
        context_text = ""
        if uploaded:
            if uploaded.type == "application/pdf":
                context_text = extract_text_from_pdf(uploaded)
                st.success("PDF loaded successfully.")
            else:
                try:
                    context_text = uploaded.getvalue().decode("utf-8")
                    st.success("Text file loaded successfully.")
                except Exception:
                    st.error("Could not read file.")
        else:
            context_text = st.text_area("Or paste your notes here:", height=260)

        if st.button("Generate Summary"):
            if not context_text.strip():
                st.warning("Please provide some text or upload a PDF.")
            else:
                with st.spinner("Summarizing..."):
                    summary = summarize_text(context_text)
                st.markdown(f'<div class="summary-box"><strong>Summary</strong><br/>{summary}</div>', unsafe_allow_html=True)

        st.subheader("Ask a question about your notes")
        question = st.text_input("Type your question here:")
        if st.button("Find Answer"):
            if not question.strip() or not context_text.strip():
                st.warning("Please provide both context and a question.")
            else:
                with st.spinner("Searching for the best answer..."):
                    res = answer_question(context_text, question)
                st.markdown(f'<div class="answer-box"><strong>Answer:</strong> {res["answer"]} <br/><small>Confidence: {res["score"]:.2f}%</small></div>', unsafe_allow_html=True)
                st.markdown("<br/><strong>Context Highlight</strong>", unsafe_allow_html=True)
                st.markdown(highlight_answer(context_text, res["answer"]), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br/><div style='text-align:center;color:#7a3aa5'>Built with ❤️ — Quiri+ (Streamlit)</div>", unsafe_allow_html=True)
