from chat_engine import ask_nova

chat_history = []

# 🧠 Tell Nova Jr to learn a new skill
prompt = """Create a skill called add_numbers
```python
def add_numbers(a, b):
    return a + b
```"""

chat_history, updated = ask_nova(prompt, chat_history)

# ✅ Show output
for msg in updated:
    print(f"{msg['role']}: {msg['content']}")
