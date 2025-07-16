#!/usr/bin/env python3
"""
nova_config.py
==============
Single helper to read and write Nova Jr’s config.json.
"""

import json
from pathlib import Path

CONFIG_PATH = Path("/mnt/nova-jr/config.json")

def load_config() -> dict:
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open(encoding="utf-8") as f:
            return json.load(f)
    raise FileNotFoundError("config.json not found")

def save_config(cfg: dict):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))

