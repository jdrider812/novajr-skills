import os

# === Memory Paths on SATA SSD ===
BASE_PATH = "/mnt/ssd2/nova-memory"

DB_PATH         = os.path.join(BASE_PATH, "db", "memory.db")
LOG_PATH        = os.path.join(BASE_PATH, "logs", "nova.log")
BACKUP_PATH     = os.path.join(BASE_PATH, "backups")
TMP_PATH        = os.path.join(BASE_PATH, "tmp")
KNOWLEDGE_PATH  = os.path.join(BASE_PATH, "knowledge")
SKILLS_PATH     = os.path.join(BASE_PATH, "skills")

# === Create all memory directories if they don't exist ===
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(LOG_PATH, exist_ok=True)
os.makedirs(BACKUP_PATH, exist_ok=True)
os.makedirs(TMP_PATH, exist_ok=True)
os.makedirs(KNOWLEDGE_PATH, exist_ok=True)
os.makedirs(SKILLS_PATH, exist_ok=True)
