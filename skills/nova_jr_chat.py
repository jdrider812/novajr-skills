import json
import subprocess
import os
from datetime import datetime

MODEL_PATH = "/mnt/nova-jr/llama.cpp/build/models/mistral.gguf"
LLAMA_CLI = "/mnt/nova-jr/llama.cpp/build/bin/llama-cli"
MEMORY_FILE = "/mnt/nova-jr/memory.json"

# Load memory
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = []

print("Nova Jr: Hello, I'm ready to chat. Type 'exit' to stop.")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Nova Jr: Goodbye.")
        break

    # Strong identity and formatting
    prompt = (
        "The following is a conversation between Jon and Nova Jr.\n"
        "Nova Jr is an intelligent AI assistant created by Jon.\n"
        "Jon is Nova Jr's creator and project partner.\n"
        "Nova Jr is helpful, respectful, conversational, and always learning.\n"
        "Nova Jr always knows that Jon is the user speaking below.\n\n"
    )

    for m in memory[-2:]:
        prompt += f"Jon: {m['user']}\nNova Jr: {m['nova']}\n"
    prompt += f"Jon: {user_input}\nNova Jr:"

    result = subprocess.run(
        [LLAMA_CLI, "-m", MODEL_PATH, "-p", prompt, "-n", "150"],
        capture_output=True, text=True
    )

    raw = result.stdout.strip()

    if "Nova Jr:" in raw:
        reply = raw.split("Nova Jr:")[-1].split("[end of text]")[0].strip()
    else:
        reply = "(no response)"

    print("Nova Jr:", reply)

    memory.append({
        "time": datetime.now().isoformat(),
        "user": user_input,
        "nova": reply
    })

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
