import urllib.request
import urllib.parse
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

inspect_queries = [
    "SketchWise When Did Humans First Fall In Love",
    "StickTale How Did HUMANS Invent Attraction",
    "The Mind Relic How Did Humans First Figure Out Where Babies Come From"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

results = []

for q in inspect_queries:
    encoded = urllib.parse.quote(q)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        
        # Extract title, channel, length, viewcount
        titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}', html)
        views = re.findall(r'"viewCountText":\{"simpleText":"([^"]+)"\}', html)
        lengths = re.findall(r'"lengthText":\{"simpleText":"([^"]+)"\}', html)
        
        print(f"Query: {q}")
        for i in range(min(3, len(titles))):
            t = titles[i]
            v = views[i] if i < len(views) else "N/A"
            l = lengths[i] if i < len(lengths) else "N/A"
            print(f"  -> Title: {t} | Length: {l} | Views: {v}")
    except Exception as e:
        print(f"Error {q}: {e}")

print("Done inspection!")
