# qna_ask.py – retrieve an answer from structured Q&A memory
import json
from pathlib import Path

MEM = Path("memory/qna_memory.json")
if not MEM.exists():
    result = "No Q&A memory yet."
else:
    question = (globals().get("input") or "").strip()
    question = question.split(None, 1)[1] if question.lower().startswith("qna_ask") else question
    data = json.loads(MEM.read_text())
    answer = None
    for q, a in data.items():
        if question.lower().strip() == q.lower().strip():
            answer = a
            break
    result = f"A: {answer}" if answer else "I don't have an answer for that yet."
