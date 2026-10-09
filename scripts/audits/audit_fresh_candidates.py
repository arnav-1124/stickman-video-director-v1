import urllib.request
import urllib.parse
import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

new_candidates = [
    # 1. Uncanny valley origin
    "Why Humans Are Terrified Of Things That Look Almost Human",
    # 2. Hypnic jerk / tree falling
    "Why You Feel Like Falling In Your Sleep Evolution",
    # 3. White sclera / cooperative eye
    "Why Humans Have White In Their Eyes Evolution",
    # 4. Grandmother hypothesis
    "Why Humans Evolved Grandmothers",
    # 5. Photic sneeze reflex / cave soot
    "Why Looking At The Sun Makes You Sneeze Evolution",
    # 6. Sympathetic vomiting / disgust mirror
    "Why Seeing Someone Vomit Makes You Vomit Evolution",
    # 7. Throwing rocks superpower
    "Why Humans Are The Only Animal That Can Throw Accurately",
    # 8. Mental time travel / Tomorrow
    "When Humans First Realized Tomorrow Exists",
    # 9. Campfire trance / Fire gazing
    "Why Staring Into Fire Makes Humans Relax",
    # 10. Human chin mystery
    "Why Humans Are The Only Animal With A Chin",
    # 11. Kindchenschema / baby cute trap
    "Why Human Babies Are Born Completely Helpless",
    # 12. Piloerection / Goosebumps
    "Why Humans Get Goosebumps When Scared",
    # 13. Screaming roughness / Primal scream
    "Why Human Screams Sound So Terrifying",
    # 14. Beards cushioning punches
    "Why Men Evolved Beards Evolution Punch",
    # 15. Spicy food / capsaicin masochism
    "Why Humans Are The Only Animal That Eats Spicy Food",
    # 16. Seasonal depression as winter torpor
    "Why Humans Get Depressed In Winter Evolution",
    # 17. The first debt ledger before money
    "How Humans Traded Before Money Or Barter",
    # 18. Fidgeting and displacement grooming
    "Why Humans Fidget When Stressed Evolution",
    # 19. Synchronized stomping / Rhythm as defense
    "How Ancient Humans Used Rhythm To Scare Predators",
    # 20. Finger pointing and shared attention
    "Why Pointing Is A Human Superpower",
    # 21. How Ancient Humans Invented Names
    "How Did Ancient Humans Invent Names",
    # 22. Ostracism as tribal death penalty
    "Why Being Ignored Was A Death Sentence Ancient Humans"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"Auditing {len(new_candidates)} fresh candidates against YouTube...\n")

audit_results = []

for idx, q in enumerate(new_candidates, 1):
    encoded = urllib.parse.quote(q)
    url = f"https://www.youtube.com/results?search_query={encoded}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        
        titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}', html)
        top_titles = [t for t in titles if not t.startswith("YouTube") and len(t) > 5][:4]
        
        audit_results.append({
            "candidate": q,
            "top_titles": top_titles
        })
        print(f"[{idx:02d}] Checked: {q}")
        for t in top_titles[:2]:
            print(f"     -> {t}")
    except Exception as e:
        print(f"[{idx:02d}] Error checking '{q}': {e}")

with open("scratch/fresh_candidates_audit.json", "w", encoding="utf-8") as f:
    json.dump(audit_results, f, indent=2, ensure_ascii=False)

print("\nFresh Audit Complete!")
