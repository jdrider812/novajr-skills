import sys
import os
import urllib.request

def run(*args):
    if not args:
        return "Usage: download_file <url> [<destination_folder>]"
    url = args[0]
    folder = args[1] if len(args) > 1 else "downloads"
    os.makedirs(folder, exist_ok=True)
    filename = url.split("/")[-1].split("?")[0] or "downloaded_file"
    dest = os.path.join(folder, filename)
    try:
        urllib.request.urlretrieve(url, dest)
        return f"✅ Downloaded: {url}\n→ Saved as: {dest}"
    except Exception as e:
        return f"❌ Download failed: {e}"
