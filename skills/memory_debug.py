# memory_debug.py

from memory_manager import load_memory

memory = load_memory()

print("✅ Memory loaded:")
for fact in memory.get("facts", []):
    print("-", fact)
