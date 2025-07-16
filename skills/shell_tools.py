#!/usr/bin/env python3
"""
shell_tools.py
--------------
Run a limited set of safe system commands for Nova Jr.
"""

import subprocess

# Allow only these commands and their whitelisted flags
ALLOWED_COMMANDS = {
    "ls": ["-l", "-a", "-lh"],
    "df": ["-h"],
    "uptime": [],
    "whoami": [],
    "cat": [],      # allow reading files only
    "free": ["-h"],
    "nvidia-smi": [],
}

def run_safe_command(cmd: str, args: list[str] = []) -> str:
    if cmd not in ALLOWED_COMMANDS:
        return f"❌ Command not allowed: {cmd}"

    allowed_args = ALLOWED_COMMANDS[cmd]
    # Allow absolute paths for ls/cat; otherwise args must be whitelisted
    for arg in args:
        if not (arg in allowed_args or arg.startswith("/")):
            return f"❌ Invalid arg for {cmd}: {arg}"

    try:
        output = subprocess.check_output([cmd] + args, text=True, stderr=subprocess.STDOUT)
        return output.strip() or "(no output)"
    except subprocess.CalledProcessError as e:
        return f"❌ Command failed:\n{e.output}"
    except Exception as exc:
        return f"❌ Error: {exc}"
