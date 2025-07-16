# web_search.py – DuckDuckGo Instant‑Answer search (full coverage)
import urllib.parse, urllib.request, json, re

# ---------- helpers ----------
def fetch(query: str) -> dict:
    url = "https://api.duckduckgo.com/?" + urllib.parse.urlencode({
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1,
        "skip_disambig": 1,
    })
    with urllib.request.urlopen(url, timeout=5) as resp:
        return json.loads(resp.read().decode())

def first_related(topics):
    for item in topics:
        if isinstance(item, dict):
            if "Text" in item:
                return item["Text"]
            if "Topics" in item:
                sub = first_related(item["Topics"])
                if sub:
                    return sub
    return None

# ---------- main ----------
raw = (globals().get("input") or "").strip()

if not raw or raw.lower() == "web_search":
    result = "Please say something like: web_search python programming"
else:
    query = re.sub(r"(?i)^web_search\s+", "", raw).strip()
    try:
        data = fetch(query)

        # 1) Abstract
        msg = data.get("AbstractText") or ""

        # 2) Results list
        if not msg and data.get("Results"):
            first = data["Results"][0]
            if "Text" in first:
                msg = first["Text"]

        # 3) Answer field (plain string)
        if not msg and data.get("Answer"):
            msg = str(data["Answer"])

        # 4) RelatedTopics recursion
        if not msg:
            msg = first_related(data.get("RelatedTopics", [])) or ""

        result = msg.strip() if msg else "No results found."
    except Exception as e:
        result = f"❌ Search failed: {e}"
