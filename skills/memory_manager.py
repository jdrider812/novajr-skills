import os, json, time, shutil, datetime, uuid

# ---------- Paths ----------
BASE_DIR    = "/mnt/ssd2/nova-memory"
MEMORY_FILE = os.path.join(BASE_DIR, "memory.json")
BACKUP_DIR  = os.path.join(BASE_DIR, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

# ---------- TTL defaults ----------
TTL_SECONDS_DEFAULT = 60 * 60 * 24 * 90      # 90 days
TTL_SECONDS_SHORT   = 60 * 60 * 24 * 14      # 14 days

# ---------- Pruning / summary caps ----------
MAX_FACTS         = 12          # keep at most 12 facts
SUMMARY_TRIGGER   = 10          # create summary when >= 10 facts

# ---------- Helpers ----------
def _now() -> float: return time.time()

def _make_fact(text, ttl=TTL_SECONDS_DEFAULT, pinned=False):
    return {
        "id": str(uuid.uuid4()),
        "text": text,
        "created": _now(),
        "hits": 0,
        "expires_at": _now() + ttl,
        "pinned": pinned,
    }

# ---------- File I/O ----------
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=4)

# ---------- Backup ----------
def backup_memory():
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"memory_backup_{ts}.json")
    shutil.copy(MEMORY_FILE, backup_path)
    return backup_path

def restore_memory(backup_name):
    src = os.path.join(BACKUP_DIR, backup_name)
    shutil.copy(src, MEMORY_FILE)

# ---------- Fact operations ----------
def add_fact(text, important=False, short=False):
    mem = load_memory()
    ttl = TTL_SECONDS_SHORT if short else TTL_SECONDS_DEFAULT
    fact = _make_fact(text, ttl=ttl, pinned=important)
    mem.setdefault("facts", []).append(fact)
    save_memory(mem)
    return summarise_and_prune()  # also handles summary/prune

def bump_fact_usage(text):
    mem = load_memory()
    for f in mem.get("facts", []):
        if (isinstance(f, str) and f == text) or (isinstance(f, dict) and f["text"] == text):
            if isinstance(f, dict):
                f["hits"] += 1
    save_memory(mem)

def get_facts():
    mem = load_memory()
    return [f if isinstance(f, str) else f["text"] for f in mem.get("facts", [])]

# ---------- Summary / pruning ----------
def _generate_summary(facts):
    preview = "; ".join([(f if isinstance(f, str) else f["text"]) for f in facts[:5]])
    return f"Summary: {preview} ..."

def summarise_and_prune():
    mem   = load_memory()
    facts = mem.get("facts", [])

    # --- summary ---
    if len(facts) >= SUMMARY_TRIGGER:
        mem["summary"] = _generate_summary(facts)

    # --- prune if over cap ---
    if len(facts) > MAX_FACTS:
        sortable = []
        for f in facts:
            if isinstance(f, str):
                sortable.append((False, 0, 0, f))
            else:
                sortable.append((f["pinned"], f["hits"], f["created"], f))
        sortable.sort(reverse=True)           # highest score first
        mem["facts"] = [x[-1] for x in sortable[:MAX_FACTS]]

    save_memory(mem)
    return "🧹 Memory summarised / trimmed."

