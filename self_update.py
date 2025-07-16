# self_update.py – pull skills from GitHub repo
"""
Usage:
  self_update                       # pulls latest main branch
  self_update branch:<branch_name>  # pulls a specific branch
"""

import subprocess, os, shlex, re

REPO_URL  = "https://github.com/YourGitHubUser/novajr-skills.git"   # ← change me
CLONE_DIR = "/tmp/novajr-skills"

# --- parse branch arg -----------------------------------------------------
raw = (globals().get("input") or "").strip()
branch = None
m = re.search(r"branch:(\S+)", raw)
if m:
    branch = m.group(1)

# --- clone or pull --------------------------------------------------------
try:
    if not os.path.isdir(CLONE_DIR):
        subprocess.check_call(
            ["git", "clone", "--depth", "1", REPO_URL, CLONE_DIR]
        )
    else:
        subprocess.check_call(
            ["git", "-C", CLONE_DIR, "fetch", "--depth", "1", "origin"]
        )

    # checkout desired branch
    if branch:
        subprocess.check_call(["git", "-C", CLONE_DIR, "checkout", branch])
        subprocess.check_call(["git", "-C", CLONE_DIR, "pull", "origin", branch])
    else:
        subprocess.check_call(["git", "-C", CLONE_DIR, "checkout", "main"])
        subprocess.check_call(["git", "-C", CLONE_DIR, "pull", "origin", "main"])

    # copy updated skills into live dir
    subprocess.check_call(
        shlex.split(f"cp -r {CLONE_DIR}/skills/*.py skills/")
    )

    result = (
        f"✅ Skills updated from {REPO_URL}"
        + (f" (branch {branch})" if branch else "")
    )
except subprocess.CalledProcessError as e:
    result = f"❌ Git error: {e}"
except Exception as e:
    result = f"❌ Self‑update failed: {e}"
