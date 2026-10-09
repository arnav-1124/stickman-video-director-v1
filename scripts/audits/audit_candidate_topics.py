import urllib.request
import urllib.parse
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

candidates = [
    # 1. Pointing / Shared Attention
    "Why Humans Are The Only Animal That Points",
    # 2. Dental straightness paradox
    "Why Ancient Humans Had Perfectly Straight Teeth",
    # 3. Blushing / Guilt
    "Why Humans Are The Only Animal That Blushes",
    # 4. Laughter as False Alarm
    "Why Humans Laugh When Scared",
    # 5. Gossip as Vocal Grooming
    "Why Humans Invented Gossip",
    # 6. Kissing Origin
    "Why Did Ancient Humans Start Kissing",
    # 7. Singing before speech
    "Did Humans Sing Before They Could Talk",
    # 8. Salt Discovery & Addiction
    "How Ancient Humans Discovered Salt",
    # 9. Handshake & Touching palms
    "How Ancient Humans Invented The Handshake",
    # 10. Nail & Hair cutting
    "How Ancient Humans Cut Their Nails",
    # 11. Surviving Midday Heat / Sweating
    "Why Humans Lost Their Fur To Sweat",
    # 12. First Funeral / Birth of Ghosts
    "How Ancient Humans Invented Funerals",
    # 13. Poisonous Plant Testing
    "How Ancient Humans Knew What Plants Were Poisonous",
    # 14. Superstitions & Lucky Charms
    "How Humans Invented Superstition",
    # 15. Toothache & Ancient Dentistry
    "What Did Ancient Humans Do For Toothaches",
    # 16. Wayfinding & Getting Lost
    "How Ancient Humans Navigated Before Maps",
    # 17. Silent Barter / First Trade
    "What Happened When Ancient Tribes Met",
    # 18. Embarrassing Memories / Cringing
    "Why We Cringe At Old Memories Evolution",
    # 19. Why Humans Weep Emotional Tears
    "Why Humans Cry Emotional Tears",
    # 20. Biphasic Sleep / Two Sleeps
    "Why Ancient Humans Slept Twice A Night",
    # 21. How Ancient Humans Kept Meat Cold / Preserved
    "How Ancient Humans Preserved Food Before Refrigerators",
    # 22. Ancient Fire vs Sparks
    "How Ancient Humans Made Fire Without Matches"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"Auditing {len(candidates)} topic candidates against YouTube...\n")

results = []

for idx, q in enumerate(candidates, 1):
    encoded = urllib.parse.quote(q)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        
        # Extract top 3 video titles
        titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}', html)
        top_titles = [t for t in titles if not t.startswith("YouTube") and len(t) > 5][:5]
        
        # Check if benchmark channel or near-identical animated title appears
        is_exact_match = any(q.lower() in t.lower() for t in top_titles)
        
        results.append({
            "query": q,
            "top_titles": top_titles[:3],
            "exact_match": is_exact_match
        })
        print(f"[{idx:02d}] Checked: {q}")
        for t in top_titles[:2]:
            print(f"     -> {t}")
    except Exception as e:
        print(f"[{idx:02d}] Error checking '{q}': {e}")

with open("scratch/topic_uniqueness_audit.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nAudit Complete! Saved to scratch/topic_uniqueness_audit.json")
