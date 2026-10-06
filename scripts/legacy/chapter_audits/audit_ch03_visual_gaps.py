import sys
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
CH03_DIR = ROOT / "projects" / "long" / "ep01_why_people_fall_for_who_ignores_them" / "chapter_03_the_economy_of_availability"
SCRIPT_PATH = CH03_DIR / "script.txt"
SB_PATH = CH03_DIR / "storyboard.json"

with open("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_03_the_economy_of_availability/script.txt", "r", encoding="utf-8") as f:
    script_lines = [l.strip() for l in f if l.strip()]

with open("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_03_the_economy_of_availability/storyboard.json", "r", encoding="utf-8") as f:
    sb = json.load(f)

shots = sb["shots"]
print(f"Total script lines: {len(script_lines)}")
print(f"Total storyboard shots: {len(shots)}")
print("=" * 80)

for s in shots:
    sid = s["shot_id"]
    dur = s.get("duration_sec", 0)
    clause = s.get("spoken_clause", "")
    title = s.get("title", "")
    print(f"Shot {sid:02d} [{dur:.2f}s]: \"{clause}\"")

