#!/usr/bin/env python3
"""
config_editor.py
================

Gradio-based settings editor for Nova Jr's config.json.
Allows quick tuning of parameters like personality, reply style, etc.
"""

from pathlib import Path
import json
import gradio as gr

CONFIG_PATH = Path("/mnt/nova-jr/config.json")


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_config(updated: dict) -> str:
    try:
        with CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(updated, f, indent=2)
        return "✅ Config saved successfully!"
    except Exception as e:
        return f"❌ Failed to save: {e}"


def build_interface():
    cfg = load_config()

    with gr.Blocks(title="Nova Jr – Config Editor") as ui:
        gr.Markdown("# ⚙️ Nova Jr Config Editor")

        with gr.Row():
            personality = gr.Textbox(value=cfg.get("personality", ""), label="Personality", lines=1)
            reply_style = gr.Textbox(value=cfg.get("reply_style", ""), label="Reply Style", lines=1)

        with gr.Row():
            model_path = gr.Textbox(value=cfg.get("model_path", ""), label="Model File Path", lines=1)
            max_memory = gr.Number(value=cfg.get("max_memory", 100), label="Max Memory Entries")

        status = gr.Textbox(label="Status", interactive=False)

        def save_all(p, r, m, mm):
            new_cfg = {
                "personality": p,
                "reply_style": r,
                "model_path": m,
                "max_memory": int(mm),
            }
            return save_config(new_cfg)

        save_btn = gr.Button("💾 Save Settings")
        save_btn.click(
            fn=save_all,
            inputs=[personality, reply_style, model_path, max_memory],
            outputs=status,
        )

    return ui


if __name__ == "__main__":
    build_interface().launch(
        server_name="0.0.0.0",
        server_port=7862,
        share=False,
        inbrowser=True,
    )
