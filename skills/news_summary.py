# skills/news_summary.py – Nova Jr skill to fetch and summarize tech news

import urllib.request
import xml.etree.ElementTree as ET
from llm_engine import summarize

def run():
    url = "https://feeds.bbci.co.uk/news/technology/rss.xml"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
    except Exception as e:
        return f"❌ News fetch failed: {e}"

    try:
        root = ET.fromstring(data)
        items = root.findall(".//item")
        headlines = [item.find("title").text for item in items[:5]]
        content = "\n".join(headlines)
        summary = summarize(f"Summarize today's tech headlines:\n{content}")
        return summary
    except Exception as e:
        return f"❌ News parse failed: {e}"
