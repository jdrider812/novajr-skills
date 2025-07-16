# qna_add.py – add a structured Q&A pair to memory
import re, json
from pathlib import Path

MEM = Path("memory/qna_memory.json")
MEM.parent.mkdir(exist_ok=True)
if not MEM.exists():
    MEM.write_text("{}")

raw = (globals().get("input") or "").strip()

# Expected: qna_add Question: Answer
payload = re.sub(r"(?i)^qna_add\s+", "", raw).strip()
m = re.match(r"(.+?)\s*[:=]\s*(.+)", payload)
if not m:
    result = "Usage: qna_add Question: Answer"
else:
    q, a = m[1].strip(), m[2].strip()
    data = json.loads(MEM.read_text())
    data[q] = a
    MEM.write_text(json.dumps(data, indent=2))
    result = f"✅ Saved Q&A:\nQ: {q}\nA: {a}"
