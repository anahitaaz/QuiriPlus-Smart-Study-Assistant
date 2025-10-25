from transformers import pipeline

_summarizer = None
_qa_pipeline = None

def _get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return _summarizer

def _get_qa():
    global _qa_pipeline
    if _qa_pipeline is None:
        _qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
    return _qa_pipeline

def summarize_text(text):
    summ = _get_summarizer()
    try:
        words = len(text.split())
        max_len = min(130, max(50, int(words * 0.35)))
        out = summ(text, max_length=max_len, min_length=30, do_sample=False)
        return out[0]["summary_text"]
    except Exception as e:
        return "Summary error: " + str(e)

def answer_question(context, question):
    qa = _get_qa()
    try:
        res = qa(question=question, context=context)
        return {"answer": res["answer"], "score": res["score"] * 100}
    except Exception as e:
        return {"answer": "No valid answer found. " + str(e), "score": 0}
