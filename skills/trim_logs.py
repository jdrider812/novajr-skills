#!/usr/bin/env python3
"""
trim_logs.py – deletes chat logs older than 7 days
"""

import os, time
from pathlib import Path

# Settings
CHAT_LOG_DIR = Path("/mnt/ssd2/nova-memory/chat_logs")
DAYS_TO_KEEP = 7

def trim_logs():
    now = time.time()
    cutoff = now - DAYS_TO_KEEP * 86400
    deleted = []

    for file in CHAT_LOG_DIR.glob("*.jsonl"):
        if file.stat().st_mtime < cutoff:
            deleted.append(file.name)
            file.unlink()

    if deleted:
        print(f"🧹 Deleted old logs: {len(deleted)}")
        for f in deleted:
            print(" -", f)
    else:
        print("✅ No old logs to delete.")

if __name__ == "__main__":
    trim_logs()
