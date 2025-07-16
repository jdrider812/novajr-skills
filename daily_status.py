# daily_status.py – system + crypto snapshot
import subprocess, urllib.request, json
from datetime import datetime
from pathlib import Path

# ---------- helpers ----------
def get_uptime():
    try:
        return subprocess.check_output(["uptime", "-p"], text=True).strip()
    except Exception as e:
        return f"uptime error: {e}"

def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())
        return data[coin]["usd"]
    except Exception:
        return "N/A"

# ---------- build summary ----------
now     = datetime.now().strftime("%A, %B %d %Y – %I:%M %p")
uptime  = get_uptime()
btc     = get_price("bitcoin")
eth     = get_price("ethereum")
doge    = get_price("dogecoin")

result = (
    f"📅 {now}\n"
    f"🖥️  Uptime: {uptime}\n"
    f"💰 Crypto – BTC: {btc} USD | ETH: {eth} USD | DOGE: {doge} USD"
)
