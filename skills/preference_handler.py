import re
from memory_manager import update_preferences

def handle_preference_update(prompt):
    prompt_lower = prompt.lower()

    # Step-by-step style
    if "step-by-step" in prompt_lower:
        update_preferences({"reply_style": "step-by-step"})
        return "✅ Preference updated: reply_style = step-by-step"

    # Casual style
    if "casual" in prompt_lower:
        update_preferences({"reply_style": "casual"})
        return "✅ Preference updated: reply_style = casual"

    # Short replies
    if "short replies" in prompt_lower or "shorter answers" in prompt_lower:
        update_preferences({"reply_length": "short"})
        return "✅ Preference updated: reply_length = short"

    # Detailed replies
    if "more detail" in prompt_lower or "be detailed" in prompt_lower:
        update_preferences({"reply_length": "detailed"})
        return "✅ Preference updated: reply_length = detailed"

    # Emoji replies
    if "use emojis" in prompt_lower:
        update_preferences({"use_emojis": True})
        return "✅ Preference updated: use_emojis = True"

    if "no emojis" in prompt_lower:
        update_preferences({"use_emojis": False})
        return "✅ Preference updated: use_emojis = False"

    return None
