# chat_test.py

from chat_engine import ask_nova

chat_history = []

# Try a skill
chat_history, _ = ask_nova("Greet me as Jon", chat_history)

# Try memory
chat_history, _ = ask_nova("What do you remember about Jon?", chat_history)

# Try a new fact
chat_history, _ = ask_nova("Remember Jon likes cold brew coffee.", chat_history)

# Confirm memory updated
chat_history, _ = ask_nova("What do you remember about Jon?", chat_history)

# Print final chat history
for msg in chat_history:
    print(f"{msg['role']}: {msg['content']}")
