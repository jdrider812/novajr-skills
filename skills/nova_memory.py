# nova_memory.py – memory functions and Q&A auto-suggestion
import json, re
from pathlib import Path

MEMORY_FILE = Path("memory/memory.json")
QNA_FILE = Path("memory/qna.json")

def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return []

def save_memory(data):
    MEMORY_FILE.write_text(json.dumps(data, indent=2))

def remember_item(text):
    mem = load_memory()
    if text not in mem:
        mem.append(text)
        save_memory(mem)
    return f"Got it! I’ll remember: {text}"

def recall_from_memory(prompt):
    mem = load_memory()
    for item in mem:
        if item.lower() in prompt.lower():
            return item
    return None

def try_auto_qna(question, answer):
    if not question or not answer: return None
    # Simple heuristics: ends in ? and isn't too long
    if len(question) > 80 or not question.endswith("?"): return None
    add_qna(question, answer)
    return f"✅ Auto Q&A saved:\nQ: {question}\nA: {answer}"

def load_qna():
    if QNA_FILE.exists():
        return json.loads(QNA_FILE.read_text())
    return {}

def save_qna(data):
    QNA_FILE.write_text(json.dumps(data, indent=2))

def add_qna(question, answer):
    qna = load_qna()
    qna[question] = answer
    save_qna(qna)

def query_qna(prompt):
    qna = load_qna()
    for q, a in qna.items():
        if q.lower() in prompt.lower():
            return a
    return None
