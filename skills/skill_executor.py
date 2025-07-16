# skill_executor.py – dynamic loader (no upfront imports)
from pathlib import Path
import os, types

SKILLS_DIR = Path("skills")

def try_skill(message: str):
    """
    Detects if the message starts with a known skill name
    and runs that skill with 'input' set in its globals.
    """
    if not message:
        return None

    first_word = message.split()[0]
    skill_path = SKILLS_DIR / f"{first_word}.py"
    if not skill_path.exists():
        return None  # no matching skill file

    code = skill_path.read_text()
    g = {
        "__file__": str(skill_path),
        "__name__": f"skill_{first_word}",
        "input": message
    }
    try:
        exec(compile(code, str(skill_path), "exec"), g)
    except Exception as e:
        return f"[Skill error: {e}]"
    return g.get("result", "[No result]")
