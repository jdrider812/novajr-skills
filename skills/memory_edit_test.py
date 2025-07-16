from memory_manager import load_memory, remove_fact, replace_fact

print("\n🧠 Current Memory Facts:")
facts = load_memory()["facts"]
for i, fact in enumerate(facts):
    print(f"{i + 1}. {fact}")

print("\n=== Options ===")
print("1. Forget a fact")
print("2. Replace a fact")
choice = input("Enter your choice (1 or 2): ")

if choice == "1":
    idx = int(input("Enter the number of the fact to forget: ")) - 1
    if 0 <= idx < len(facts):
        print(f"\n🧹 Forgetting: {facts[idx]}")
        remove_fact(facts[idx])
    else:
        print("❌ Invalid number.")

elif choice == "2":
    idx = int(input("Enter the number of the fact to replace: ")) - 1
    if 0 <= idx < len(facts):
        new_fact = input("Enter the new fact: ").strip()
        print(f"\n♻️ Replacing: {facts[idx]} ➜ {new_fact}")
        replace_fact(facts[idx], new_fact)
    else:
        print("❌ Invalid number.")

else:
    print("❌ Invalid choice.")
