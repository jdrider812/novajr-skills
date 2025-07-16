# llm_engine.py – minimal llama_cpp wrapper for Nova Jr
import os
from pathlib import Path
from llama_cpp import Llama

MODEL_PATH = os.environ.get("NOVA_MODEL", "/mnt/nova-jr/models/mistral-7b-instruct-v0.1.Q2_K.gguf")

# Keep one global instance so we don’t reload the model every query
_llama = None

def get_llama():
    global _llama
    if _llama is None:
        if not Path(MODEL_PATH).exists():
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
        _llama = Llama(
            model_path=str(MODEL_PATH),
            n_ctx=4096,
            n_gpu_layers=-1,    # let llama_cpp decide
            verbose=False,
        )
    return _llama

def ask(prompt: str, system_prompt: str = "You are Nova Jr, a helpful AI."):
    llama = get_llama()
    full_prompt = f"<s>[SYSTEM] {system_prompt}\n\n[USER] {prompt}\n\n[ASSISTANT]"
    output = llama(full_prompt, max_tokens=512, temperature=0.7, stop=["</s>", "[USER]"])
    return output["choices"][0]["text"].lstrip()
