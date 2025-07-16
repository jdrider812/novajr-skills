# json_tool.py – Nova Jr JSON parser + pretty-printer
import json, urllib.request, os, re
from pathlib import Path

def try_load_json(text):
    try:
        return json.loads(text)
    except Exception:
        return None

raw = (globals().get("input") or "").strip()
if not raw or raw.lower() == "json_tool":
    result = "Please say something like: json_tool memory/memory.json"
else:
    raw = re.sub(r"(?i)^json_tool\s+", "", raw).strip()
    data = None

    try:
        if raw.startswith("http://") or raw.startswith("https://"):
            with urllib.request.urlopen(raw, timeout=5) as resp:
                data = try_load_json(resp.read().decode())
        else:
            path = Path(raw)
            if path.exists() and path.is_file():
                data = try_load_json(path.read_text())
            else:
                result = f"❌ File not found: {raw}"

        if data is not None:
            result = json.dumps(data, indent=2)
        elif not result:
            result = "❌ Failed to parse valid JSON."
    except Exception as e:
        result = f"❌ JSON tool error: {e}"
