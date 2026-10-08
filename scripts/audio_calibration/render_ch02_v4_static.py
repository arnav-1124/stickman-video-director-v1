import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import cv2
import math
import time
import subprocess
import shutil
from pathlib import Path
import numpy as np

def format_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

# Workspace paths
CH02_DIR = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_02_the_casino_effect")
CH03_DIR = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_03_the_economy_of_availability")
SLIDES_DIR = CH02_DIR / "slides"
CARDS_DIR = SLIDES_DIR / "cards"
VOICE_WAV = Path("temp/ch02_v2_continuous_build/ch02_v2_voice_mastered.wav")
BGM_MP3 = Path("assets/bgm/dark_contemplation.mp3")
LOGO_PNG = Path("assets/branding/channel_logo.png")
SENTENCES_TXT = Path("temp/ch02_exact_sentence_timestamps.txt")

# Complete 64-Shot Static Storyboard (No Ken Burns, pure 1.0x framing)
# Max single-shot duration <= 4.3s, average duration ~2.64s
STATIC_SHOTS = [
    # Act 1 (Title, Lab, Skinner, Predictable Reward)
    (1, SLIDES_DIR / "slide_37.jpg", 0.000, 2.164, "Title: Chapter Two The Casino Effect"),
    (2, SLIDES_DIR / "slide_37_b.jpg", 2.164, 4.304, "Title: The Dopamine of Uncertainty (NEW)"),
    (3, SLIDES_DIR / "slide_38.jpg", 4.304, 6.700, "Psychology lab retro 1950s"),
    (4, SLIDES_DIR / "slide_38.jpg", 6.700, 9.200, "Observation chamber wide"),
    (5, SLIDES_DIR / "slide_39.jpg", 9.200, 11.600, "B.F. Skinner at clipboard"),
    (6, SLIDES_DIR / "slide_39.jpg", 11.600, 14.074, "Experiments with animals"),
    (7, SLIDES_DIR / "slide_40.jpg", 14.074, 17.700, "Pigeon inside box with lever"),
    (8, SLIDES_DIR / "slide_41.jpg", 17.700, 20.700, "Press lever food pellet drops"),
    (9, SLIDES_DIR / "slide_41.jpg", 20.700, 23.714, "Press lever get food repetition"),
    (10, CARDS_DIR / "card_what_happened.jpg", 23.714, 24.784, "Card: WHAT HAPPENED?"),
    (11, SLIDES_DIR / "slide_42.jpg", 24.784, 28.984, "Pigeon turns back on lever hungry vs full"),
    (12, CARDS_DIR / "card_100_predictable.jpg", 28.984, 31.100, "Card: 100% PREDICTABLE"),
    (13, CARDS_DIR / "card_reliable_safe_boring.jpg", 31.100, 33.300, "Card: RELIABLE. SAFE. BORING."),
    (14, SLIDES_DIR / "slide_44.jpg", 33.300, 35.200, "Skinner changes the rules"),
    (15, CARDS_DIR / "card_variable_ratio.jpg", 35.200, 37.600, "Card: VARIABLE RATIO SCHEDULE"),
    (16, SLIDES_DIR / "slide_44.jpg", 37.600, 40.000, "Indicator lamp amber switch"),
    (17, SLIDES_DIR / "slide_45.jpg", 40.000, 44.300, "Food only dropped out sometimes"),
    (18, SLIDES_DIR / "slide_46.jpg", 44.300, 46.064, "1 press"),
    (19, SLIDES_DIR / "slide_46.jpg", 46.064, 47.500, "5 presses"),
    (20, CARDS_DIR / "card_reward_unpredictable.jpg", 47.500, 49.500, "Card: 12 PRESSES WITH NOTHING"),
    (21, SLIDES_DIR / "slide_46.jpg", 49.500, 51.500, "2 pellets dropped at once"),
    (22, CARDS_DIR / "card_reward_unpredictable.jpg", 51.500, 53.800, "Card: REWARD UNPREDICTABLE"),
    (23, CARDS_DIR / "card_what_happened.jpg", 53.800, 54.900, "Card: WHAT DID PIGEON DO?"),
    (24, SLIDES_DIR / "slide_47.jpg", 54.900, 56.600, "Completely obsessed dilated eyes"),
    (25, SLIDES_DIR / "slide_48.jpg", 56.600, 59.500, "Pressing frantically for hours"),
    (26, SLIDES_DIR / "slide_48.jpg", 59.500, 62.400, "Ignoring sleep and other birds"),
    (27, SLIDES_DIR / "slide_49.jpg", 62.400, 66.800, "Neurological reward circuitry hijacked"),

    # Act 2 (Neuroscience, Dopamine of Anticipation, The Slot Machine)
    (28, SLIDES_DIR / "slide_50.jpg", 66.800, 70.300, "Neuroscientists know why this happens"),
    (29, SLIDES_DIR / "slide_51.jpg", 70.300, 73.000, "Dopamine is not pleasure"),
    (30, CARDS_DIR / "card_dopamine_anticipation.jpg", 73.000, 75.700, "Card: DOPAMINE IS ANTICIPATION"),
    (31, SLIDES_DIR / "slide_52.jpg", 75.700, 80.200, "Brain does not release biggest spike when prize received"),
    (32, SLIDES_DIR / "slide_53.jpg", 80.200, 82.700, "Massive volcanic dopamine eruption"),
    (33, CARDS_DIR / "card_dopamine_anticipation.jpg", 82.700, 85.200, "Card: UNCERTAINTY SPIKE"),
    (34, SLIDES_DIR / "slide_54.jpg", 85.200, 88.500, "Slot machines and lottery tickets"),
    (35, SLIDES_DIR / "slide_54.jpg", 88.500, 91.800, "Social media notification badges"),
    (36, SLIDES_DIR / "slide_55.jpg", 91.800, 94.300, "Pull lever on slot machine"),
    (37, SLIDES_DIR / "slide_55.jpg", 94.300, 96.800, "Spinning reels thrilling tension"),
    (38, CARDS_DIR / "card_unresolved_gap.jpg", 96.800, 99.900, "Card: WILL 3 CHERRIES ALIGN?"),
    (39, SLIDES_DIR / "slide_56.jpg", 99.900, 104.000, "Unresolved gap between hope and fear"),

    # Act 3 (Human Interaction, Available vs Aloof, The Chemical Cocktail)
    (40, CARDS_DIR / "card_aloof_casino.jpg", 104.000, 105.740, "Card: BRING TO HUMAN INTERACTION"),
    (41, SLIDES_DIR / "slide_57.jpg", 105.740, 109.650, "Always available person like first lever"),
    (42, SLIDES_DIR / "slide_58.jpg", 109.650, 112.000, "Text them reply in 30 seconds"),
    (43, SLIDES_DIR / "slide_58.jpg", 112.000, 114.500, "Compliment them shower praise"),
    (44, SLIDES_DIR / "slide_58.jpg", 114.500, 116.800, "Ask to meet immediately say yes"),
    (45, CARDS_DIR / "card_100_predictable.jpg", 116.800, 119.000, "Card: 100% PREDICTABLE"),
    (46, SLIDES_DIR / "slide_59.jpg", 119.000, 120.200, "No mystery"),
    (47, SLIDES_DIR / "slide_59.jpg", 120.200, 121.500, "No tension"),
    (48, SLIDES_DIR / "slide_60.jpg", 121.500, 124.400, "No anticipation no dopamine"),
    (49, CARDS_DIR / "card_zero_pull.jpg", 124.400, 126.800, "Card: ZERO GRAVITATIONAL PULL"),
    (50, SLIDES_DIR / "slide_61.jpg", 126.800, 129.100, "Weightless stickman floating"),
    (51, CARDS_DIR / "card_aloof_casino.jpg", 129.100, 131.200, "Card: THE ALOOF CASINO"),
    (52, SLIDES_DIR / "slide_62.jpg", 131.200, 133.450, "Aloof person in dark hoodie leaning"),
    (53, SLIDES_DIR / "slide_63.jpg", 133.450, 137.000, "Rare meaningful glance"),
    (54, SLIDES_DIR / "slide_64.jpg", 137.000, 140.200, "Compliment sticks for 3 weeks"),
    (55, CARDS_DIR / "card_three_weeks_later.jpg", 140.200, 143.400, "Card: 3 WEEKS LATER (NEW)"),
    (56, SLIDES_DIR / "slide_65.jpg", 143.400, 146.900, "Phone lights up heart skips beat"),
    (57, CARDS_DIR / "card_unresolved_gap.jpg", 146.900, 149.200, "Card: UNRESOLVED GAP"),
    (58, SLIDES_DIR / "slide_65.jpg", 149.200, 151.600, "Did not know if they would reply at all"),
    (59, SLIDES_DIR / "slide_66.jpg", 151.600, 154.500, "Not in love with person"),
    (60, CARDS_DIR / "card_chemical_cocktail.jpg", 154.500, 158.500, "Card: CHEMICAL COCKTAIL (NEW)"),

    # Outro (Chapter 3 Teaser, Economy of Availability, Subscribe CTA)
    (61, CH03_DIR / "slides" / "slide_67.jpg", 158.500, 161.800, "Chapter 3 teaser: having somewhere else to be"),
    (62, CH03_DIR / "slides" / "slide_67.jpg", 161.800, 164.500, "Walking out the door into neon night"),
    (63, CH03_DIR / "slides" / "slide_67.jpg", 164.500, 166.600, "The economy of availability title hold"),
    (64, CH03_DIR / "slides" / "slide_67.jpg", 166.600, 169.180, "Subscribe to Sticky in Dark CTA hold")
]

def generate_subtitles(out_ass_path):
    sentences = []
    with open(SENTENCES_TXT, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split(']')
            time_part = parts[0].replace('[', '')
            text = parts[1].strip() if len(parts) > 1 else ''
            t1, t2 = time_part.split('-->')
            m1, s1 = t1.strip().split(':')
            m2, s2 = t2.strip().split(':')
            st = int(m1)*60 + float(s1)
            et = int(m2)*60 + float(s2)
            sentences.append((st, et, text))

    header = """[Script Info]
Title: Sticky in Dark 16:9 Kinetic Subtitles - Chapter 02 (Static Master Synchronized)
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ExplainerWordSub,Arial Black,50,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.0,2.0,2,80,80,110,1
Style: OutroWordSub,Arial Black,46,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.0,2.0,2,80,80,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = []
    chunk_size = 4

    for s_start, s_end, s_text in sentences:
        words = s_text.split()
        if not words: continue

        s_dur = max(0.2, s_end - s_start)
        # Weight word duration by length for natural speech cadence
        weights = [max(2, len(w)) for w in words]
        total_w = sum(weights)
        word_durs = [(w / total_w) * s_dur for w in weights]

        w_times = []
        curr = s_start
        for wd in word_durs:
            w_times.append((curr, curr + wd))
            curr += wd
        w_times[-1] = (w_times[-1][0], s_end)

        style = "OutroWordSub" if s_start >= 158.0 else "ExplainerWordSub"

        for i in range(0, len(words), chunk_size):
            chunk = words[i:i+chunk_size]
            chunk_w_times = w_times[i:i+len(chunk)]

            for j, (w_s, w_e) in enumerate(chunk_w_times):
                if w_e <= w_s: continue
                line_parts = []
                for k, w_text in enumerate(chunk):
                    cw = w_text.upper().replace('"', '').replace('—', ' - ')
                    if k == j:
                        # Gold pop highlight
                        line_parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)}" + cw + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        line_parts.append(cw)
                display_text = " ".join(line_parts)
                events.append(f"Dialogue: 0,{format_ass(w_s)},{format_ass(w_e)},{style},,0,0,0,,{display_text}")

    with open(out_ass_path, 'w', encoding='utf-8') as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Generated {len(events)} synchronized kinetic subtitle events.")

def main():
    print("=" * 80)
    print("  🎬 RENDERING CHAPTER 02 V4: PURE STATIC MASTER WITH OPTIMIZED PACING")
    print("=" * 80)

    t_start = time.time()
    out_dir = CH02_DIR / "renders"
    out_dir.mkdir(parents=True, exist_ok=True)
    master_mp4 = out_dir / "WHY_UNPREDICTABLE_PEOPLE_ARE_ADDICTIVE_Chapter_02_V4_STATIC_MASTER.mp4"
    central_mp4 = Path("renders/long/ep01_why_people_fall_for_who_ignores_them/WHY_UNPREDICTABLE_PEOPLE_ARE_ADDICTIVE_Chapter_02_V4_STATIC_MASTER.mp4")
    central_mp4.parent.mkdir(parents=True, exist_ok=True)

    sub_ass = CH02_DIR / "subtitles_ch02_v4_synchronized.ass"
    generate_subtitles(sub_ass)

    fps = 30
    w_out, h_out = 1920, 1080
    total_video_dur = STATIC_SHOTS[-1][3]
    total_frames = int(round(total_video_dur * fps))
    print(f"Total Video Duration: {total_video_dur:.3f}s ({total_frames} frames across {len(STATIC_SHOTS)} static shots)")

    raw_video_mp4 = Path("temp/ch02_v4_raw_video.mp4")
    raw_video_mp4.parent.mkdir(parents=True, exist_ok=True)

    # 1. Pipe pure static 1080p frames directly into FFmpeg
    cmd_pipe = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{w_out}x{h_out}", "-pix_fmt", "bgr24", "-r", str(fps),
        "-i", "pipe:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(raw_video_mp4)
    ]
    proc = subprocess.Popen(cmd_pipe, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    loaded_images = {}
    print("\nEncoding pure 1.0x static shots (zero camera drift, zero black borders)...")

    for shot_idx, (sid, fpath, ts, te, desc) in enumerate(STATIC_SHOTS):
        shot_dur = te - ts
        shot_frames = int(round(shot_dur * fps))
        if shot_frames <= 0: continue

        sp_key = str(fpath.resolve())
        if sp_key not in loaded_images:
            img = cv2.imread(sp_key)
            if img is None:
                raise RuntimeError(f"Could not load image: {fpath}")
            # Resize directly to 1920x1080 (all assets are 16:9)
            resized = cv2.resize(img, (w_out, h_out), interpolation=cv2.INTER_AREA)
            loaded_images[sp_key] = resized.tobytes()

        frame_bytes = loaded_images[sp_key]
        for _ in range(shot_frames):
            proc.stdin.write(frame_bytes)

        if (shot_idx + 1) % 15 == 0 or shot_idx == len(STATIC_SHOTS) - 1:
            print(f"  Processed {shot_idx + 1}/{len(STATIC_SHOTS)} shots ({desc[:40]})...")

    proc.stdin.close()
    proc.wait()
    print("Static video track encoded.")

    # 2. Final assembly: Burn subtitles, watermark logo, duck BGM, master audio
    print("\nFinalizing master audio/video muxing with kinetic subtitles and BGM...")
    sub_escaped = sub_ass.resolve().as_posix().replace(":", "\\:").replace("'", "\\'")
    filter_complex = (
        f"[0:v][2:v]overlay=W-w-50:50:format=auto[vbranded];"
        f"[vbranded]subtitles='{sub_escaped}'[vfinal];"
        f"[3:a]volume=0.08,afade=t=in:st=0:d=2.0,afade=t=out:st={total_video_dur-3.0:.2f}:d=3.0[bgm];"
        f"[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[afinal]"
    )

    cmd_final = [
        "ffmpeg", "-y",
        "-i", str(raw_video_mp4),
        "-i", str(VOICE_WAV),
        "-loop", "1", "-i", str(LOGO_PNG.resolve()),
        "-stream_loop", "-1", "-i", str(BGM_MP3.resolve()),
        "-filter_complex", filter_complex,
        "-map", "[vfinal]",
        "-map", "[afinal]",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
        "-t", f"{total_video_dur:.3f}",
        "-movflags", "+faststart",
        str(master_mp4)
    ]
    subprocess.run(cmd_final, check=True)

    shutil.copy2(master_mp4, central_mp4)

    print("\n" + "=" * 80)
    print("  🎉 CHAPTER 02 V4 STATIC MASTER RENDER COMPLETE!")
    print("=" * 80)
    print(f"Local Master:   {master_mp4.resolve().as_posix()}")
    print(f"Central Master: {central_mp4.resolve().as_posix()}")
    print(f"Total processing time: {time.time() - t_start:.1f}s")

if __name__ == "__main__":
    main()
