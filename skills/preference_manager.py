import json
import os

PREFS_FILE = "/mnt/ssd2/nova-memory/memory.json"

def handle_preference_update(prompt):
    if "reply style" in prompt.lower():
        if "step-by-step" in prompt.lower():
            return update_reply_style("step-by-step")
        elif "minimal" in prompt.lower():
            return update_reply_style("minimal")
    return None

def update_reply_style(style):
    if not os.path.exists(PREFS_FILE):
        return "⚠️ Preferences file not found."

    with open(PREFS_FILE, "r") as f:
        memory = json.load(f)

    memory["preferences"] = memory.get("preferences", {})
    memory["preferences"]["reply_style"] = style

    with open(PREFS_FILE, "w") as f:
        json.dump(memory, f, indent=4)

    return f"✅ Preference updated: reply_style = '{style}'"
