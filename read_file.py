# read_file.py – Nova Jr safe file viewer
import os
from pathlib import Path

BASE = Path("/mnt/nova-jr").resolve()
MAX_BYTES = 50_000

# Get user message
msg = (globals().get("input") or "").strip()

# Extract target path
target = msg
if target.lower().startswith("read_file"):
    target = target.split(None, 1)[1] if " " in target else ""

# Check for missing argument
if not target:
    result = "Please say something like: read_file memory/memory.json"
else:
    # Build safe path
    try:
        full = (BASE / target).resolve()
        if not full.exists():
            result = f"❌ File not found: {target}"
        elif not str(full).startswith(str(BASE)):
            result = f"❌ Access denied: {target} is outside /mnt/nova-jr"
        elif full.stat().st_size > MAX_BYTES:
            result = f"❌ File too large (>50KB): {target}"
        else:
            text = full.read_text(errors="replace")
            result = f"$ cat {target}\n" + text.strip()
    except Exception as e:
        result = f"❌ Error reading file: {e}"
