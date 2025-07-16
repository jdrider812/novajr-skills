#!/usr/bin/env python3
"""
nova_chat_engine.py
===================
Generates replies with automatic memory context.

• Reads config.json
• Injects key‑value memory into every prompt
• Uses llama‑2 chat format (works well with Mistral GGUF)
• Silences all backend logs
"""

import os, json
from pathlib import Path
from llama_cpp import Llama, LlamaCache
from nova_memory import load_memory

# ---- silence ALL llama‑cpp console spam ----
os.environ["LLAMA_LOG_LEVEL"] = "None"

CONFIG_PATH = Path("/mnt/nova-jr/config.json")
_MODEL = None


def _cfg() -> dict:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    raise FileNotFoundError("config.json not found")


def _model():
    global _MODEL
    if _MODEL:
        return _MODEL
    cfg = _cfg()
    path = Path(cfg["model_path"]).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")

    _MODEL = Llama(
        model_path=str(path),
        n_ctx=4096,
        n_threads=8,
        chat_format="llama-2",   # >>> plain format Mistral understands
        verbose=False,
        cache=LlamaCache(),
    )
    return _MODEL


def _memory_block() -> str:
    kv = load_memory()
    if not kv:
        return "(no prior memories stored)"
    return "\n".join(f"* {k}: {v}" for k, v in kv.items())


def _prompt(user: str) -> str:
    cfg = _cfg()
    sys_msg = (
        f"You are Nova Jr, a helpful AI with a {cfg.get('personality','')} personality."
    )
    style = cfg.get("reply_style", "concise")
    mem  = _memory_block()

    # llama‑2 chat format: <s>[INST] system ... [/INST] user [/INST]
    return (
        f"<s>[INST] {sys_msg}\n"
        f"You know these facts about the user and must use them when relevant:\n{mem}\n"
        f"(Respond {style}) [/INST]\n"
        f"{user} [/INST]"
    )


def generate_reply(prompt: str) -> str:
    llm = _model()
    out = llm(
        _prompt(prompt),
        max_tokens=400,
        temperature=0.7,
        top_p=0.95,
        stop=["</s>"],
    )
    return out["choices"][0]["text"].strip()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: nova_chat_engine.py \"Your prompt\"")
        raise SystemExit
    print(generate_reply(" ".join(sys.argv[1:])))
