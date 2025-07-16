#!/usr/bin/env python3
"""
fact_extractor.py
Optional: detects & stores facts from assistant replies
"""

import re
from uuid import uuid4
from datetime import datetime, timedelta
from memory_manager import save_memory, load_memory


def maybe_extract_fact(user_msg: str, assistant_reply: str):
    """
    Looks for simple factual statements about Jon in the assistant reply.
    If a fact is found and not already stored, save it.
    """

    text = assistant_reply.strip()

    # Example match: "You were born in Arizona"
    match = re.match(r"You were born in ([A-Za-z\s]+)", text, re.I)
    if match:
        fact = f"Jon was born in {match.group(1).strip()}"
    else:
        return None  # no extractable fact

    # Check if already known
    memory = load_memory()
    for f in memory.get("facts", []):
        if f.get("text", "") == fact:
            return None  # already known

    # Save as new fact
    new_fact = {
        "id": str(uuid4()),
        "text": fact,
        "created": datetime.now().timestamp(),
        "hits": 0,
        "expires_at": (datetime.now() + timedelta(days=90)).timestamp(),
        "pinned": False,
    }

    memory["facts"].append(new_fact)
    save_memory(memory)

    return new_fact
