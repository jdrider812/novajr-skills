import sqlite3
import subprocess
import os
import gradio as gr
from datetime import datetime

# === Paths ===
DB_PATH = "/mnt/nova-jr/memory.db"
MODEL_PATH = "/mnt/nova-jr/llama.cpp/build/models/mistral.gguf"
LLAMA_CLI = "/mnt/nova-jr/llama.cpp/build/bin/llama-cli"

# === SQLite Setup ===
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        sender TEXT,
        message TEXT
    )
""")
conn.commit()

# === Save Message ===
def save_message(sender, message):
    cursor.execute("INSERT INTO chat (timestamp, sender, message) VALUES (?, ?, ?)",
                   (datetime.now().isoformat(), sender, message))
    conn.commit()

# === Get Recent Conversation ===
def get_conversation(n=5):
