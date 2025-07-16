import urllib.request, json, os

CITY = "New York"   # change to your city

try:
    url = f"https://wttr.in/{CITY}?format=j1"
    data = json.loads(urllib.request.urlopen(url, timeout=5).read())
    current = data["current_condition"][0]
    temp_c  = current["temp_C"]
    feels   = current["FeelsLikeC"]
    cond    = current["weatherDesc"][0]["value"]
    result  = f"🌤  {CITY}: {temp_c} °C, feels {feels} °C – {cond}"
except Exception as e:
    result = f"❌ Weather fetch failed: {e}"
