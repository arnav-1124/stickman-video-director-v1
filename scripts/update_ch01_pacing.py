import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = ROOT_DIR / "projects" / "long" / "ep01_why_people_fall_for_who_ignores_them"
CH01_DIR = PROJECT_DIR / "chapter_01_the_pedestal_paradox"
AUDIO_DIR_EN = CH01_DIR / "audio" / "en"
MASTER_VO_PATH = CH01_DIR / "audio" / "ch01_master_en.mp3"
STORYBOARD_FILE = CH01_DIR / "storyboard.json"

# Production Voice Settings: Dynamic Storytelling Cadence
VOICE_EN = "en-US-ChristopherNeural"
PITCH_EN = "-2Hz"
RATE_EN = "+14%"  # Tested sweet spot: brisk, confident, natural cadence

def get_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_and_trim(text, raw_path, final_path):
    comm = edge_tts.Communicate(text, VOICE_EN, pitch=PITCH_EN, rate=RATE_EN)
    await comm.save(str(raw_path))
    
    # Trim excessive trailing silence from Edge-TTS while leaving 0.16s breath cushion
    cmd_trim = [
        "ffmpeg", "-y", "-i", str(raw_path),
        "-af", "areverse,silenceremove=start_periods=1:start_duration=0.1:start_threshold=-35dB,areverse,apad=pad_dur=0.16",
        str(final_path)
    ]
    subprocess.run(cmd_trim, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Remove temp raw file
    if raw_path.exists():
        raw_path.unlink()

async def main():
    print("=" * 70)
    print(f"  UPDATING CHAPTER 01 PACING & NARRATION (Target Rate: {RATE_EN})")
    print("=" * 70)

    with open(STORYBOARD_FILE, "r", encoding="utf-8") as f:
        sb_data = json.load(f)

    shots = sb_data["shots"]
    print(f"Loaded {len(shots)} shots from storyboard.")

    temp_raw_dir = CH01_DIR / "audio" / "_raw_temp"
    temp_raw_dir.mkdir(parents=True, exist_ok=True)

    concat_shots_list = []
    total_new_dur = 0.0

    print("\n--- [1/3] Re-synthesizing all 36 shots with dynamic cadence ---")
    for s in shots:
        shot_id = s["shot_id"]
        clause = s["spoken_clause"].strip()

        if clause.startswith("[CHAPTER"):
            speech_text = "Chapter One: The Pedestal Paradox."
        else:
            speech_text = clause

        raw_mp3 = temp_raw_dir / f"shot_{shot_id:03d}_raw.mp3"
        final_mp3 = AUDIO_DIR_EN / f"shot_{shot_id:03d}.mp3"

        await synthesize_and_trim(speech_text, raw_mp3, final_mp3)
        dur = get_duration(final_mp3)
        s["duration_sec"] = round(dur, 3)
        total_new_dur += dur
        concat_shots_list.append(f"file 'en/{final_mp3.name}'")
        print(f"  Shot {shot_id:02d} ({dur:.2f}s): {speech_text[:45]}...")

    # Cleanup temp dir
    try:
        temp_raw_dir.rmdir()
    except Exception:
        pass

    # Save updated storyboard
    with open(STORYBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(sb_data, f, indent=2)
    print(f"\n  ✓ Storyboard updated with new measured shot durations.")

    # 2. Concat all shots into master VO track
    print("\n--- [2/3] Building new master VO track (ch01_master_en.mp3) ---")
    concat_txt_file = CH01_DIR / "audio" / "_concat_shots.txt"
    with open(concat_txt_file, "w", encoding="utf-8") as f:
        for line in concat_shots_list:
            f.write(line + "\n")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt_file),
        "-c", "copy",
        str(MASTER_VO_PATH)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if concat_txt_file.exists():
        concat_txt_file.unlink()

    master_dur = get_duration(MASTER_VO_PATH)
    print(f"  ✓ Master VO Track compiled: {MASTER_VO_PATH}")
    print(f"  ✓ Old Total Duration: 177.12s (2m 57s)")
    print(f"  ✓ New Total Duration: {master_dur:.2f}s ({int(master_dur//60)}m {int(master_dur%60):02d}s)")
    print(f"  ✓ Net Time Saved:     {177.12 - master_dur:.2f}s of sluggish dead air removed!")

    print("\n--- [3/3] Ready for video assembly ---")

if __name__ == "__main__":
    asyncio.run(main())
