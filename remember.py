# remember.py – Save simple facts to memory.json
import re, json
from pathlib import Path

MEMORY_FILE = "memory/memory.json"
Path("memory").mkdir(exist_ok=True)

# Get input from Nova’s skill system
msg = (
    globals().get("input")
    or globals().get("user_input")
    or ""
).strip()

# First: check for explicit "Remember: …"
m = re.search(r"remember:\s*(.+)", msg, re.I)

if m:
    fact = m.group(1).strip()
else:
    # Fall back to using entire message as the fact
    fact = msg

# Load existing memory list or start new
mem_path = Path(MEMORY_FILE)
try:
    memory = json.loads(mem_path.read_text()) if mem_path.exists() else []
except json.JSONDecodeError:
    memory = []

# Store the fact if it’s new
if fact and fact not in memory:
    memory.append(fact)
    mem_path.write_text(json.dumps(memory, indent=2))

result = f"Got it! I’ll remember: {fact}"
