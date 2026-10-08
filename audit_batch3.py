import urllib.request
import urllib.parse
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

candidates_batch3 = [
    "Why Humans Are The Only Animal That Chokes On Food Evolution",
    "Why Humans Have Eyebrows Evolution Nonverbal",
    "Why Contagious Yawning Exists Evolution Tribal",
    "Why Humans Have Different Blood Types Evolution Plague",
    "How Ancient Humans Invented The First Knot String Revolution",
    "Why Children Hate Vegetables Bitter Taste Stone Age",
    "Why Humans Walk In Circles When Lost Evolution",
    "Why 90% Of Humans Are Right Handed Evolution",
    "How Ancient Humans Captured Lightning Fire",
    "Why Humans Swing Their Arms When Walking Evolution",
    "Why Cold Drinks Cause Brain Freeze Evolution",
    "Why Humans Clench Teeth When Lifting Heavy",
    "How Rabies Created Werewolf Myths Ancient Humans",
    "Why Humans Count In Tens Instead Of Twelves",
    "How Ancient Humans Discovered Antidotes Snake Bites"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

results = []

for idx, q in enumerate(candidates_batch3, 1):
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
            "top": top
        })
    except Exception as e:
        results.append({"idx": idx, "query": q, "error": str(e)})

with open("scratch/batch3_audit.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Batch 3 complete!")
