import json
import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))
from pipeline.generate_subtitles import build_subtitles

shots_data = [
    {
        "shot_id": 1,
        "offset": 0.0,
        "text": "In every hallway, ten guys stare at her. She only notices the one who didn't.",
        "speech_start": 0.5,
        "speech_end": 7.2
    },
    {
        "shot_id": 2,
        "offset": 8.0,
        "text": "Most guys give away their attention for free. And free attention has zero value.",
        "speech_start": 0.4,
        "speech_end": 6.8
    },
    {
        "shot_id": 3,
        "offset": 16.0,
        "text": "The attractive man never chases. He exists in his own orbit, completely unbothered.",
        "speech_start": 0.4,
        "speech_end": 7.1
    },
    {
        "shot_id": 4,
        "offset": 24.0,
        "text": "When a woman is used to being worshipped, your silent indifference feels like an irresistible challenge.",
        "speech_start": 0.4,
        "speech_end": 7.2
    },
    {
        "shot_id": 5,
        "offset": 32.0,
        "text": "Because her brain demands answers: why isn't he looking, and what makes him so confident?",
        "speech_start": 0.4,
        "speech_end": 6.8
    },
    {
        "shot_id": 6,
        "offset": 40.0,
        "text": "Never exhaust yourself begging for validation. Hold your frame, and let natural curiosity do the work.",
        "speech_start": 0.4,
        "speech_end": 7.0
    }
]

all_words = []
for shot in shots_data:
    words = shot["text"].split()
    shot_offset = shot["offset"]
    s_start = shot_offset + shot["speech_start"]
    s_end = shot_offset + shot["speech_end"]
    dur = s_end - s_start
    step = dur / len(words)
    
    for idx, w in enumerate(words):
        w_clean = w.strip(".,:;-\"\'?!")
        all_words.append({
            "word": w_clean,
            "start_sec": round(s_start + (idx * step), 2),
            "end_sec": round(s_start + ((idx + 1) * step), 2)
        })

project_dir = Path("projects/ep03_the_hallway_rule")
words_path = project_dir / "audio" / "word_timestamps.json"
words_path.parent.mkdir(parents=True, exist_ok=True)

with open(words_path, "w", encoding="utf-8") as f:
    json.dump(all_words, f, indent=2)

print(f"Generated {len(all_words)} word timestamps in {words_path}")

# Generate kinetic ASS subtitles
ass_file = build_subtitles(str(project_dir), aspect="9:16")
print(f"Generated ASS subtitles at: {ass_file}")
