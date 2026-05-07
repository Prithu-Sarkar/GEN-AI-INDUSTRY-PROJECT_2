import os
from groq import Groq
from typing import List, Dict

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Token budgets (Groq rate limits: 6000 TPM instant, 32768 context)
INSTANT_MODEL   = "llama-3.1-8b-instant"   # fast, cheap — interviewer / transformer
VERSATILE_MODEL = "llama-3.3-70b-versatile" # smarter — evaluator
MAX_TOKENS_FAST = 300
MAX_TOKENS_EVAL = 500


def chat(model: str, messages: List[Dict], max_tokens: int = MAX_TOKENS_FAST) -> str:
    """Single call wrapper with token guard."""
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()


def interviewer_ask(job: str, history: List[Dict], q_num: int) -> str:
    system = (
        f"You are a professional interviewer for a {job} position. "
        f"Ask question {q_num} of 3 (technical/problem-solving/culture fit). "
        "Keep it under 50 words. If all 3 done, reply exactly: TERMINATE"
    )
    msgs = [{"role": "system", "content": system}] + history
    return chat(INSTANT_MODEL, msgs, MAX_TOKENS_FAST)


def evaluator_feedback(job: str, question: str, answer: str) -> str:
    system = (
        f"You are a career coach for {job} interviews. "
        "Give constructive feedback on the candidate answer in max 60 words."
    )
    msgs = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"""Question: {question}
Answer: {answer}"""},
    ]
    return chat(VERSATILE_MODEL, msgs, MAX_TOKENS_EVAL)


def final_evaluator(job: str, transcript: List[Dict]) -> str:
    system = (
        f"You are a senior hiring manager for a {job} role. "
        "Summarise the candidate performance across all answers. "
        "Give: score /10, strengths, weaknesses, hire recommendation. Max 150 words."
    )
    summary_text = "\n".join(
        [f"Q{i+1}: {t['question']}\nA: {t['answer']}" for i, t in enumerate(transcript)]
    )
    msgs = [
        {"role": "system", "content": system},
        {"role": "user", "content": summary_text},
    ]
    return chat(VERSATILE_MODEL, msgs, MAX_TOKENS_EVAL)