from chat_engine import ask_nova
import os
import json
from datetime import datetime

# Path to chat logs
CHAT_LOG_DIR = "/mnt/ssd2/nova-memory/chat_logs"
os.makedirs(CHAT_LOG_DIR, exist_ok=True)

# New conversation
chat_history = []

# Test message
chat_history, updated = ask_nova("How are you today?", chat_history)

# Save chat log with timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
log_file = os.path.join(CHAT_LOG_DIR, f"chat_{timestamp}.json")
with open(log_file, "w") as f:
    json.dump(updated, f, indent=2)

print(f"✅ Chat log saved to: {log_file}")
