#!/usr/bin/env python3
"""
nova_dashboard.py
-----------------
Web UI for Nova Jr (Gradio 5.x)
"""

import gradio as gr, json, psutil, platform, time, subprocess
from pathlib import Path

from nova_chat_engine import generate_reply
from nova_memory import load_memory, remember, forget
from nova_config import load_config

# ---------- helpers ----------
def system_snapshot():
    m = psutil.virtual_memory()
    try:
        out = subprocess.check_output(
            ["nvidia-smi","--query-gpu=name,memory.total","--format=csv,noheader"],
            encoding="utf-8")
        gpu = "\n".join(out.strip().splitlines())
    except Exception:
        gpu = "nvidia-smi not found"
    return (f"{psutil.cpu_percent()} %",             # CPU
            f"{m.used//2**20}/{m.total//2**20} MiB", # RAM
            time.strftime('%H:%M:%S',time.gmtime(time.time()-psutil.boot_time())),
            platform.python_version(),
            gpu)

def refresh_memory():
    kv = load_memory()
    return "\n".join(f"{k} = {v}" for k,v in kv.items()) or "(empty)"

def add_memory(pair):
    if "=" not in pair: return gr.update(value="Format key=value"), refresh_memory()
    k,v = pair.split("=",1); remember(k.strip(),v.strip())
    return gr.update(value=""), refresh_memory()

def del_memory(key):
    forget(key.strip()); return refresh_memory()

def chat_fn(history, user_msg):
    if not user_msg: return history, ""
    reply = generate_reply(user_msg)
    history.append({"role":"user","content":user_msg})
    history.append({"role":"assistant","content":reply})
    return history, ""

# ---------- UI ----------
with gr.Blocks(title="Nova Jr Dashboard") as demo:
    gr.Markdown("# 🛰️ Nova Jr Dashboard")

    with gr.Row():
        with gr.Column(scale=3):              # Chat
            chatbot = gr.Chatbot(height=400, label="Chat with Nova Jr", type="messages")
            msg_box = gr.Textbox(placeholder="Type a message…")
            send_btn= gr.Button("Send")

        with gr.Column(scale=1):              # Side panel
            status_btn = gr.Button("🔄 Refresh Status")
            cpu = gr.Textbox(label="CPU")
            ram = gr.Textbox(label="RAM")
            up  = gr.Textbox(label="Uptime")
            pyv = gr.Textbox(label="Python")
            gpu = gr.Textbox(label="GPU")

            gr.Markdown("### Memory")
            mem_display = gr.Textbox(lines=8, interactive=False)
            mem_add = gr.Textbox(placeholder="key=value")
            add_btn = gr.Button("Add / Update")
            del_btn = gr.Button("Delete Key")

            cfg_btn = gr.Button("View config.json")
            cfg_out = gr.Code(label="config.json")

    # wiring
    send_btn.click(chat_fn, [chatbot,msg_box],[chatbot,msg_box])
    msg_box.submit(chat_fn,[chatbot,msg_box],[chatbot,msg_box])

    status_btn.click(system_snapshot, outputs=[cpu,ram,up,pyv,gpu])
    status_btn.click(refresh_memory, outputs=mem_display)

    add_btn.click(add_memory, mem_add, [mem_add, mem_display])
    del_btn.click(del_memory, mem_add, mem_display)

    cfg_btn.click(lambda: json.dumps(load_config(),indent=2), outputs=cfg_out)

    demo.load(system_snapshot, outputs=[cpu,ram,up,pyv,gpu])
    demo.load(refresh_memory, outputs=mem_display)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
