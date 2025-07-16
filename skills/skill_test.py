# /mnt/nova-jr/skill_test.py

from skill_manager import save_skill, load_skills, get_skill_by_name

# Save a new skill
save_skill(
    name="greet_user",
    description="Greets the user with their name",
    code="""
def greet_user(name):
    return f"Hello, {name}! Welcome back."
"""
)

# Load all skills
print("\n🧠 All Stored Skills:")
for skill in load_skills():
    print(f"- {skill['name']}: {skill['description']}")

# Retrieve specific skill
print("\n🔍 Testing Specific Skill:")
skill = get_skill_by_name("greet_user")
if skill:
    print("Skill Found:")
    print(skill["code"])
else:
    print("Skill not found.")
