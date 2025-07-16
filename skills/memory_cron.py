#!/usr/bin/env python3
"""
memory_cron.py
Run once per day (via cron, systemd-timer, or @reboot loop) to:
• drop expired short-term facts
• vacuum the JSON DB to keep it small
• create an automatic backup
"""

import json, os, time, shutil, datetime, uuid
MEM_PATH   = "/mnt/ssd2/nova-memory/memory.json"
BACK_DIR   = "/mnt/ssd2/nova-memory/backups"
os.makedirs(BACK_DIR, exist_ok=True)

NOW = time.time()

def load():
    if not os.path.exists(MEM_PATH):
        return {"facts": [], "preferences": {}}
    with open(MEM_PATH) as f:
        return json.load(f)

def save(data):
    with open(MEM_PATH, "w") as f:
        json.dump(data, f, indent=4)

def backup():
    fn = f"auto_{datetime.datetime.now():%Y%m%d-%H%M%S}_{uuid.uuid4().hex}.json"
    shutil.copy(MEM_PATH, os.path.join(BACK_DIR, fn))
    return fn

def clean_expired(mem):
    before = len(mem["facts"])
    mem["facts"] = [
        f for f in mem["facts"]
        if not (isinstance(f, dict) and f.get("expires_at", 9e99) < NOW)
    ]
    return before - len(mem["facts"])

if __name__ == "__main__":
    data  = load()
    gone  = clean_expired(data)
    save(data)
    bk = backup()
    print(f"✅ Memory cleanup complete. Removed {gone} expired facts.")
    print(f"📦 Backup saved as {bk}")
