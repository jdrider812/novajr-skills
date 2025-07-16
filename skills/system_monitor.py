#!/usr/bin/env python3
"""
system_monitor.py
=================

Local system monitor panel for Nova Jr.
Shows live CPU, memory, GPU usage, and uptime.
"""

import subprocess
import platform
import psutil
import gradio as gr
from datetime import timedelta


def get_uptime() -> str:
    uptime_sec = int(psutil.boot_time())
    current = int(psutil.time.time())
    return str(timedelta(seconds=current - uptime_sec))


def get_gpu_usage() -> str:
    try:
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"], encoding="utf-8")
        lines = output.strip().splitlines()
        results = []
        for idx, line in enumerate(lines):
            gpu_util, mem_used, mem_total = line.split(", ")
            results.append(f"GPU {idx}: {gpu_util}% | {mem_used} / {mem_total} MiB")
        return "\n".join(results)
    except Exception:
        return "⚠️ No GPU info available (nvidia-smi not found?)"


def get_stats() -> dict:
    return {
        "CPU Usage": f"{psutil.cpu_percent()}%",
        "RAM Used": f"{psutil.virtual_memory().used // (1024**2)} MB / {psutil.virtual_memory().total // (1024**2)} MB",
        "Uptime": get_uptime(),
        "GPU Stats": get_gpu_usage(),
        "Platform": platform.platform()
    }


def build_ui():
    with gr.Blocks(title="Nova Jr – System Monitor") as ui:
        gr.Markdown("# 🖥️ Nova Jr System Monitor\nLive view of system performance and GPU load.")

        cpu = gr.Textbox(label="CPU Usage")
        ram = gr.Textbox(label="RAM Usage")
        uptime = gr.Textbox(label="Uptime")
        gpu = gr.Textbox(label="GPU(s)", lines=4)
        plat = gr.Textbox(label="OS / Platform")

        def refresh():
            stats = get_stats()
            return stats["CPU Usage"], stats["RAM Used"], stats["Uptime"], stats["GPU Stats"], stats["Platform"]

        refresh_btn = gr.Button("🔄 Refresh Stats")
        refresh_btn.click(refresh, outputs=[cpu, ram, uptime, gpu, plat])

    return ui


if __name__ == "__main__":
    build_ui().launch(
        server_name="0.0.0.0",
        server_port=7863,
        share=False,
        inbrowser=True,
    )
