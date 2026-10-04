import json
from pathlib import Path

sb_file = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_02_the_casino_effect/storyboard.json")
with open(sb_file, encoding="utf-8") as f:
    sb = json.load(f)

slides_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_02_the_casino_effect/slides")
print(f"Total shots defined in Chapter 2: {len(sb['shots'])}")

missing = []
for s in sb["shots"]:
    sid = s["shot_id"]
    candidates = [
        slides_dir / f"slide_{sid}.jpg",
        slides_dir / f"slide_{sid}.png",
        slides_dir / f"slide_{sid:02d}.jpg",
        slides_dir / f"slide_{sid:03d}.jpg",
        slides_dir / f"slide_{sid:02d}.png",
        slides_dir / f"slide_{sid:03d}.png"
    ]
    found = None
    for c in candidates:
        if c.exists():
            found = c
            break
            
    if found:
        print(f"Shot {sid:02d}: [FOUND] -> {found.name} ({found.stat().st_size} bytes)")
    else:
        print(f"Shot {sid:02d}: [MISSING!] - {s['title']} | \"{s['spoken_clause']}\"")
        missing.append(sid)

print("\n" + "="*50)
if missing:
    print(f"MISSING SHOTS: {missing}")
else:
    print("ALL SHOTS PRESENT!")
