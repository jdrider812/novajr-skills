#!/usr/bin/env python3
import readline
from chat_engine import ask_nova

chat_history = []

print("🤠 Nova Jr is online. Type 'exit' to quit.\n")

while True:
    try:
        user_input = input("You: ")
        if user_input.strip().lower() in {"exit", "quit"}:
            print("👋 Shutting down Nova Jr.")
            break

        chat_history, updated = ask_nova(user_input, chat_history)
        print(f"Nova Jr: {updated[-1]['content']}")

    except KeyboardInterrupt:
        print("\n👋 Shutting down Nova Jr.")
        break
    except Exception as e:
        print(f"⚠️ Error: {e}")
