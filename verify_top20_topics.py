import urllib.request
import urllib.parse
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

top20_titles = [
    "When Humans First Realized Tomorrow Exists",
    "Why Humans Are The Only Animal That Points",
    "How Ancient Humans Survived The First Broken Bone",
    "Why Humans Feel Second Hand Embarrassment Evolution",
    "How Ancient Humans Survived The First Solar Eclipse",
    "The Uncanny Valley Why Humans Fear Almost Human",
    "How Ancient Humans Named Each Other Before Language",
    "Why Ancient Humans Were Biologically Lazy",
    "Why Looking At The Sun Makes You Sneeze Evolution",
    "Why Humans Feel The Urge To Jump From High Places",
    "How Ancient Humans Discovered Plants Have Sex",
    "How Humans Accidentally Domesticated Themselves",
    "What Did Ancient Humans Do When Earthquakes Struck",
    "Why Humans Stare Into Blank Space When Thinking",
    "How Ancient Humans Made Maps Before Writing",
    "Why Humans Laugh When Terrified False Alarm",
    "How Ancient Humans Survived Frozen Water In Winter",
    "Why Epic Sounds Give Humans Goosebumps Frisson",
    "How Ancient Humans Settled Fights Without Murder",
    "Why Humans Fidget And Bite Nails When Stressed"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

results = []

for idx, q in enumerate(top20_titles, 1):
    encoded = urllib.parse.quote(q)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}', html)
        top = [t for t in titles if not t.startswith("YouTube") and len(t) > 5][:3]
        results.append({
            "idx": idx,
            "query": q,
            "top_youtube_hits": top
        })
    except Exception as e:
        results.append({"idx": idx, "query": q, "error": str(e)})

with open("scratch/top20_youtube_verified.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Top 20 verification complete!")
