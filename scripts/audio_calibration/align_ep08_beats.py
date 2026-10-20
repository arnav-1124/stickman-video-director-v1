import json
from pathlib import Path

PROJECT_DIR = Path("projects/sticky_in_dark/shorts/ep08_the_toothbrush_protocol")
SCRIPT_FILE = PROJECT_DIR / "script.txt"
WORDS_FILE = PROJECT_DIR / "audio/word_timestamps.json"

with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

with open(WORDS_FILE, "r", encoding="utf-8") as f:
    words = json.load(f)

word_idx = 0
beats = []

for line_idx, line in enumerate(lines, 1):
    tokens = line.split()
    n_tokens = len(tokens)
    
    start_w = words[word_idx]
    end_w = words[word_idx + n_tokens - 1]
    
    start_sec = start_w["start_sec"]
    end_sec = end_w["end_sec"]
    
    beats.append({
        "beat_id": line_idx,
        "line": line,
        "first_word": start_w["word"],
        "last_word": end_w["word"],
        "start_sec": start_sec,
        "end_sec": end_sec,
        "duration": round(end_sec - start_sec, 2),
        "word_range": [word_idx, word_idx + n_tokens - 1]
    })
    
    word_idx += n_tokens

print(json.dumps(beats, indent=2))

with open(PROJECT_DIR / "audio/calibrated_beats_timing.json", "w", encoding="utf-8") as f:
    json.dump(beats, f, indent=2)
