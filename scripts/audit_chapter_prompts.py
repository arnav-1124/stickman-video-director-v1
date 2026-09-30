import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

sb_path = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/storyboard.json")
with open(sb_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for s in data["shots"][:18]:
    sid = s["shot_id"]
    title = s["title"]
    stype = s["scene_type"]
    voice = s.get("spoken_clause", "")
    comp = s.get("visual_composition_16_9", "").replace("\n", " ").strip()
    accent = s.get("color_accent", "")
    print(f"[{sid:03d}] {title} ({stype})")
    print(f"  VO: {voice}")
    print(f"  COMP: {comp}")
    print(f"  ACCENT: {accent}")
    print("-" * 50)
