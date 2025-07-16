#!/usr/bin/env python3
import subprocess
import datetime

LOG_FILE = "auto_self_update.log"

def main():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        output = subprocess.check_output(
            ["./nova_cli.py", "chat", "self_update"],
            stderr=subprocess.STDOUT
        ).decode()
        result = f"[{now}] SUCCESS:\n{output}\n"
    except subprocess.CalledProcessError as e:
        result = f"[{now}] ERROR:\n{e.output.decode()}\n"
    with open(LOG_FILE, "a") as f:
        f.write(result)

if __name__ == "__main__":
    main()
