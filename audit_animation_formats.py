import urllib.request
import urllib.parse
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

queries = [
    ("Topic_A_Babies", "How Did Early Humans Figure Out Where Babies Come From"),
    ("Topic_A_Babies_Anim", "How Did Ancient Humans Discover Reproduction animation"),
    ("Topic_B_Love", "How Humans First Fell In Love"),
    ("Topic_B_Love_Anim", "Why Humans Evolved Romantic Attraction animation")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

audit_summary = []

for tag, q in queries:
    encoded = urllib.parse.quote(q)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        
        # Extract all video chunks
        # Find all title runs and channel names
        raw_titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}', html)
        clean_titles = [t for t in raw_titles if not t.startswith("YouTube") and len(t) > 5][:8]
        
        # Check channel owners
        raw_channels = re.findall(r'"ownerText":\{"runs":\[\{"text":"([^"]+)"', html)
        if not raw_channels:
            raw_channels = re.findall(r'"longBylineText":\{"runs":\[\{"text":"([^"]+)"', html)
            
        items = []
        for i in range(min(len(clean_titles), 6)):
            ch = raw_channels[i] if i < len(raw_channels) else "Unknown"
            items.append({
                "title": clean_titles[i],
                "channel": ch
            })
            
        audit_summary.append({
            "tag": tag,
            "query": q,
            "top_hits": items
        })
        print(f"=== {tag} ===")
        for it in items[:4]:
            print(f"  - [{it['channel']}] {it['title']}")
    except Exception as e:
        print(f"Error {tag}: {e}")

with open("scratch/animation_format_audit.json", "w", encoding="utf-8") as f:
    json.dump(audit_summary, f, indent=2, ensure_ascii=False)

print("\nDone parsing!")
