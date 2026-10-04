import json
import subprocess
from pathlib import Path

sb_file = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/storyboard.json")
with open(sb_file, "r", encoding="utf-8") as f:
    data = json.load(f)

shots = data["shots"]
print("=" * 80)
print(f"{'Shot':<6} | {'Dur (s)':<8} | {'Words':<6} | {'WPM':<6} | Spoken Clause")
print("=" * 80)

total_words = 0
total_dur = 0.0

for s in shots:
    sid = s["shot_id"]
    clause = s["spoken_clause"].strip()
    if clause.startswith("[CHAPTER"):
        text = "Chapter One: The Pedestal Paradox."
    else:
        text = clause
    mp3 = Path(f"projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/audio/en/shot_{sid:03d}.mp3")
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(mp3)]
    dur = float(subprocess.check_output(cmd).decode().strip())
    words = len(text.split())
    wpm = (words / dur) * 60 if dur > 0 else 0
    total_words += words
    total_dur += dur
    print(f"#{sid:<4} | {dur:<8.2f} | {words:<6} | {wpm:<6.1f} | {text}")

print("=" * 80)
print(f"TOTALS: {len(shots)} shots | {total_dur:.2f}s ({total_dur/60:.2f} min) | {total_words} words | Overall WPM: {(total_words/total_dur)*60:.1f}")
