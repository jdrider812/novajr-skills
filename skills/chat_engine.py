# chat_engine.py – chat logic for Nova Jr (auto‑Q&A, fixed)
import re
from pathlib import Path
import llm_engine, nova_memory, skill_executor

LAST_RESPONSE_FILE = Path("memory/last_response.txt")

def chat_response(message: str) -> str:
    message = message.strip()

    # ---------- skills ----------
    skill_out = skill_executor.try_skill(message)
    if skill_out:
        _store_last(message)
        return skill_out

    # ---------- remember: ----------
    if message.lower().startswith("remember:"):
        fact = message.split(":", 1)[1].strip()
        res  = nova_memory.remember_item(fact)

        # auto‑Q&A if the last stored line was a question
        last_q = _load_last_question()
        if last_q and last_q.endswith("?"):
            auto = nova_memory.try_auto_qna(last_q, fact)
            if auto:
                res += f"\n🤖 {auto}"
        return res

    # ---------- manual Q&A ----------
    if message.lower().startswith("qna_add "):
        try:
            q, a = message[8:].split("?:")
            nova_memory.add_qna(q.strip()+"?", a.strip())
            return f"✅ Saved Q&A:\nQ: {q.strip()}?\nA: {a.strip()}"
        except:
            return "Format: qna_add Question?: Answer"
    if message.lower().startswith("qna_ask "):
        q = message[8:].strip()
        ans = nova_memory.query_qna(q)
        return ans or "🤔 I don’t know that yet."

    # ---------- auto Q&A recall ----------
    ans = nova_memory.query_qna(message)
    if ans:
        return ans

    # ---------- free‑text fact recall ----------
    fact = nova_memory.recall_from_memory(message)
    if fact:
        return f"I remember you told me: {fact}"

    # ---------- LLM fallback ----------
    reply = llm_engine.ask(message)

    # store last question if needed
    if message.endswith("?"):
        _save_last_question(message)

    _store_last(message)
    return f"{reply}\n🤔 Should I remember this as a Q&A? (Reply: remember: <answer>)"

# -------- helpers --------
def _store_last(msg: str):
    if not msg.lower().startswith("remember:"):
        LAST_RESPONSE_FILE.write_text(msg)

def _save_last_question(q: str):
    Path("memory/last_question.txt").write_text(q)

def _load_last_question():
    qp = Path("memory/last_question.txt")
    return qp.read_text() if qp.exists() else ""
