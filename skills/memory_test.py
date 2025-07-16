# /mnt/nova-jr/memory_test.py

from memory_manager import load_memory, add_fact

# Show current memory
print("📖 Current memory:")
memory = load_memory()
for fact in memory.get("facts", []):
    print("-", fact)

# Add a new fact
new_fact = "Nova Jr runs on Jon's custom hardware"
add_fact(new_fact)

# Show updated memory
print("\n✅ Updated memory:")
memory = load_memory()
for fact in memory.get("facts", []):
    print("-", fact)
