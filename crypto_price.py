# crypto_price.py – fixed version using correct CoinGecko coin IDs
"""
Usage:
  crypto_price BTC
  crypto_price ETH usd
"""

import json, urllib.request, urllib.parse, sys, re

# Map common symbols to CoinGecko IDs
coin_map = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "ltc": "litecoin",
    "doge": "dogecoin",
    "xrp": "ripple",
    "ada": "cardano",
    "sol": "solana",
    "dot": "polkadot",
    "bch": "bitcoin-cash",
    "link": "chainlink"
}

raw = (globals().get("input") or "").strip()
cmd = re.sub(r"(?i)^crypto_price\s+", "", raw).strip()
parts = cmd.split()

if not parts:
    result = "Usage: crypto_price SYMBOL [CURRENCY]"
else:
    symbol = parts[0].lower()
    vs     = parts[1].lower() if len(parts) > 1 else "usd"
    coin_id = coin_map.get(symbol, symbol)

    url = "https://api.coingecko.com/api/v3/simple/price?" + urllib.parse.urlencode({
        "ids": coin_id,
        "vs_currencies": vs
    })

    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read().decode())
        price = data.get(coin_id, {}).get(vs)
        if price is None:
            result = f"Price not found for {symbol.upper()} in {vs.upper()}"
        else:
            result = f"{symbol.upper()} = {price} {vs.upper()}"
    except Exception as e:
        result = f"❌ Failed to fetch price: {e}"
