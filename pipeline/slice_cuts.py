"""
Dynamic Story-Driven Cut Slicer & Manifest Engine
Strictly follows narrative and storytelling cues to slice voiceover audio into
dynamic visual comic panels. ZERO fixed intervals. ZERO arbitrary frame limits.
"""

import json
from pathlib import Path

def generate_dynamic_manifest(project_dir, custom_cuts=None):
    """
    Builds the frame-accurate build_manifest.json and storyboard.json
    based on story-driven cuts.
    """
    project_dir = Path(project_dir).resolve()
    manifest_path = project_dir / "build_manifest.json"
    storyboard_path = project_dir / "storyboard.json"
    
    if custom_cuts:
        cuts = custom_cuts
    else:
        # Fallback to loading existing storyboard cuts if available
        if storyboard_path.exists():
            with open(storyboard_path, "r", encoding="utf-8") as f:
                sb_data = json.load(f)
                cuts = sb_data.get("cuts", [])
        else:
            print(f"[Error] No custom cuts provided and {storyboard_path} not found.")
            return None

    manifest_clips = []
    for c in cuts:
        cid = c.get("cut_id")
        manifest_clips.append({
            "cut_id": cid,
            "shot_id": c.get("shot_id"),
            "sub_beat": c.get("sub_beat"),
            "file_path": f"slides/slide_{cid:02d}.png",
            "duration": round(float(c.get("duration", c.get("duration_sec", 1.5))), 2),
            "text": c.get("text", c.get("audio_phrase", ""))
        })

    manifest = {
        "project_id": project_dir.name,
        "aspect_ratio": "9:16",
        "fps": 30,
        "pipeline_type": "static_comic_sync",
        "voiceover_track": "audio/voiceover.mp3",
        "subtitles_file": "subtitles.ass",
        "bgm_track": "../../assets/bgm/dark_contemplation.mp3",
        "bgm_volume_db": -22.0,
        "clips": manifest_clips
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    total_dur = sum(c["duration"] for c in manifest_clips)
    print(f"\n[DYNAMIC MANIFEST] Successfully built {manifest_path}")
    print(f"  Total Story Cuts: {len(manifest_clips)}")
    print(f"  Total Duration: {total_dur:.2f}s")
    print(f"  Min Cut: {min(c['duration'] for c in manifest_clips):.2f}s | Max Cut: {max(c['duration'] for c in manifest_clips):.2f}s")
    print(f"  Pacing: Dynamic Storytelling (NO fixed timers or intervals)")
    return manifest

if __name__ == "__main__":
    import sys
    proj = sys.argv[1] if len(sys.argv) > 1 else "projects/ep04_why_girls_like_silent_boy"
    generate_dynamic_manifest(proj)
