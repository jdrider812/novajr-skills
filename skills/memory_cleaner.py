# memory_cleaner.py

import json
import os

MEMORY_FILE = "/mnt/ssd2/nova-memory/memory.json"

def load_memory():
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def normalize_facts(facts):
    cleaned = []
    seen = set()

    for fact in facts:
        # Remove "Remember" if it starts the sentence
        if fact.lower().startswith("remember jon"):
            fact = fact[9:].strip().capitalize()
        elif fact.lower().startswith("remember"):
            fact = fact[8:].strip().capitalize()

        # Capitalize and fix minor inconsistencies
        if fact.lower().startswith("jon "):
            fact = "Jon " + fact[4:].strip()

        fact = fact.strip().rstrip(".")

        # Deduplicate
        if fact.lower() not in seen:
            seen.add(fact.lower())
            cleaned.append(fact)

    return cleaned

def run_cleaner():
    memory = load_memory()
    original_facts = memory.get("facts", [])
    cleaned_facts = normalize_facts(original_facts)
    memory["facts"] = cleaned_facts
    save_memory(memory)

    print("✅ Cleaned memory facts:")
    for fact in cleaned_facts:
        print("-", fact)

if __name__ == "__main__":
    run_cleaner()
