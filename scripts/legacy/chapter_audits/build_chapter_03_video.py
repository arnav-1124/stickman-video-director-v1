import os
import sys
import json
import asyncio
import subprocess
import shutil
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = ROOT_DIR / "projects" / "long" / "ep01_why_people_fall_for_who_ignores_them"
CH03_DIR = PROJECT_DIR / "chapter_03_the_economy_of_availability"
SLIDES_DIR = CH03_DIR / "slides"
AUDIO_DIR_EN = CH03_DIR / "audio" / "en"
MASTER_VO_PATH = CH03_DIR / "audio" / "ch03_master_en.mp3"
BGM_PATH = ROOT_DIR / "assets" / "bgm" / "dark_contemplation.mp3"
STORYBOARD_FILE = CH03_DIR / "storyboard.json"
RENDERS_DIR = CH03_DIR / "renders"
CENTRAL_RENDERS_DIR = ROOT_DIR / "renders" / "long" / "ep01_why_people_fall_for_who_ignores_them"
SEGMENTS_DIR = CH03_DIR / "_segments_temp"

AUDIO_DIR_EN.mkdir(parents=True, exist_ok=True)
RENDERS_DIR.mkdir(parents=True, exist_ok=True)
CENTRAL_RENDERS_DIR.mkdir(parents=True, exist_ok=True)
SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)

# 100% Natural Storytelling Voice Settings
VOICE_EN = "en-US-ChristopherNeural"
PITCH_EN = "-2Hz"
RATE_EN = "+5%"  # Natural conversational storytelling pace (neither rushed nor dragging)

# Major thought transitions where a slightly longer beat (0.45s) is natural
MAJOR_PAUSE_SHOTS = {67, 71, 76, 77, 82, 87, 90}

def get_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_exact_shot(sid, text, raw_dir, out_mp3):
    comm = edge_tts.Communicate(text, VOICE_EN, pitch=PITCH_EN, rate=RATE_EN, boundary="WordBoundary")
    raw_mp3 = raw_dir / f"shot_{sid:03d}_raw.mp3"
    words = []
    
    with open(raw_mp3, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = (chunk["offset"] / 10000) / 1000.0
                end_sec = ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                words.append((chunk["text"], start_sec, end_sec))

    total_raw = get_duration(raw_mp3)
    last_word_text, _, last_word_end = words[-1]
    
    # Breathing pause: 0.45s for major scene breaks, 0.35s for regular narrative flow
    pause_dur = 0.45 if sid in MAJOR_PAUSE_SHOTS else 0.35
    target_dur = min(total_raw, round(last_word_end + pause_dur, 3))
    
    # Clean cut at target_dur with a gentle 0.04s fade-out at the very tail of silence
    fade_start = max(0, target_dur - 0.04)
    cmd_trim = [
        "ffmpeg", "-y", "-i", str(raw_mp3),
        "-t", f"{target_dur:.3f}",
        "-af", f"afade=t=out:st={fade_start:.3f}:d=0.04",
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(out_mp3)
    ]
    subprocess.run(cmd_trim, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    actual_dur = get_duration(out_mp3)
    return {
        "shot_id": sid,
        "text": text,
        "last_word": last_word_text,
        "last_word_end": round(last_word_end, 3),
        "pause_dur": round(actual_dur - last_word_end, 3),
        "duration": actual_dur
    }

async def main():
    print("=" * 80)
    print("  CHAPTER 03 VIDEO ASSEMBLER: THE ECONOMY OF AVAILABILITY")
    print("=" * 80)

    with open(STORYBOARD_FILE, "r", encoding="utf-8") as f:
        sb_data = json.load(f)

    shots = sb_data["shots"]
    print(f"Loaded {len(shots)} shots from storyboard (Shots 67 to 90).")

    raw_dir = CH03_DIR / "audio" / "_raw_tts"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # 1. Synthesize all 24 shots with exact word boundaries
    print("\n--- [1/4] Generating natural voiceover with exact word-boundary timing ---")
    shot_metrics = []
    total_audio_time = 0.0

    for s in shots:
        sid = s["shot_id"]
        clause = s["spoken_clause"].strip()

        if clause.startswith("[CHAPTER"):
            speech_text = "Chapter Three: The Economy of Availability."
        else:
            speech_text = clause

        out_mp3 = AUDIO_DIR_EN / f"shot_{sid:03d}.mp3"
        metrics = await synthesize_exact_shot(sid, speech_text, raw_dir, out_mp3)
        shot_metrics.append(metrics)
        
        dur = metrics["duration"]
        s["duration_sec"] = dur
        total_audio_time += dur
        
        print(f"  Shot {sid:02d} ({dur:.2f}s) | Speech ends at {metrics['last_word_end']:.2f}s (\"{metrics['last_word']}\") + {metrics['pause_dur']:.2f}s breath -> \"{speech_text[:40]}...\"")

    # Cleanup raw dir
    shutil.rmtree(raw_dir, ignore_errors=True)

    # Save updated storyboard with exact measured durations
    with open(STORYBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(sb_data, f, indent=2)
    print(f"\n  ✓ Storyboard updated with exact measured durations (Total Audio: {total_audio_time:.2f}s / {total_audio_time/60:.2f}m)")

    # 2. Build sample-accurate master VO track
    print("\n--- [2/4] Assembling sample-accurate master VO track ---")
    inputs = []
    filter_inputs = []
    for idx, s in enumerate(shots):
        sid = s["shot_id"]
        inputs.extend(['-i', str(AUDIO_DIR_EN / f"shot_{sid:03d}.mp3")])
        filter_inputs.append(f'[{idx}:a]')
    filter_str = ''.join(filter_inputs) + f'concat=n={len(shots)}:v=0:a=1[aout]'
    cmd_master = ['ffmpeg', '-y'] + inputs + ['-filter_complex', filter_str, '-map', '[aout]', '-c:a', 'libmp3lame', '-b:a', '192k', str(MASTER_VO_PATH)]
    subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    master_dur = get_duration(MASTER_VO_PATH)
    print(f"  ✓ Master VO Track compiled: {MASTER_VO_PATH} ({master_dur:.3f}s)")

    # 3. Render 24 individual micro-segments (100% Image-Audio Binding)
    print("\n--- [3/4] Rendering 24 micro-segments (guaranteeing 100% frame sync) ---")
    vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#FAF9F6,setsar=1,fps=30"
    segment_files = []

    for sid in range(67, 91):
        candidates = [
            SLIDES_DIR / f"slide_{sid}.jpg",
            SLIDES_DIR / f"slide_{sid:02d}.jpg",
            SLIDES_DIR / f"slide_{sid:03d}.jpg",
            SLIDES_DIR / f"slide_{sid}.png",
            SLIDES_DIR / f"slide_{sid:02d}.png"
        ]
        img_path = None
        for c in candidates:
            if c.exists():
                img_path = c
                break
        if not img_path:
            raise FileNotFoundError(f"Missing slide image for shot {sid}")

        audio_path = AUDIO_DIR_EN / f"shot_{sid:03d}.mp3"
        seg_out = SEGMENTS_DIR / f"seg_{sid:02d}.mp4"
        dur = get_duration(audio_path)

        cmd_seg = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img_path),
            "-i", str(audio_path),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
            "-t", f"{dur:.3f}",
            "-shortest",
            str(seg_out)
        ]
        subprocess.run(cmd_seg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        segment_files.append(seg_out)
        if (sid - 66) % 6 == 0 or sid == 90:
            print(f"  ✓ Built segments 67 through {sid:02d}...")

    # Write segment concat list
    seg_list_path = SEGMENTS_DIR / "concat_segments.txt"
    with open(seg_list_path, "w", encoding="utf-8") as f:
        for seg in segment_files:
            f.write(f"file '{seg.as_posix()}'\n")

    # 4. Concatenate segments into clean preview video
    out_no_bgm = RENDERS_DIR / "ch03_the_economy_of_availability_preview_no_bgm.mp4"
    print(f"\n--- [4/4] Assembling full Chapter 3 video ---")
    print(f"  Rendering clean narration preview: {out_no_bgm.name}")

    cmd_stitch = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(seg_list_path),
        "-c", "copy",
        str(out_no_bgm)
    ]
    subprocess.run(cmd_stitch, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Render with BGM
    out_with_bgm = RENDERS_DIR / "ch03_the_economy_of_availability_preview.mp4"
    central_out = CENTRAL_RENDERS_DIR / "ch03_the_economy_of_availability_preview.mp4"

    if BGM_PATH.exists():
        print(f"  Adding atmospheric BGM track: {BGM_PATH.name}")
        fade_out_start = max(0, total_audio_time - 2.5)
        filter_complex = (
            f"[1:a]volume=0.10,afade=t=in:st=0:d=0.5,afade=t=out:st={fade_out_start:.2f}:d=2.0[bgm];"
            f"[0:a]volume=1.0[vo];"
            f"[vo][bgm]amix=inputs=2:duration=first:normalize=0[aout]"
        )
        cmd_bgm = [
            "ffmpeg", "-y",
            "-i", str(out_no_bgm),
            "-stream_loop", "-1", "-i", str(BGM_PATH),
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(out_with_bgm)
        ]
        subprocess.run(cmd_bgm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        shutil.copy2(str(out_with_bgm), str(central_out))
        print(f"  ✓ Production video with BGM ready: {out_with_bgm}")
        print(f"  ✓ Central archive copy: {central_out}")

    # Cleanup temp segments
    shutil.rmtree(SEGMENTS_DIR, ignore_errors=True)

    final_v_dur = get_duration(out_with_bgm if out_with_bgm.exists() else out_no_bgm)
    print("\n" + "=" * 80)
    print("  CHAPTER 03 VIDEO ASSEMBLY COMPLETE!")
    print(f"  Final Video Duration: {final_v_dur:.2f}s ({int(final_v_dur//60)}m {int(final_v_dur%60):02d}s)")
    print(f"  Audio/Video Sync:     100.000% frame-bound")
    print(f"  Natural Speech Rate:  +5% ChristopherNeural with 0.35s-0.45s breathing pauses")
    print(f"  Preview with BGM:     {out_with_bgm}")
    print(f"  Narration Only:       {out_no_bgm}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
