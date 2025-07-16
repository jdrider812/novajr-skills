#!/usr/bin/env python3
"""
chat_terminal.py – CLI interface to talk with Nova Jr, with JSONL log
"""

import readline
import json, uuid, time, os
from datetime import datetime
from chat_engine import ask_nova

chat_history = []
print("🤠 Nova Jr terminal chat.  Type 'exit' to quit.\n")

# 🗃️ Save log to unique file
log_path = "/mnt/ssd2/nova-memory/chat_logs"
ts = datetime.now().strftime("%Y%m%d-%H%M%S")
uid = uuid.uuid4().hex[:32]
filename = f"termchat_{ts}_{uid}.jsonl"
full_path = os.path.join(log_path, filename)

def log(role, text):
    with open(full_path, "a") as f:
        f.write(json.dumps({"ts": time.time(), "role": role, "text": text}) + "\n")

while True:
    try:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("👋 Shutting down Nova Jr.")
            break

        log("user", user_input)
        chat_history, updated = ask_nova(user_input, chat_history)
        reply = updated[-1]["content"]
        print(f"Nova Jr: {reply}")
        log("assistant", reply)

    except KeyboardInterrupt:
        print("\n👋 Shutting down Nova Jr.")
        break
    except Exception as e:
        print(f"⚠️ Error: {e}")
