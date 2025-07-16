from memory_manager import backup_memory, restore_memory
import os

# Backup current memory
backup_path = backup_memory()

# List available backups
print("\n📂 Available backups:")
for f in os.listdir("/mnt/ssd2/nova-memory/backups"):
    print("- " + f)

# Example: restore the most recent backup
filename = os.path.basename(backup_path)
print("\n🔄 Now restoring from:", filename)
restore_memory(filename)
