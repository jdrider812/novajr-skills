# summarize.py – Nova Jr TL;DR skill (LLM‑powered)
import re, textwrap, urllib.request
from pathlib import Path
import llm_engine  # Nova Jr’s existing LLM wrapper

MAX_CHARS = 20_000          # limit per request
CHUNK_SIZE = 3_000          # chunk before sending to LLM
SYSTEM_PROMPT = (
    "You are Nova Jr's summarizer. "
    "Return a concise, neutral 4–6 sentence summary of the provided text."
)

def fetch_text(source: str) -> str:
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source, timeout=10) as r:
            html = r.read().decode(errors="ignore")
        # naïve tag strip
        return re.sub(r"<[^>]+>", " ", html)
    p = Path(source)
    if p.exists() and p.is_file():
        return p.read_text(errors="ignore")
    return source  # treat raw text

raw = (globals().get("input") or "").strip()
if not raw or raw.lower() == "summarize":
    result = "Usage: summarize <url | path | text>"
else:
    try:
        body = fetch_text(raw)[:MAX_CHARS]

        # split into roughly CHUNK_SIZE pieces
        chunks = [
            body[i : i + CHUNK_SIZE] for i in range(0, len(body), CHUNK_SIZE)
        ]

        partials = []
        for chunk in chunks:
            partials.append(
                llm_engine.ask(chunk.strip(), system_prompt=SYSTEM_PROMPT)
            )

        # final merge
        merged = " ".join(partials)
        result = textwrap.shorten(merged, width=1200, placeholder="…")
    except Exception as e:
        result = f"❌ Summarize error: {e}"
