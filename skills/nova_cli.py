#!/usr/bin/env python3
"""
nova_cli.py – Nova Jr command‑line interface
"""
import argparse, sys
from pathlib import Path
import chat_engine
import llm_engine

SKILLS_DIR = Path("skills")
SKILLS_DIR.mkdir(exist_ok=True)

# ---------- helpers ----------
def save_skill(name, code):
    (SKILLS_DIR / f"{name}.py").write_text(code)
    print(f"✅ Skill '{name}' saved.")

def load_skill(name):
    p = SKILLS_DIR / f"{name}.py"
    return p.read_text() if p.exists() else None

# ---------- CLI ----------
parser = argparse.ArgumentParser()
parser.add_argument("args", nargs="+", help='use: chat "message"')
parsed = parser.parse_args()

# Expect first token to be the literal word "chat"
if parsed.args[0].lower() != "chat":
    print("Usage: nova_cli.py chat \"<message>\"")
    sys.exit(1)

user_input = " ".join(parsed.args[1:]).strip()
low = user_input.lower()

# ── 1. Skill learning ───────────────────────────────────────────
if low.startswith("learn skill:"):
    name = user_input.split(":", 1)[1].strip()
    print(f'Paste Python code for "{name}", then Ctrl‑D (Ctrl‑Z on Windows)…')
    save_skill(name, sys.stdin.read())
    sys.exit()

# ── 2. Manual multi‑skill chain  (run: A, B, C …) ──────────────
if low.startswith("run:"):
    skill_names = [s.strip() for s in user_input.split(":", 1)[1].split(",")]
    chain_input = ""
    log = []

    for skill_name in skill_names:
        code = load_skill(skill_name)
        if not code:
            log.append(f"❌ Skill '{skill_name}' not found.")
            continue

        result = chat_engine.run_skill(code, {"input": chain_input})
        log.append(f"✅ {skill_name}: {result}")
        chain_input = result  # feed next skill

    print("\n".join(log))
    sys.exit()

# ── 3. Normal chat flow ────────────────────────────────────────
reply = chat_engine.chat_response(user_input)

if reply is None:                       # no skill / memory hit
    reply = llm_engine.ask(user_input)  # fall back to LLM

print("🤖 Nova Jr:", reply)
