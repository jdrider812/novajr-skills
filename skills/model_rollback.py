#!/usr/bin/env python3
"""
model_rollback.py
Restore a previous model version recorded in git (latest.json).
Usage:
    ./model_rollback.py <git-ref>     # e.g. HEAD~1 or <commit-hash>
"""
import json, subprocess, shutil, sys, hashlib, urllib.request, pathlib, tempfile

REPO_DIR   = pathlib.Path(__file__).parent
LATEST_JS  = REPO_DIR / "latest.json"
MODEL_DIR  = REPO_DIR / "llama.cpp" / "build" / "models"
MODEL_FILE = MODEL_DIR / "mistral.gguf"

def load_latest(ref: str):
    data = subprocess.check_output(["git", "show", f"{ref}:latest.json"],
                                   cwd=REPO_DIR, text=True)
    return json.loads(data)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def download(url, dest):
    print(f"⬇️  downloading {url} …")
    with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)

def main():
    if len(sys.argv) != 2:
        print("Usage: model_rollback.py <git-ref>"); sys.exit(1)
    ref = sys.argv[1]

    meta = load_latest(ref)
    want_sha = meta["sha256"]; url = meta["url"]
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # download to temp if needed
    if MODEL_FILE.exists() and sha256(MODEL_FILE) == want_sha:
        print("✓ Model already matches selected version."); return
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        download(url, tmp.name)
        if sha256(tmp.name) != want_sha:
            print("❌ Checksum mismatch – aborting."); sys.exit(1)
        shutil.move(tmp.name, MODEL_FILE)
    # overwrite working latest.json so future updates start from here
    with open(LATEST_JS, "w") as f: json.dump(meta, f, indent=2)
    print("✅ Rolled back and locked to commit", ref)

if __name__ == "__main__":
    main()
