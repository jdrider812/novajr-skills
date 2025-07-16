#!/usr/bin/env python3
"""
shell_explainer.py
------------------
Explains common shell commands in plain English.
"""

def explain_command(command_str: str) -> str:
    command_str = command_str.strip()
    if not command_str:
        return "⚠️ You didn't enter a command."

    # Manual explanations for safety and clarity
    explanations = {
        "ls": "Lists files and directories.",
        "ls -l": "Lists files in long format showing permissions, ownership, size, and timestamp.",
        "ls -a": "Lists all files, including hidden ones.",
        "ls -lh": "Lists files using human‑readable sizes.",
        "df -h": "Shows disk space usage in human‑readable form.",
        "uptime": "Shows how long the system has been running.",
        "whoami": "Displays the current logged‑in user.",
        "cat /etc/os-release": "Displays Linux distribution information.",
        "cat /etc/passwd": "Shows user account details.",
        "free -h": "Displays memory usage in human‑readable format.",
        "nvidia-smi": "Shows GPU usage and stats (NVIDIA only).",
    }

    return explanations.get(
        command_str,
        f"🤷 Sorry, I don’t have an explanation for `{command_str}` yet."
    )
