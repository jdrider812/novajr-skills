#!/usr/bin/env python3
"""
log_trimmer.py – Keep only the 10 most recent chat logs
"""

import os
import glob

# Where logs are stored
LOG_DIR = "/mnt/ssd2/nova-memory/chat_logs"
LOG_GLOB = os.path.join(LOG_DIR, "*.jsonl")

# Sort by modified time (newest first)
all_logs = sorted(glob.glob(LOG_GLOB), key=os.path.getmtime, reverse=True)

# Keep the 10 most recent, delete the rest
old_logs = all_logs[10:]

for path in old_logs:
    try:
        os.remove(path)
        print(f"🗑️  Deleted: {path}")
    except Exception as e:
        print(f"⚠️  Could not delete {path}: {e}")
