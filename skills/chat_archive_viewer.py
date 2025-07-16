#!/usr/bin/env python3
"""
chat_archive_viewer.py
======================

A lightweight Gradio web interface for browsing trimmed Nova Jr chat logs.

Launch:
    python3 chat_archive_viewer.py
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Tuple
import gradio as gr

# --------------------------------------------------
# Configuration
# --------------------------------------------------
LOG_DIR = Path("/mnt/nova-jr/logs")
FILE_EXT_WHITELIST = {".txt", ".log", ".jsonl"}

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def get_log_files() -> List[str]:
    return sorted(
        [f.name for f in LOG_DIR.iterdir() if f.is_file() and f.suffix.lower() in FILE_EXT_WHITELIST],
        reverse=True,
    )


def read_log_file(fname: str) -> str:
    path = LOG_DIR / fname
    if not path.exists():
        return f"⚠️ File not found: {fname}"

    if path.suffix.lower() == ".jsonl":
        lines = []
        with path.open(encoding="utf-8") as f:
            for raw in f:
                try:
                    obj = json.loads(raw)
                    role = obj.get("role", "unknown").title()
                    content = obj.get("content", "").strip()
                    lines.append(f"**{role}:** {content}")
                except json.JSONDecodeError:
                    lines.append(f"⚠️ Bad JSON:\n{raw}")
        return "\n\n".join(lines)

    # Plain-text passthrough
    return path.read_text(encoding="utf-8")


# --------------------------------------------------
# Gradio Interface
# --------------------------------------------------
def build_interface() -> gr.Blocks:
    with gr.Blocks(title="Nova Jr – Chat Archive Viewer") as demo:
        gr.Markdown(
            "# 📜 Nova Jr Chat Archive Viewer\nSelect any log on the left to view its contents."
        )
        with gr.Row():
            file_list = gr.Radio(
                choices=get_log_files(),
                label="Available Logs",
                value=None,
                interactive=True,
            )
            viewer = gr.Markdown(label="Log Contents")

        # --- Callbacks ---
        file_list.change(
            lambda f: read_log_file(f) if f else "Select a file to preview…",
            inputs=file_list,
            outputs=viewer,
        )

        def refresh_files() -> Tuple[List[str], None]:
            return gr.update(choices=get_log_files()), None

        gr.Button("🔄 Refresh List").click(refresh_files, outputs=[file_list, viewer])

    return demo


# --------------------------------------------------
# Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    build_interface().launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        inbrowser=True,
    )
