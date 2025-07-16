# profile_summary.py – compile what Nova Jr knows about you
import json, textwrap
from pathlib import Path

FACT_FILE = Path("memory/memory.json")
QNA_FILE  = Path("memory/qna.json")

def load_json(path):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return {}
    return {}

facts = load_json(FACT_FILE) or []
qna   = load_json(QNA_FILE)  or {}

# ----- build summary text -----
lines = []

if qna:
    lines.append("🔖 **Structured Q&A**")
    for q, a in qna.items():
        lines.append(f"- **{q}** {a}")

if facts:
    lines.append("\n📝 **Free‑text facts**")
    for item in facts:
        lines.append(f"- {item}")

if not (facts or qna):
    result = "I don’t have any remembered information yet."
else:
    result = "\n".join(lines)
