# write_file.py – Safe file writer for Nova Jr
import os, re, textwrap, json
from pathlib import Path

BASE = Path("/mnt/nova-jr").resolve()
MAX_BYTES = 50_000

raw = (globals().get("input") or "").strip()

# Expected: write_file <relative_path>\n<content...>
parts = raw.split(None, 2)  # split into cmd, path, rest
if len(parts) < 3 or parts[0].lower() != "write_file":
    result = textwrap.dedent("""
        Usage:
        write_file path/to/file.txt
        <paste your new file content here>
    """).strip()
else:
    rel_path, content = parts[1], parts[2]
    try:
        target = (BASE / rel_path).resolve()
        if not str(target).startswith(str(BASE)):
            result = f"❌ Access denied: {rel_path} is outside /mnt/nova-jr"
        elif len(content.encode()) > MAX_BYTES:
            result = "❌ Content too large (>50KB)"
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
            result = f"✅ Wrote {len(content.encode())} bytes to {rel_path}"
    except Exception as e:
        result = f"❌ Error writing file: {e}"
