import requests
from pathlib import Path

def run(command: str) -> str:
    parts = command.split()
    if len(parts) != 2:
        return "Usage: download_file <url>"

    url = parts[1]
    filename = url.split("/")[-1]
    save_path = Path("skills") / filename

    try:
        response = requests.get(url)
        response.raise_for_status()
        save_path.write_bytes(response.content)
        return f"Downloaded {filename} to skills/"
    except Exception as e:
        return f"Failed to download: {e}"
