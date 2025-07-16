#!/usr/bin/env python3
"""
model_updater.py  – nightly job that checks a manifest and
                    downloads + swaps in a newer .gguf model if needed.
This variant uses a LOCAL manifest so you can test without hosting files.
"""

import os, json, hashlib, urllib.request, subprocess, argparse, shutil, sys, time
from pathlib import Path

# ── paths ───────────────────────────────────────────────────────────────────
BASE        = Path("/mnt/nova-jr")
MODELS_DIR  = BASE / "llama.cpp" / "build" / "models"
CURRENT     = MODELS_DIR / "mistral.gguf"          #  in-use file
MANIFEST    = BASE / "latest.json"                 #  local manifest
BACKUP_DIR  = MODELS_DIR / "old"

# ── helper: sha-256 of a file ───────────────────────────────────────────────
def sha256_of(fp: Path, buf=131072) -> str:
    h = hashlib.sha256()
    with fp.open("rb") as f:
        while chunk := f.read(buf):
            h.update(chunk)
    return h.hexdigest()

# ── load manifest (local file URL) ──────────────────────────────────────────
def fetch_manifest() -> dict:
    if MANIFEST.is_file():
        return json.loads(MANIFEST.read_text())
    raise FileNotFoundError(f"Manifest {MANIFEST} not found")

# ── download new model if url starts with http(s) or file:// ────────────────
def download(url: str, out: Path):
    if url.startswith("file://"):          # local copy
        src = Path(url[7:])
        shutil.copy(src, out)
    else:                                  # remote
        with urllib.request.urlopen(url) as r, out.open("wb") as f:
            shutil.copyfileobj(r, f)

# ── main logic ──────────────────────────────────────────────────────────────
def check_and_update(check_only=False):
    m = fetch_manifest()
    manifest_ver   = m["version"]
    manifest_url   = m["url"]
    manifest_sha   = m["sha256"]

    CURRENT.parent.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(exist_ok=True)

    if CURRENT.exists() and sha256_of(CURRENT) == manifest_sha:
        print("✓ Model already up-to-date")
        return

    if check_only:
        print("⚠️  New model available but --check-only set")
        return

    tmp = CURRENT.with_suffix(".download")
    print(f"⬇️  Downloading {manifest_url} …")
    download(manifest_url, tmp)

    if sha256_of(tmp) != manifest_sha:
        tmp.unlink(missing_ok=True)
        raise RuntimeError("❌ SHA256 mismatch; aborting")

    # backup current
    if CURRENT.exists():
        ts = time.strftime("%Y%m%d-%H%M%S")
        CURRENT.rename(BACKUP_DIR / f"mistral_{ts}.gguf")

    tmp.rename(CURRENT)
    print(f"✅ Updated to version {manifest_ver}")

# ── CLI ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true", help="just report")
    args = ap.parse_args()
    try:
        check_and_update(check_only=args.check_only)
    except Exception as e:
        print(f"⚠️  Model update failed: {e}")
        sys.exit(1)
