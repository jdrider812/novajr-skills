from skill_manager import save_skill, load_skills

# Define a new skill as Python code
skill_name = "say_hi"
skill_code = """
def say_hi(name="Jon"):
    return f"Hi there, {name}! Great to see you."
"""

# Save the skill to disk
save_skill(skill_name, skill_code)

# Load skills and confirm
skills = load_skills()
print("🧠 Saved Skills:")
for name in skills:
    print(f"- {name}")
