# memory_summary_test.py

from chat_engine import ask_nova

chat_history = []

# Ask Nova Jr to summarize what he knows about Jon
chat_history, updated = ask_nova("Summarize everything you remember about Jon.", chat_history)

# Print chat response
for msg in updated:
    print(f"{msg['role']}: {msg['content']}")
