import os
import json

MEMORY_FILE = "/mnt/ssd2/nova-memory/memory.json"

def handle_personality_update(prompt):
    if "personality" in prompt.lower():
        if "cowboy" in prompt.lower():
            return update_personality("cowboy")
        elif "hacker" in prompt.lower():
            return update_personality("hacker")
        elif "butler" in prompt.lower():
            return update_personality("butler")
    return None

def update_personality(personality):
    if not os.path.exists(MEMORY_FILE):
        return "⚠️ Preferences file not found."

    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)

    memory["preferences"] = memory.get("preferences", {})
    memory["preferences"]["personality"] = personality

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

    return f"🎭 Personality updated to '{personality}'"
