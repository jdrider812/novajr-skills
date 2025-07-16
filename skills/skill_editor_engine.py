from pathlib import Path

SKILL_DIR = Path("skills")
SKILL_DIR.mkdir(exist_ok=True)

def save_skill(name: str, code: str):
    """Save skill source under skills/<name>.py"""
    (SKILL_DIR / f"{name}.py").write_text(code.strip())

def load_skill(name: str) -> str | None:
    path = SKILL_DIR / f"{name}.py"
    return path.read_text() if path.exists() else None

def load_all_skills() -> dict[str, str]:
    """Return {skill_name: code} for every saved skill"""
    return {f.stem: f.read_text() for f in SKILL_DIR.glob("*.py")}
