import subprocess, os, sys, textwrap

REPO = "https://github.com/YourUser/novajr-skills.git"
CLONE_DIR = "/tmp/novajr-skills"

try:
    if not os.path.isdir(CLONE_DIR):
        subprocess.check_call(["git", "clone", "--depth", "1", REPO, CLONE_DIR])
    else:
        subprocess.check_call(["git", "-C", CLONE_DIR, "pull", "--depth", "1"])
    subprocess.check_call(["cp", "-r", f"{CLONE_DIR}/skills/.", "skills/"])
    result = "✅ Skills updated from GitHub."
except Exception as e:
    result = f"❌ Self‑update failed: {e}"

