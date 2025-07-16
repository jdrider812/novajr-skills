# STEP 1: Setup paths for Nova Jr's memory system
import os
import json
import datetime

# Base memory folder (on SSD)
BASE_PATH = "/mnt/ssd2/nova-memory"

# Subdirectories
DB_PATH         = os.path.join(BASE_PATH, "db", "memory.db")
LOG_PATH        = os.path.join(BASE_PATH, "logs", "nova.log")
BACKUP_PATH     = os.path.join(BASE_PATH, "backups")
TMP_PATH        = os.path.join(BASE_PATH, "tmp")
KNOWLEDGE_PATH  = os.path.join(BASE_PATH, "knowledge")
SKILLS_PATH     = os.path.join(BASE_PATH, "skills")

# Create all memory directories (safe to re-run)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(LOG_PATH, exist_ok=True)
os.makedirs(BACKUP_PATH, exist_ok=True)
os.makedirs(TMP_PATH, exist_ok=True)
os.makedirs(KNOWLEDGE_PATH, exist_ok=True)
os.makedirs(SKILLS_PATH, exist_ok=True)

# STEP 2: Persistent memory file
MEMORY_FILE = os.path.join(BASE_PATH, "memory.json")

# Initialize if missing
def init_memory():
    if not os.path.exists(MEMORY_FILE):
        data = {
            "name": "Nova Jr",
            "creator": "Jon",
            "facts": ["Jon prefers full code blocks", "Jon uses Tesla V100 GPUs"],
            "preferences": {"reply_style": "step-by-step"},
            "created": datetime.datetime.now().isoformat()
        }
        with open(MEMORY_FILE, 'w') as f:
            json.dump(data, f, indent=4)

# Load memory
def load_memory():
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

# Save memory
def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# STEP 3: Test it works
if __name__ == '__main__':
    init_memory()
    memory = load_memory()
    print("Loaded memory for:", memory['name'])
    print("Facts I know:")
    for fact in memory['facts']:
        print("-", fact)
