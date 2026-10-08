import urllib.request
import urllib.parse
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

attraction_queries = [
    "How Humans First Fell In Love Evolution",
    "Why Humans Evolved Romantic Attraction",
    "How Did Early Humans Pick A Mate",
    "How The First Humans Fell In Love",
    "The Evolution of Human Attraction",
    "Why Humans Fall In Love Instead Of Just Mating"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

results = []

for idx, q in enumerate(attraction_queries, 1):
    encoded = urllib.parse.quote(q)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}', html)
        top = [t for t in titles if not t.startswith("YouTube") and len(t) > 5][:4]
        results.append({
            "idx": idx,
            "query": q,
            "top": top
        })
        print(f"[{idx}] {q}")
        for t in top[:2]:
            print(f"   -> {t}")
    except Exception as e:
        results.append({"idx": idx, "query": q, "error": str(e)})

with open("scratch/attraction_audit.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nAttraction Audit complete!")
