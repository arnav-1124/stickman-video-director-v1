import os
import re
import json
import math
import subprocess
from pathlib import Path

BASE_DIR = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox")
AUDIO_FILE = BASE_DIR / "audio" / "google_tts" / "master_narration_ludo.wav"
SCRIPT_FILE = BASE_DIR / "script_upgraded.txt"
SLIDES_DIR = BASE_DIR / "slides"
LOGO_FILE = Path("assets/branding/channel_logo.png")
BGM_FILE = Path("assets/bgm/dark_contemplation.mp3")
OUTPUT_DIR = Path("renders/long/ep01_why_people_fall_for_who_ignores_them")
OUTPUT_VIDEO = OUTPUT_DIR / "YOU_REPLIED_INSTANTLY_Chapter_01_MASTER.mp4"

# 36 visual shots rearranged for the viral Cold Open Hook:
# Frame 1 starts on slide_03 (The 3-second text), then continues through the story.
# Slide 02 (The Riddle) and Slide 01 (Title Card) act as the psychological pivot and title reveal at ~1:05.
SHOT_ORDER = [
    3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
    2,  # Slide 02: Why does the human mind do this? (The Riddle)
    1,  # Slide 01: CHAPTER 01 (Title Card Reveal)
    23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36
]

# Relative weights of each shot to distribute audio duration proportionally
SHOT_WEIGHTS = [
    3.2, 2.6, 3.8, 2.5, 3.2, 3.5, 2.4, 2.6, 3.2, 2.5,
    2.5, 2.8, 3.2, 2.4, 2.4, 4.5, 2.6, 2.0, 5.5, 4.0,
    4.5,  # Slide 02
    3.5,  # Slide 01
    3.0, 3.2, 3.0, 3.5, 3.8, 3.5, 4.2, 4.0, 3.2, 4.5, 4.2, 3.8, 3.5, 4.5
]

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - math.floor(seconds)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_subtitles(total_dur, script_path, output_ass):
    with open(script_path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    total_words = sum(len(l.split()) for l in lines)
    sentence_timings = []
    cur_t = 0.0
    for l in lines:
        w_cnt = len(l.split())
        line_dur = (w_cnt / total_words) * total_dur
        end_t = min(total_dur, cur_t + line_dur)
        sentence_timings.append((round(cur_t, 3), round(end_t, 3), l))
        cur_t = end_t

    header = """[Script Info]
Title: Sticky in Dark 16:9 Kinetic Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ExplainerWordSub,Arial Black,50,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.0,2.0,2,80,80,110,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for s_start, s_end, text in sentence_timings:
        words = text.split()
        if not words: continue
        dur = s_end - s_start
        word_dur = dur / len(words)
        chunk_size = 3
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i+chunk_size]
            chunk_start = s_start + (i * word_dur)
            chunk_end = min(s_end, s_start + ((i + len(chunk_words)) * word_dur))
            for j, w in enumerate(chunk_words):
                w_start = chunk_start + (j * (chunk_end - chunk_start) / len(chunk_words))
                w_end = chunk_start + ((j + 1) * (chunk_end - chunk_start) / len(chunk_words))
                display_parts = []
                for k, cw in enumerate(chunk_words):
                    clean_w = cw.upper()
                    if k == j:
                        display_parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)}" + clean_w + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        display_parts.append(clean_w)
                line_text = " ".join(display_parts)
                events.append(f"Dialogue: 0,{format_ass_time(w_start)},{format_ass_time(w_end)},ExplainerWordSub,,0,0,0,,{line_text}")

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Generated {len(events)} kinetic subtitle events -> {output_ass}")

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not AUDIO_FILE.exists():
        print(f"Waiting for audio file: {AUDIO_FILE}")
        return

    total_dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(AUDIO_FILE)]).decode().strip())
    print(f"Master Audio Duration: {total_dur:.2f}s")

    # Generate subtitles
    sub_file = BASE_DIR / "subtitles_16_9.ass"
    generate_subtitles(total_dur, SCRIPT_FILE, sub_file)

    # Distribute cut durations
    weight_sum = sum(SHOT_WEIGHTS)
    cut_durations = [(w / weight_sum) * total_dur for w in SHOT_WEIGHTS]
    
    # Generate concat file
    concat_file = BASE_DIR / "concat_master.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for idx, dur in zip(SHOT_ORDER, cut_durations):
            slide_path = SLIDES_DIR / f"slide_{idx:02d}.jpg"
            # Format as absolute forward-slash path for FFmpeg
            f.write(f"file '{slide_path.resolve().as_posix()}'\n")
            f.write(f"duration {dur:.3f}\n")
        # Final frame hold
        last_slide = SLIDES_DIR / f"slide_{SHOT_ORDER[-1]:02d}.jpg"
        f.write(f"file '{last_slide.resolve().as_posix()}'\n")

    print(f"Generated concat demuxer file with 36 cuts -> {concat_file}")

    # Build Unified FFmpeg Command
    # 1. Slide sequence (concat demuxer)
    # 2. Channel logo (for watermark masking at 1800, 960)
    # 3. Master narration
    # 4. Looped BGM ducked to -23dB
    
    # Subtitle path formatted for libass filter (escape colons and backslashes)
    sub_filter_path = sub_file.resolve().as_posix().replace(":", r"\:")
    
    filter_complex = (
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_base];"
        f"[1:v]scale=110:110[logo];"
        f"[v_base][logo]overlay=1800:960[v_masked];"
        f"[v_masked]subtitles='{sub_filter_path}'[v_out];"
        f"[3:a]volume=0.08,afade=t=in:st=0:d=2.0,afade=t=out:st={total_dur-3.0:.2f}:d=3.0[bgm_ducked];"
        f"[2:a][bgm_ducked]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(LOGO_FILE.resolve()),
        "-i", str(AUDIO_FILE.resolve()),
        "-stream_loop", "-1", "-i", str(BGM_FILE.resolve()),
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k",
        "-t", f"{total_dur:.3f}",
        str(OUTPUT_VIDEO)
    ]

    print("\nRunning Master FFmpeg Assembly Render...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        out_size = OUTPUT_VIDEO.stat().st_size / (1024 * 1024)
        print(f"\n🎉 MASTER FILM RENDER COMPLETE!")
        print(f"File: {OUTPUT_VIDEO}")
        print(f"Size: {out_size:.2f} MB")
        print(f"Duration: {total_dur:.2f}s")
    else:
        print(f"Error during FFmpeg render:\n{res.stderr}")
        raise RuntimeError("FFmpeg render failed")

if __name__ == "__main__":
    main()
