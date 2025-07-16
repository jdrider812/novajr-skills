# === File: /mnt/nova-jr/skill_editor.py ===

import os
import json

SKILL_DIR = "/mnt/ssd2/nova-memory/skills"

def save_skill(name, code):
    filename = os.path.join(SKILL_DIR, f"{name}.py")
    with open(filename, "w") as f:
        f.write(code)
    return f"✅ Skill '{name}' saved."

def delete_skill(name):
    filename = os.path.join(SKILL_DIR, f"{name}.py")
    if os.path.exists(filename):
        os.remove(filename)
        return f"🗑️ Skill '{name}' deleted."
    return f"⚠️ Skill '{name}' not found."

def list_skills():
    return [f[:-3] for f in os.listdir(SKILL_DIR) if f.endswith(".py")]
