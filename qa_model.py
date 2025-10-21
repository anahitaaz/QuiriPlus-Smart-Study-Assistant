from transformers import pipeline

_qa_pipeline = None
_summarizer = None

def _get_qa():
    global _qa_pipeline
    if _qa_pipeline is None:
        _qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
    return _qa_pipeline

def _get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return _summarizer

def answer_question(context, question):
    qa = _get_qa()
    try:
        out = qa(question=question, context=context)
        return {"answer": out["answer"], "score": round(out["score"] * 100, 2)}
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "score": 0.0}

def summarize_text(text, max_length=120):
    summ = _get_summarizer()
    try:
        words = len(text.split())
        dyn_max = min(max_length, max(30, int(words * 0.35)))
        out = summ(text, max_length=dyn_max, min_length=20, do_sample=False)
        return out[0]["summary_text"]
    except Exception as e:
        return f"Summary not available: {str(e)}"
