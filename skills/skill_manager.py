import os
import importlib.util

SKILL_DIR = "/mnt/ssd2/nova-memory/skills"

def try_run_skill(prompt):
    for filename in os.listdir(SKILL_DIR):
        if filename.endswith(".py"):
            skill_name = filename[:-3]
            skill_path = os.path.join(SKILL_DIR, filename)

            spec = importlib.util.spec_from_file_location(skill_name, skill_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                func = getattr(module, skill_name, None)
                if callable(func) and skill_name.lower() in prompt.lower():
                    return func()
            except Exception as e:
                return f"❌ Error loading skill '{skill_name}': {e}"

    return None
