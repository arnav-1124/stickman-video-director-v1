import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = ROOT_DIR / "projects" / "long" / "ep01_why_people_fall_for_who_ignores_them"
CH1_DIR = PROJECT_DIR / "chapter_01_the_pedestal_paradox"
SLIDES_DIR = CH1_DIR / "slides"
AUDIO_DIR_EN = CH1_DIR / "audio" / "en"
MASTER_VO_PATH = CH1_DIR / "audio" / "ch01_master_en.mp3"
BGM_PATH = ROOT_DIR / "assets" / "bgm" / "dark_contemplation.mp3"
RENDERS_DIR = CH1_DIR / "renders"
CENTRAL_RENDERS_DIR = ROOT_DIR / "renders" / "long" / "ep01_why_people_fall_for_who_ignores_them"
SEGMENTS_DIR = CH1_DIR / "_segments_temp"

RENDERS_DIR.mkdir(parents=True, exist_ok=True)
CENTRAL_RENDERS_DIR.mkdir(parents=True, exist_ok=True)
SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)

def get_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def main():
    print("=" * 60)
    print("  CHAPTER 01 VIDEO ASSEMBLER: THE PEDESTAL PARADOX")
    print("=" * 60)

    # 1. Verify all 36 slides and get individual audio durations
    slide_durations = []
    print("\n--- [1/4] Verifying slides and exact audio durations ---")
    for i in range(1, 37):
        img_name = f"slide_{i:02d}.jpg"
        img_path = SLIDES_DIR / img_name
        if not img_path.exists():
            alt = SLIDES_DIR / f"slide_{i:03d}.png"
            if alt.exists():
                img_path = alt
                img_name = alt.name
            else:
                raise FileNotFoundError(f"Missing slide image: {img_path}")

        audio_name = f"shot_{i:03d}.mp3"
        audio_path = AUDIO_DIR_EN / audio_name
        if not audio_path.exists():
            raise FileNotFoundError(f"Missing audio shot: {audio_path}")

        dur = get_duration(audio_path)
        slide_durations.append((img_name, dur))
        print(f"  Slide {i:02d} -> {img_name} ({dur:.3f}s)")

    total_audio_dur = sum(d for _, d in slide_durations)

    # 2. Assembling sample-accurate master VO track
    print("\n--- [2/4] Assembling sample-accurate master VO track ---")
    inputs = []
    filter_inputs = []
    for i in range(1, 37):
        inputs.extend(['-i', str(AUDIO_DIR_EN / f"shot_{i:03d}.mp3")])
        filter_inputs.append(f'[{i-1}:a]')
    filter_str = ''.join(filter_inputs) + f'concat=n=36:v=0:a=1[aout]'
    cmd_master = ['ffmpeg', '-y'] + inputs + ['-filter_complex', filter_str, '-map', '[aout]', '-c:a', 'libmp3lame', '-b:a', '192k', str(MASTER_VO_PATH)]
    subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    master_vo_dur = get_duration(MASTER_VO_PATH)
    print(f"  ✓ Total Shots Duration: {total_audio_dur:.3f}s")
    print(f"  ✓ Master VO Duration:   {master_vo_dur:.3f}s (Sync Drift: {abs(total_audio_dur - master_vo_dur)*1000:.1f}ms)")

    # 3. Render 36 frame-bound micro-segments (100% Image-Audio Binding)
    print("\n--- [3/4] Rendering 36 micro-segments (guaranteeing 100% frame sync) ---")
    vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#FAF9F6,setsar=1,fps=30"
    segment_files = []

    for sid in range(1, 37):
        img_name, dur = slide_durations[sid - 1]
        img_path = SLIDES_DIR / img_name
        audio_path = AUDIO_DIR_EN / f"shot_{sid:03d}.mp3"
        seg_out = SEGMENTS_DIR / f"seg_{sid:02d}.mp4"

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

    seg_list_path = SEGMENTS_DIR / "concat_segments.txt"
    with open(seg_list_path, "w", encoding="utf-8") as f:
        for seg in segment_files:
            f.write(f"file '{seg.as_posix()}'\n")

    # 4. Concatenate segments into clean preview video
    out_no_bgm = RENDERS_DIR / "ch01_the_pedestal_paradox_preview_no_bgm.mp4"
    print(f"\n--- [4/4] Assembling full video ---")
    print(f"  Rendering clean narration preview: {out_no_bgm.name}")

    cmd_stitch = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(seg_list_path),
        "-c", "copy",
        str(out_no_bgm)
    ]
    subprocess.run(cmd_stitch, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  ✓ Rendered narration preview: {out_no_bgm}")

    # Render production version with subtle BGM ducking
    out_with_bgm = RENDERS_DIR / "ch01_the_pedestal_paradox_preview.mp4"
    central_out = CENTRAL_RENDERS_DIR / "ch01_the_pedestal_paradox_preview.mp4"

    if BGM_PATH.exists():
        print(f"  Adding atmospheric BGM track: {BGM_PATH.name}")
        fade_out_start = max(0, total_audio_dur - 2.5)
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

    print("\n" + "=" * 60)
    print("  CHAPTER 01 VIDEO ASSEMBLY COMPLETE!")
    print(f"  Narration Only: {out_no_bgm}")
    if out_with_bgm.exists():
        print(f"  With Subtle BGM: {out_with_bgm}")
    print("=" * 60)

if __name__ == "__main__":
    main()
