"""
skill_admin.py – utilities for listing, deleting, and searching learned skills
"""

from pathlib import Path
SKILL_DIR = Path("skills"); SKILL_DIR.mkdir(exist_ok=True)

def list_skills() -> list[str]:
    return sorted(f.stem for f in SKILL_DIR.glob("*.py"))

def delete_skill(name: str) -> bool:
    for f in SKILL_DIR.glob("*.py"):
        if f.stem.lower() == name.lower():
            f.unlink(); return True
    return False

def search_skills(keyword: str) -> list[str]:
    kw = keyword.lower(); hits = []
    for f in SKILL_DIR.glob("*.py"):
        if kw in f.read_text().lower():
            hits.append(f.stem)
    return hits

