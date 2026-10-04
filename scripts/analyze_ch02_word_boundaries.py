import json
import sys
import asyncio
from pathlib import Path
import edge_tts

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(".").resolve()
CH02_DIR = ROOT_DIR / "projects" / "long" / "ep01_why_people_fall_for_who_ignores_them" / "chapter_02_the_casino_effect"
STORYBOARD_FILE = CH02_DIR / "storyboard.json"

VOICE_EN = "en-US-ChristopherNeural"
PITCH_EN = "-2Hz"
RATE_EN = "+5%"

with open(STORYBOARD_FILE, "r", encoding="utf-8") as f:
    sb_data = json.load(f)

shots = sb_data["shots"]

async def analyze_words():
    for s in shots:
        sid = s["shot_id"]
        clause = s["spoken_clause"].strip()
        if clause.startswith("[CHAPTER"):
            clause = "Chapter Two: The Casino Effect. The Dopamine of Uncertainty."
            
        comm = edge_tts.Communicate(clause, VOICE_EN, pitch=PITCH_EN, rate=RATE_EN, boundary="WordBoundary")
        words = []
        async for chunk in comm.stream():
            if chunk["type"] == "WordBoundary":
                start_sec = (chunk["offset"] / 10000) / 1000.0
                end_sec = ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                words.append((chunk["text"], round(start_sec, 2), round(end_sec, 2)))
        
        first_w = words[0] if words else ("", 0, 0)
        last_w = words[-1] if words else ("", 0, 0)
        print(f"Shot {sid:02d} ({last_w[2]:.2f}s total): '{clause}'")
        # Print breakdown of sub-sentences if multiple sentences
        sentences = [sent.strip() for sent in clause.replace("?", "?|").replace(".", ".|").replace("!", "!|").split("|") if sent.strip()]
        if len(sentences) > 1:
            for sent in sentences:
                # find start and end of this sentence
                sent_words = sent.split()
                # find first word matching
                print(f"    Sub-sent: '{sent}'")

asyncio.run(analyze_words())
