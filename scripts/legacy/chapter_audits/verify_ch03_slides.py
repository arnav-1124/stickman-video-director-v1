import os
import json
from PIL import Image
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CH03_DIR = ROOT_DIR / "projects" / "long" / "ep01_why_people_fall_for_who_ignores_them" / "chapter_03_the_economy_of_availability"
SLIDES_DIR = CH03_DIR / "slides"
SB_PATH = CH03_DIR / "storyboard.json"

with open(SB_PATH, "r", encoding="utf-8") as f:
    sb = json.load(f)

shots = sb["shots"]
print(f"Total Shots in Storyboard: {len(shots)}")
print("=" * 80)

all_valid = True
results = []

for s in shots:
    sid = s["shot_id"]
    candidates = [
        SLIDES_DIR / f"slide_{sid}.jpg",
        SLIDES_DIR / f"slide_{sid:02d}.jpg",
        SLIDES_DIR / f"slide_{sid:03d}.jpg",
        SLIDES_DIR / f"slide_{sid}.png",
        SLIDES_DIR / f"slide_{sid:02d}.png"
    ]
    slide_file = None
    for c in candidates:
        if c.exists():
            slide_file = c
            break
            
    if not slide_file:
        print(f"Shot {sid:02d}: MISSING SLIDE!")
        all_valid = False
        continue
        
    try:
        with Image.open(slide_file) as img:
            w, h = img.size
            ratio = w / h
            is_16_9 = abs(ratio - (16 / 9)) < 0.02
            size_kb = slide_file.stat().st_size / 1024
            status = "VALID (16:9)" if is_16_9 else f"INVALID RATIO ({ratio:.2f})"
            if not is_16_9:
                all_valid = False
            results.append((sid, slide_file.name, w, h, ratio, size_kb, status, s["title"], s["spoken_clause"]))
            print(f"Shot {sid:02d} | {slide_file.name:14} | {w}x{h} ({status}) | {size_kb:6.1f} KB | {s['title']}")
    except Exception as e:
        print(f"Shot {sid:02d} | ERROR OPENING {slide_file.name}: {e}")
        all_valid = False

print("=" * 80)
print(f"All 24 slides present and technically fit: {all_valid}")
