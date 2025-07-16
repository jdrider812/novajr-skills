import urllib.request, json, textwrap, llm_engine

TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"
COUNT = 5
SYSTEM = "Summarize these Hacker News titles in 3 crisp sentences."

try:
    ids = json.loads(urllib.request.urlopen(TOP, timeout=5).read())
    titles = []
    for i in ids[:COUNT]:
        data = json.loads(urllib.request.urlopen(ITEM.format(i), timeout=5).read())
        titles.append(data.get("title", ""))
    bullets = "\n".join(f"- {t}" for t in titles)
    tldr = llm_engine.ask(bullets, system_prompt=SYSTEM)
    result = textwrap.dedent(f"📰 **Top Hacker News**\n{bullets}\n\n**TL;DR:** {tldr}")
except Exception as e:
    result = f"❌ HN fetch failed: {e}"
