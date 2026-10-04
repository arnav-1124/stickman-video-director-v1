import json
from pathlib import Path

PROJECT_DIR = Path("projects/shorts/ep05_how_to_handle_disrespect")
STORYBOARD_FILE = PROJECT_DIR / "storyboard.json"

with open(STORYBOARD_FILE, "r", encoding="utf-8") as f:
    storyboard = json.load(f)

cuts = storyboard["cuts"]

clips = []
concat_lines = []

for cut in cuts:
    cut_id = cut["cut_id"]
    dur = cut["duration"]
    text = cut["text"]
    slide_file = f"slides/slide_{cut_id:02d}.png"
    
    clips.append({
        "cut_id": cut_id,
        "beat_id": cut.get("beat_id", cut_id),
        "sub_beat": cut.get("sub_beat", "a"),
        "file_path": slide_file,
        "duration": dur,
        "text": text
    })
    
    concat_lines.append(f"file '{slide_file}'")
    concat_lines.append(f"duration {dur:.3f}")

# ffmpeg concat demuxer requirement: repeat the last file entry without duration
if clips:
    concat_lines.append(f"file '{clips[-1]['file_path']}'")

build_manifest = {
    "project_id": storyboard["project_id"],
    "aspect_ratio": storyboard["format"],
    "fps": 30,
    "pipeline_type": "static_comic_sync",
    "voiceover_track": "audio/voiceover.mp3",
    "subtitles_file": "subtitles.ass",
    "bgm_track": "../../assets/bgm/dark_contemplation.mp3",
    "bgm_volume_db": -22.0,
    "total_cuts": len(clips),
    "total_duration": round(sum(c["duration"] for c in clips), 3),
    "clips": clips
}

with open(PROJECT_DIR / "build_manifest.json", "w", encoding="utf-8") as f:
    json.dump(build_manifest, f, indent=2)

with open(PROJECT_DIR / "concat_en_23.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(concat_lines) + "\n")

print(f"Created build_manifest.json with {len(clips)} cuts ({build_manifest['total_duration']}s)")
print(f"Created concat_en_23.txt")
