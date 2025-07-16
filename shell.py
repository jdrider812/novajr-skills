# shell.py – Safe, read‑only shell skill for Nova Jr
import shlex, subprocess, re

# Get input text
raw = (
    globals().get("input")
    or globals().get("user_input")
    or ""
).strip()

if not raw or raw.lower() == "shell":
    result = "Please specify a command, e.g. 'shell ls -l'"
else:
    # Clean leading 'shell' and trailing chatter like 'and remember that'
    cleaned = re.sub(r"(?i)^shell\s+", "", raw)
    cleaned = re.split(r"\s+and\s+", cleaned)[0].strip()

    SAFE_CMDS = [
        "ls", "cat", "pwd", "whoami",
        "nvidia-smi", "df", "free", "uname"
    ]

    try:
        parts = shlex.split(cleaned)
        if not parts:
            result = "Please specify a command, e.g. 'shell ls -l'"
        elif parts[0] not in SAFE_CMDS:
            result = f"❌ Command '{parts[0]}' not allowed."
        else:
            output = subprocess.check_output(
                parts, stderr=subprocess.STDOUT, text=True, timeout=5
            )
            result = f"$ {' '.join(parts)}\n{output}"
    except Exception as exc:
        result = f"❌ {exc}"
