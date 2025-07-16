import urllib.parse, urllib.request, re, html

query = (globals().get("input") or "").split(None, 1)[1:]
if not query:
    result = "Usage: search_youtube <keywords>"
else:
    q = urllib.parse.quote_plus(query[0])
    url = f"https://ytsearch.com/search?q={q}"
    try:
        page = urllib.request.urlopen(url, timeout=5).read().decode()
        titles = re.findall(r'"title":"(.*?)"', page)[:5]
        titles = [html.unescape(t) for t in titles]
        result = "🎬 Top YouTube results:\n" + "\n".join(f"- {t}" for t in titles)
    except Exception as e:
        result = f"❌ YouTube search failed: {e}"
