#!/usr/bin/env python3
"""
git_autocommit.py
Automatically stages & commits latest.json when it has changed.
"""

import subprocess, hashlib, json, os, sys, time
from pathlib import Path

REPO        = Path("/mnt/nova-jr")
LATEST_JSON = REPO / "latest.json"

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def run(cmd, **kw):
    kw.setdefault("check", True)
    return subprocess.run(cmd, text=True, capture_output=True, **kw)

def main():
    os.chdir(REPO)

    # 1️⃣  ensure repository exists
    if not (REPO / ".git").is_dir():
        run(["git", "init"])

    # 2️⃣  compute working-tree hash & last committed hash
    working_hash = file_sha256(LATEST_JSON)

    # may fail if file never committed before
    try:
        res = run(["git", "show", "HEAD:latest.json"])
        committed_hash = hashlib.sha256(res.stdout.encode()).hexdigest()
    except subprocess.CalledProcessError:
        committed_hash = None

    # 3️⃣  commit only if changed
    if working_hash != committed_hash:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        run(["git", "add", "latest.json"])
        run(["git", "-c", "user.name=Nova Jr",
                     "-c", "user.email=nova@localhost",
                     "commit", "-m", f"💾 Auto-lock model ({ts})"])
        print("✅ Committed new model lock.")
    else:
        print("✓ latest.json already matches HEAD – nothing to do.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"⚠️  Auto-commit failed: {e}", file=sys.stderr)
        sys.exit(1)
