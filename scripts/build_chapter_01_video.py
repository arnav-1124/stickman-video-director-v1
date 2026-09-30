import os
import sys
import json
import subprocess
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

RENDERS_DIR.mkdir(parents=True, exist_ok=True)
CENTRAL_RENDERS_DIR.mkdir(parents=True, exist_ok=True)

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
            # Check for alternative naming
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
    master_vo_dur = get_duration(MASTER_VO_PATH)
    print(f"\nTotal Shots Audio Duration: {total_audio_dur:.3f}s")
    print(f"Master VO Track Duration:   {master_vo_dur:.3f}s")

    # 2. Write exact concat list
    print("\n--- [2/4] Generating frame-perfect concat list ---")
    concat_file = CH1_DIR / "concat_en_ch01.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for img_name, dur in slide_durations:
            f.write(f"file 'slides/{img_name}'\n")
            f.write(f"duration {dur:.4f}\n")
        # Repeat last file for ffmpeg concat demuxer quirk
        f.write(f"file 'slides/{slide_durations[-1][0]}'\n")

    print(f"  ✓ Updated concat list: {concat_file}")

    # 3. Render clean video (Voiceover only)
    out_no_bgm = RENDERS_DIR / "ch01_the_pedestal_paradox_preview_no_bgm.mp4"
    print(f"\n--- [3/4] Rendering video with narration track ---")
    print(f"  Output: {out_no_bgm.name}")

    # Video filter: scale to 1920x1080 with padding if needed, paper background color #FAF9F6, 30fps
    vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#FAF9F6,setsar=1,fps=30"

    cmd_no_bgm = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0',
        '-i', str(concat_file),
        '-i', str(MASTER_VO_PATH),
        '-vf', vf,
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
        '-shortest',
        str(out_no_bgm)
    ]
    subprocess.run(cmd_no_bgm, check=True)
    print(f"  ✓ Rendered narration preview: {out_no_bgm}")

    # 4. Render production version with subtle BGM ducking
    out_with_bgm = RENDERS_DIR / "ch01_the_pedestal_paradox_preview.mp4"
    central_out = CENTRAL_RENDERS_DIR / "ch01_the_pedestal_paradox_preview.mp4"

    if BGM_PATH.exists():
        print(f"\n--- [4/4] Rendering production video with subtle BGM ---")
        print(f"  BGM Track: {BGM_PATH.name}")
        print(f"  Output: {out_with_bgm.name}")

        fade_out_start = max(0, total_audio_dur - 2.5)
        # BGM: looped, volume scaled to 0.10 (subtle atmospheric lo-fi), soft fade in and fade out
        # Mixed with VO at full clarity (1.0)
        filter_complex = (
            f"[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#FAF9F6,setsar=1,fps=30[v];"
            f"[2:a]volume=0.10,afade=t=in:st=0:d=0.5,afade=t=out:st={fade_out_start:.2f}:d=2.0[bgm];"
            f"[1:a]volume=1.0[vo];"
            f"[vo][bgm]amix=inputs=2:duration=first:normalize=0[aout]"
        )

        cmd_bgm = [
            'ffmpeg', '-y',
            '-f', 'concat', '-safe', '0',
            '-i', str(concat_file),
            '-i', str(MASTER_VO_PATH),
            '-stream_loop', '-1', '-i', str(BGM_PATH),
            '-filter_complex', filter_complex,
            '-map', '[v]',
            '-map', '[aout]',
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
            '-shortest',
            str(out_with_bgm)
        ]
        subprocess.run(cmd_bgm, check=True)
        print(f"  ✓ Rendered production preview with BGM: {out_with_bgm}")

        # Also copy to central renders
        import shutil
        shutil.copy2(str(out_with_bgm), str(central_out))
        print(f"  ✓ Central archive copy: {central_out}")
    else:
        print("  Notice: BGM track not found, skipping BGM mix.")

    print("\n" + "=" * 60)
    print("  CHAPTER 01 VIDEO ASSEMBLY COMPLETE!")
    print(f"  Narration Only: {out_no_bgm}")
    if out_with_bgm.exists():
        print(f"  With Subtle BGM: {out_with_bgm}")
    print("=" * 60)

if __name__ == "__main__":
    main()
