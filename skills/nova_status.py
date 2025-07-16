#!/usr/bin/env python3
"""
nova_status.py
==============

Prints Nova Jr system snapshot:
• Config settings
• Uptime
• Python version
• GPU list via nvidia‑smi
"""

import json
import platform
import subprocess
from datetime import timedelta
from pathlib import Path
import time

CONFIG_PATH = Path("/mnt/nova-jr/config.json")


def read_config():
    if CONFIG_PATH.exists():
        try:
            with CONFIG_PATH.open(encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to parse config.json: {e}"}
    return {"error": "config.json not found"}


def uptime():
    try:
        seconds = float(Path("/proc/uptime").read_text().split()[0])
        return str(timedelta(seconds=int(seconds)))
    except Exception:
        return "unknown"


def gpu_info():
    try:
        out = subprocess.check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total",
                "--format=csv,noheader,nounits",
            ],
            encoding="utf-8",
        )
        return [f"GPU {i}: {line}" for i, line in enumerate(out.strip().splitlines())]
    except Exception:
        return ["No NVIDIA GPUs detected or nvidia-smi failed"]


def show_status():
    cfg = read_config()
    print("\n🌐 Nova Jr System Status\n" + "=" * 30)

    if "error" in cfg:
        print(f"⚠️ Config: {cfg['error']}")
    else:
        print(f"Model Path  : {cfg.get('model_path', 'not set')}")
        print(f"Max Memory  : {cfg.get('max_memory', 'not set')}")
        print(f"Reply Style : {cfg.get('reply_style', 'not set')}")
        print(f"Personality : {cfg.get('personality', 'not set')}")

    print(f"\nUptime      : {uptime()}")
    print(f"Python Ver  : {platform.python_version()}")

    print("\nGPU(s):")
    for line in gpu_info():
        print(f"  {line}")

    print("=" * 30 + "\n")


if __name__ == "__main__":
    show_status()
