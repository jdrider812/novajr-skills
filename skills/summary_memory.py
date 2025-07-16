#!/usr/bin/env python3
"""
summary_memory.py
-----------------
Summarize a conversation chunk into a key-value memory line.
"""

from nova_chat_engine import generate_reply
from nova_memory import remember


def summarize_and_store(session_text: str):
    """Generate a one‑liner summary and store it in memory."""
    prompt = (
        "Summarize the following dialog in ONE short factual sentence, "
        "suitable to store as a memory about the user:\n\n"
        f"{session_text}\n\n"
        "Return the sentence only."
    )
    summary = generate_reply(prompt)
    key = f"summary_{hash(summary) & 0xffff}"  # simple unique key
    remember(key, summary)
    return key, summary
