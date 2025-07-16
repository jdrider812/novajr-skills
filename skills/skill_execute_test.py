import importlib.util
import os
import re

SKILLS_DIR = "/mnt/ssd2/nova-memory/skills"

def try_run_skill(command):
    match = re.match(r"(\w+)(?:\((.*?)\))?", command)
    if not match:
        return "❌ Invalid skill format."

    skill_name = match.group(1)
    args_str = match.group(2)
    args = []

    if args_str:
        try:
            args = [eval(arg.strip()) for arg in args_str.split(",")]
        except Exception as e:
            return f"❌ Failed to parse arguments: {e}"

    skill_path = os.path.join(SKILLS_DIR, f"{skill_name}.py")
    if not os.path.exists(skill_path):
        return f"❌ Skill '{skill_name}' not found."

    try:
        spec = importlib.util.spec_from_file_location(skill_name, skill_path)
        skill_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(skill_module)

        func = getattr(skill_module, skill_name)
        result = func(*args)
        return result
    except Exception as e:
        return f"❌ Error running skill '{skill_name}': {e}"

# === Test Loop ===
while True:
    user_input = input("user: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    response = try_run_skill(user_input)
    print(f"assistant: {response}")
