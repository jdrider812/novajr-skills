import importlib.util
import traceback

# Skill execution utility
def try_run_skill(prompt):
    if prompt.startswith("Run ") and "(" in prompt and prompt.endswith(")"):
        try:
            skill_name = prompt.split("Run ")[1].split("(")[0].strip()
            skill_path = f"/mnt/ssd2/nova-memory/skills/{skill_name}.py"

            if not os.path.exists(skill_path):
                return f"⚠️ Skill '{skill_name}' not found."

            # Dynamically load the skill module
            spec = importlib.util.spec_from_file_location(skill_name, skill_path)
            skill_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(skill_module)

            # Extract args from the prompt
            args = eval(prompt.split("Run ")[1])  # safe-ish in local dev

            # Call the skill function
            if isinstance(args, tuple):
                result = getattr(skill_module, skill_name)(*args)
            else:
                result = getattr(skill_module, skill_name)(args)

            return f"✅ Skill Result:\n{result}"
        except Exception as e:
            return f"❌ Error running skill:\n{traceback.format_exc()}"
    return None
