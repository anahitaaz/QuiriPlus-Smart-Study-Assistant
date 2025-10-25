import streamlit as st
from qa_model import summarize_text, answer_question
from utils import extract_text_from_pdf, highlight_answer
from persona_data import persona_prompts, persona_colors

st.set_page_config(page_title="QuiriX — The Multiverse of Mindsets", page_icon="🪩", layout="wide")

# Sidebar persona selector
persona = st.sidebar.selectbox("🪩 Choose Your Persona", list(persona_prompts.keys()))
st.sidebar.markdown(f"<div style='color:{persona_colors[persona]['accent']};font-weight:600'>Active Persona: {persona}</div>", unsafe_allow_html=True)

# Header with persona color theme
header_color = persona_colors[persona]["header"]
bg_grad = persona_colors[persona]["bg"]

st.markdown(f"""
    <style>
    .main-header {{
        background: {bg_grad};
        color: white;
        text-align: center;
        padding: 18px;
        border-radius: 18px;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 15px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"<div class='main-header'>🎭 QuiriX — {persona} Mode</div>", unsafe_allow_html=True)

# --- Main layout ---
uploaded = st.file_uploader("Upload your study notes (.pdf / .txt)", type=["pdf","txt"])
context_text = ""
if uploaded:
    if uploaded.type == "application/pdf":
        context_text = extract_text_from_pdf(uploaded)
        st.success("PDF uploaded and text extracted.")
    else:
        context_text = uploaded.getvalue().decode("utf-8")
else:
    context_text = st.text_area("Or paste your notes here:", height=260)

st.divider()

# --- Summarization section ---
st.subheader(f"{persona} Summarizes Your Notes 🪶")
if st.button("✨ Generate Persona-Based Summary"):
    if context_text.strip():
        with st.spinner("Summarizing through the multiverse..."):
            persona_prefix = persona_prompts[persona]
            styled_input = f"{persona_prefix}\n\n{context_text}"
            summary = summarize_text(styled_input)
        st.markdown(f"<div style='background:white;padding:15px;border-radius:12px;border-left:6px solid {header_color}'>{summary}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please upload or paste some text first.")

st.divider()

# --- Q&A Section ---
st.subheader(f"💬 Ask {persona} Anything")
question = st.text_input("Type your question:")
if st.button("🔮 Get Answer"):
    if question.strip() and context_text.strip():
        with st.spinner(f"{persona} is thinking..."):
            persona_prefix = persona_prompts[persona]
            styled_context = f"{persona_prefix}\n\n{context_text}"
            result = answer_question(styled_context, question)
        answer, score = result["answer"], result["score"]
        st.markdown(f"<div style='background:white;padding:12px;border-radius:12px;border-left:6px solid {header_color}'>"
                    f"<b>Answer:</b> {answer}<br><small>Confidence: {score:.1f}%</small></div>", unsafe_allow_html=True)
        st.markdown("<br><b>Context Highlight:</b>", unsafe_allow_html=True)
        st.markdown(highlight_answer(context_text, answer), unsafe_allow_html=True)
    else:
        st.warning("Please provide both your notes and a question.")

st.markdown(f"<br><center><i>Built with ❤️ by Anahita Malviya — Powered by QuiriX Multiverse Engine</i></center>", unsafe_allow_html=True)
