import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import cv2
import math
import time
import subprocess
from pathlib import Path
import numpy as np

def format_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

# Complete 53-Shot Cinematic Storyboard
# Format: (shot_id, file_path, start_t, end_t, start_zoom, end_zoom, (cx1, cy1), (cx2, cy2), description)
CH02_DIR = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_02_the_casino_effect")
CH03_DIR = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_03_the_economy_of_availability")
SLIDES_DIR = CH02_DIR / "slides"
CARDS_DIR = SLIDES_DIR / "cards"

CINEMATIC_SHOTS = [
    # Act 1
    (1, SLIDES_DIR / "slide_37.jpg", 0.08, 2.16, 1.00, 1.06, (0.50, 0.50), (0.50, 0.50), "Title Card Subtle Push"),
    (2, SLIDES_DIR / "slide_37.jpg", 2.16, 4.22, 1.06, 1.18, (0.50, 0.50), (0.50, 0.60), "Push into slot machine reels"),
    (3, SLIDES_DIR / "slide_38.jpg", 4.22, 6.60, 1.00, 1.06, (0.46, 0.50), (0.54, 0.50), "Tracking pan across retro lab"),
    (4, SLIDES_DIR / "slide_38.jpg", 6.60, 9.00, 1.25, 1.34, (0.50, 0.55), (0.50, 0.52), "Close-up cut on center chamber"),
    (5, SLIDES_DIR / "slide_39.jpg", 9.00, 11.50, 1.00, 1.06, (0.50, 0.50), (0.50, 0.48), "Wide view of Skinner at clipboard"),
    (6, SLIDES_DIR / "slide_39.jpg", 11.50, 13.90, 1.28, 1.36, (0.52, 0.42), (0.52, 0.40), "Push past glasses to observation window"),
    (7, SLIDES_DIR / "slide_40.jpg", 13.90, 17.60, 1.02, 1.08, (0.50, 0.50), (0.52, 0.50), "Profile creep towards pigeon and brass lever"),
    (8, SLIDES_DIR / "slide_41.jpg", 17.60, 19.80, 1.00, 1.06, (0.50, 0.50), (0.50, 0.50), "Wide tap action"),
    (9, SLIDES_DIR / "slide_41.jpg", 19.80, 21.84, 1.32, 1.38, (0.52, 0.58), (0.52, 0.60), "Punch-in on food pellet dropping into bowl"),
    (10, SLIDES_DIR / "slide_41.jpg", 21.84, 24.76, 1.10, 1.18, (0.50, 0.50), (0.52, 0.52), "Rhythmic mechanical repetition push"),
    (11, CARDS_DIR / "card_what_happened.jpg", 24.76, 26.50, 1.00, 1.08, (0.50, 0.50), (0.50, 0.50), "High-impact punch card pop"),
    (12, SLIDES_DIR / "slide_42.jpg", 26.50, 29.18, 1.12, 1.00, (0.50, 0.50), (0.48, 0.50), "Pull-back: pigeon turns back on lever"),
    (13, CARDS_DIR / "card_100_predictable.jpg", 29.18, 31.02, 1.00, 1.06, (0.50, 0.50), (0.50, 0.50), "Predictability flatline card"),
    (14, CARDS_DIR / "card_reliable_safe_boring.jpg", 31.02, 33.34, 1.00, 1.08, (0.50, 0.50), (0.50, 0.50), "Triple stamp card pop"),
    (15, SLIDES_DIR / "slide_44.jpg", 33.34, 35.42, 1.00, 1.07, (0.50, 0.50), (0.50, 0.48), "Skinner changes the rules"),
    (16, CARDS_DIR / "card_variable_ratio.jpg", 35.42, 38.00, 1.00, 1.06, (0.50, 0.50), (0.50, 0.50), "Variable-ratio schedule card"),
    (17, SLIDES_DIR / "slide_44.jpg", 38.00, 40.32, 1.25, 1.34, (0.54, 0.42), (0.54, 0.40), "Punch-in on blinking amber indicator"),
    (18, SLIDES_DIR / "slide_45.jpg", 40.32, 44.20, 1.04, 1.12, (0.50, 0.50), (0.50, 0.54), "Tension push on empty food bowl"),
    (19, SLIDES_DIR / "slide_46.jpg", 44.20, 45.54, 1.00, 1.05, (0.50, 0.50), (0.50, 0.50), "1 press rapid beat"),
    (20, SLIDES_DIR / "slide_46.jpg", 45.54, 47.34, 1.08, 1.15, (0.50, 0.50), (0.52, 0.50), "5 presses rapid beat"),
    (21, CARDS_DIR / "card_reward_unpredictable.jpg", 47.34, 49.62, 1.00, 1.08, (0.50, 0.50), (0.50, 0.50), "12 presses nothing card"),
    (22, SLIDES_DIR / "slide_46.jpg", 49.62, 51.92, 1.26, 1.35, (0.50, 0.58), (0.50, 0.60), "Detail cut: 2 pellets drop at once"),
    (23, CARDS_DIR / "card_reward_unpredictable.jpg", 51.92, 53.76, 1.04, 1.10, (0.50, 0.50), (0.50, 0.50), "Reward unpredictable card"),
    (24, CARDS_DIR / "card_what_happened.jpg", 53.76, 54.92, 1.00, 1.07, (0.50, 0.50), (0.50, 0.50), "Pigeon reaction question card"),
    (25, SLIDES_DIR / "slide_47.jpg", 54.92, 56.88, 1.10, 1.25, (0.50, 0.48), (0.50, 0.45), "Dramatic punch-in on obsessive dilated pupils"),
    (26, SLIDES_DIR / "slide_48.jpg", 56.88, 59.80, 1.02, 1.10, (0.48, 0.50), (0.52, 0.50), "Tracking pan across frantic tapping"),
    (27, SLIDES_DIR / "slide_48.jpg", 59.80, 62.50, 1.20, 1.30, (0.52, 0.48), (0.52, 0.46), "Detail cut: stickman ignoring sleep"),
    (28, SLIDES_DIR / "slide_49.jpg", 62.50, 64.50, 1.00, 1.07, (0.50, 0.50), (0.50, 0.50), "Wide brain circuitry"),
    (29, SLIDES_DIR / "slide_49.jpg", 64.50, 66.66, 1.25, 1.35, (0.50, 0.45), (0.50, 0.42), "Deep push into glowing synapses"),

    # Act 2
    (30, SLIDES_DIR / "slide_50.jpg", 67.03, 70.15, 1.00, 1.08, (0.50, 0.50), (0.50, 0.50), "Neuroscientists explanation wide"),
    (31, SLIDES_DIR / "slide_51.jpg", 70.15, 73.25, 1.02, 1.09, (0.48, 0.50), (0.52, 0.50), "Dopamine is not pleasure drift"),
    (32, CARDS_DIR / "card_dopamine_anticipation.jpg", 73.25, 75.93, 1.00, 1.08, (0.50, 0.50), (0.50, 0.50), "Dopamine is anticipation card"),
    (33, SLIDES_DIR / "slide_52.jpg", 75.93, 78.10, 1.00, 1.06, (0.50, 0.50), (0.50, 0.50), "Brain scan prize baseline"),
    (34, SLIDES_DIR / "slide_52.jpg", 78.10, 80.31, 1.28, 1.35, (0.50, 0.48), (0.50, 0.45), "Detail cut on flatline baseline spark"),
    (35, SLIDES_DIR / "slide_53.jpg", 80.31, 83.00, 1.00, 1.08, (0.50, 0.50), (0.50, 0.50), "Massive volcanic dopamine eruption"),
    (36, SLIDES_DIR / "slide_53.jpg", 83.00, 85.61, 1.25, 1.35, (0.50, 0.45), (0.50, 0.40), "Zoom on glowing question mark core"),
    (37, SLIDES_DIR / "slide_54.jpg", 85.61, 88.80, 1.00, 1.07, (0.48, 0.50), (0.52, 0.50), "Slot machines, lottery, notifications wide"),
    (38, SLIDES_DIR / "slide_54.jpg", 88.80, 91.95, 1.26, 1.35, (0.62, 0.50), (0.62, 0.48), "Detail zoom on glowing red notification badge"),
    (39, SLIDES_DIR / "slide_55.jpg", 91.95, 94.20, 1.00, 1.06, (0.50, 0.50), (0.50, 0.50), "Pull lever on slot machine"),
    (40, SLIDES_DIR / "slide_55.jpg", 94.20, 96.57, 1.25, 1.35, (0.46, 0.50), (0.54, 0.50), "Horizontal tracking across spinning reels"),
    (41, CARDS_DIR / "card_unresolved_gap.jpg", 96.57, 99.91, 1.00, 1.08, (0.50, 0.50), (0.50, 0.50), "Will 3 cherries align tension card"),
    (42, SLIDES_DIR / "slide_56.jpg", 99.91, 103.71, 1.05, 1.15, (0.50, 0.50), (0.50, 0.48), "Unresolved gap between hope and fear"),

    # Act 3
    (43, CARDS_DIR / "card_aloof_casino.jpg", 104.24, 105.74, 1.00, 1.07, (0.50, 0.50), (0.50, 0.50), "Shift to human interaction card"),
    (44, SLIDES_DIR / "slide_57.jpg", 105.74, 109.46, 1.02, 1.09, (0.50, 0.50), (0.50, 0.50), "Available person as the first lever"),
    (45, SLIDES_DIR / "slide_58.jpg", 109.46, 111.78, 1.28, 1.35, (0.52, 0.50), (0.52, 0.48), "Detail: text reply in 30 seconds"),
    (46, SLIDES_DIR / "slide_58.jpg", 111.78, 114.40, 1.00, 1.07, (0.50, 0.50), (0.50, 0.50), "Wide: showered with praise"),
    (47, SLIDES_DIR / "slide_58.jpg", 114.40, 116.66, 1.15, 1.25, (0.50, 0.55), (0.50, 0.52), "Instant YES calendar invite"),
    (48, CARDS_DIR / "card_100_predictable.jpg", 116.66, 119.22, 1.00, 1.08, (0.50, 0.50), (0.50, 0.50), "100% predictable card"),
    (49, SLIDES_DIR / "slide_59.jpg", 119.22, 120.32, 1.00, 1.06, (0.50, 0.50), (0.50, 0.50), "There is no mystery"),
    (50, SLIDES_DIR / "slide_59.jpg", 120.32, 121.32, 1.10, 1.18, (0.50, 0.50), (0.50, 0.48), "There is no tension bored detail"),
    (51, SLIDES_DIR / "slide_60.jpg", 121.32, 124.56, 1.04, 1.12, (0.50, 0.50), (0.50, 0.50), "No anticipation no dopamine"),
    (52, CARDS_DIR / "card_zero_pull.jpg", 124.56, 126.80, 1.00, 1.06, (0.50, 0.50), (0.50, 0.50), "Zero gravitational pull card"),
    (53, SLIDES_DIR / "slide_61.jpg", 126.80, 128.82, 1.05, 1.14, (0.50, 0.50), (0.48, 0.50), "Floating weightless stickman"),
    (54, CARDS_DIR / "card_aloof_casino.jpg", 128.82, 131.00, 1.00, 1.07, (0.50, 0.50), (0.50, 0.50), "The aloof slot machine card"),
    (55, SLIDES_DIR / "slide_62.jpg", 131.00, 133.36, 1.04, 1.12, (0.50, 0.50), (0.50, 0.48), "Aloof sovereign in dark hoodie leaning"),
    (56, SLIDES_DIR / "slide_63.jpg", 133.36, 136.84, 1.05, 1.15, (0.50, 0.50), (0.52, 0.48), "Rare meaningful glance creep"),
    (57, SLIDES_DIR / "slide_64.jpg", 136.84, 140.10, 1.00, 1.07, (0.50, 0.50), (0.50, 0.50), "Compliment sticks for 3 weeks calendar"),
    (58, SLIDES_DIR / "slide_64.jpg", 140.10, 143.54, 1.25, 1.35, (0.50, 0.48), (0.50, 0.45), "Rare golden coin in locked vault"),
    (59, SLIDES_DIR / "slide_65.jpg", 143.54, 146.98, 1.08, 1.18, (0.50, 0.50), (0.50, 0.48), "Phone lights up screen flash"),
    (60, CARDS_DIR / "card_unresolved_gap.jpg", 146.98, 149.30, 1.00, 1.06, (0.50, 0.50), (0.50, 0.50), "Didn't know if they'd reply card"),
    (61, SLIDES_DIR / "slide_65.jpg", 149.30, 151.70, 1.22, 1.30, (0.50, 0.48), (0.50, 0.46), "Stickman staring at glowing phone"),
    (62, SLIDES_DIR / "slide_66.jpg", 151.70, 154.22, 1.00, 1.07, (0.50, 0.50), (0.50, 0.50), "Not in love with person wide"),
    (63, SLIDES_DIR / "slide_66.jpg", 154.22, 158.22, 1.08, 1.18, (0.50, 0.48), (0.50, 0.45), "In love with unpredictability cocktail"),

    # Outro
    (64, CH03_DIR / "slides" / "slide_67.jpg", 158.99, 161.60, 1.00, 1.06, (0.50, 0.50), (0.50, 0.50), "Chapter 3 teaser wide"),
    (65, CH03_DIR / "slides" / "slide_67.jpg", 161.60, 164.33, 1.20, 1.30, (0.52, 0.48), (0.52, 0.45), "Stickman walking out the door"),
    (66, CH03_DIR / "slides" / "slide_67.jpg", 164.33, 165.69, 1.12, 1.20, (0.50, 0.50), (0.50, 0.48), "Economy of availability punch"),
    (67, CH03_DIR / "slides" / "slide_67.jpg", 165.69, 169.13, 1.05, 1.15, (0.50, 0.50), (0.50, 0.50), "Subscribe to Sticky in Dark hold")
]

def generate_kinetic_subtitles(out_ass):
    words_data = []
    import re
    time_re = re.compile(r'\[(\d+):([\d\.]+) --> (\d+):([\d\.]+)\]\s*(.*)')
    with open('temp/calibrated_word_timestamps.txt', encoding='utf-8') as f:
        for line in f:
            m = time_re.match(line.strip())
            if m:
                m1, s1, m2, s2, w = m.groups()
                t_start = int(m1) * 60 + float(s1)
                t_end = int(m2) * 60 + float(s2)
                clean_w = w.strip()
                if clean_w:
                    words_data.append((t_start, t_end, clean_w))

    header = """[Script Info]
Title: Sticky in Dark 16:9 Kinetic Subtitles - Chapter 02 (Acoustic Word Synced)
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
    for i in range(0, len(words_data), chunk_size):
        chunk = words_data[i:i+chunk_size]
        for j, (w_s, w_e, _) in enumerate(chunk):
            style = "OutroWordSub" if w_s >= 158.0 else "ExplainerWordSub"
            line_parts = []
            for k, (_, _, w_text) in enumerate(chunk):
                cw = w_text.upper().replace('"', '').replace('—', ' - ')
                if k == j:
                    line_parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)}" + cw + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                else:
                    line_parts.append(cw)
            display_text = " ".join(line_parts)
            events.append(f"Dialogue: 0,{format_ass(w_s)},{format_ass(w_e)},{style},,0,0,0,,{display_text}")

    with open(out_ass, 'w', encoding='utf-8') as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Generated {len(events)} acoustic-locked kinetic subtitle events.")

def main():
    print("=" * 80)
    print("  🎬 RENDERING CHAPTER 02 V3: 67-SHOT CINEMATIC KEN BURNS MOTION MASTER")
    print("=" * 80)

    t_start_all = time.time()
    out_dir = CH02_DIR / "renders"
    out_dir.mkdir(parents=True, exist_ok=True)
    master_mp4 = out_dir / "WHY_UNPREDICTABLE_PEOPLE_ARE_ADDICTIVE_Chapter_02_V3_CINEMATIC.mp4"
    central_mp4 = Path("renders/long/ep01_why_people_fall_for_who_ignores_them/WHY_UNPREDICTABLE_PEOPLE_ARE_ADDICTIVE_Chapter_02_V3_CINEMATIC.mp4")
    central_mp4.parent.mkdir(parents=True, exist_ok=True)

    voice_wav = Path("temp/ch02_v2_continuous_build/ch02_v2_voice_mastered.wav")
    bgm_mp3 = Path("assets/bgm/dark_contemplation.mp3")
    logo_png = Path("assets/branding/channel_logo.png")

    sub_ass = CH02_DIR / "subtitles_ch02_v3_acoustic.ass"
    generate_kinetic_subtitles(sub_ass)

    fps = 30
    w_out, h_out = 1920, 1080
    total_video_dur = CINEMATIC_SHOTS[-1][3]
    total_frames = int(round(total_video_dur * fps))
    print(f"Total Video Duration: {total_video_dur:.2f}s ({total_frames} frames across {len(CINEMATIC_SHOTS)} shots)")

    # Render video stream via pipe directly into FFmpeg
    raw_video_mp4 = Path("temp/ch02_v3_motion_video.mp4")
    raw_video_mp4.parent.mkdir(parents=True, exist_ok=True)

    cmd_pipe = [
        "ffmpeg", "-y",
        "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{w_out}x{h_out}", "-pix_fmt", "bgr24", "-r", str(fps),
        "-i", "pipe:0",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        str(raw_video_mp4)
    ]
    proc = subprocess.Popen(cmd_pipe, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    loaded_images = {}
    print("\nRendering frame-by-frame cinematic Ken Burns trajectories with OpenCV...")

    for shot_idx, (sid, fpath, ts, te, z1, z2, (cx1, cy1), (cx2, cy2), desc) in enumerate(CINEMATIC_SHOTS):
        shot_dur = te - ts
        shot_frames = int(round(shot_dur * fps))
        if shot_frames <= 0: continue

        sp_key = str(fpath.resolve())
        if sp_key not in loaded_images:
            img = cv2.imread(sp_key)
            if img is None:
                raise RuntimeError(f"Could not load image: {fpath}")
            loaded_images[sp_key] = img
        src_img = loaded_images[sp_key]
        src_h, src_w = src_img.shape[:2]

        for fi in range(shot_frames):
            prog = fi / max(1, shot_frames - 1)
            # Smooth cosine ease-in-out
            ease = 0.5 * (1.0 - math.cos(prog * math.pi))

            zoom = z1 + (z2 - z1) * ease
            cur_cx = cx1 + (cx2 - cx1) * ease
            cur_cy = cy1 + (cy2 - cy1) * ease

            crop_w = src_w / zoom
            crop_h = src_h / zoom

            px = cur_cx * src_w
            py = cur_cy * src_h

            x1 = int(round(np.clip(px - crop_w / 2.0, 0, src_w - crop_w)))
            y1 = int(round(np.clip(py - crop_h / 2.0, 0, src_h - crop_h)))

            cropped = src_img[y1:int(round(y1 + crop_h)), x1:int(round(x1 + crop_w))]
            frame = cv2.resize(cropped, (w_out, h_out), interpolation=cv2.INTER_CUBIC)
            proc.stdin.write(frame.tobytes())

        if (shot_idx + 1) % 10 == 0 or shot_idx == len(CINEMATIC_SHOTS) - 1:
            print(f"  Processed {shot_idx + 1}/{len(CINEMATIC_SHOTS)} shots...")

    proc.stdin.close()
    proc.wait()
    print("Video motion stream completed.")

    # Final assembly: burn subtitles, add logo watermark, duck BGM
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
        "-i", str(voice_wav),
        "-loop", "1", "-i", str(logo_png.resolve()),
        "-stream_loop", "-1", "-i", str(bgm_mp3.resolve()),
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

    import shutil
    shutil.copy2(master_mp4, central_mp4)

    print("\n" + "=" * 80)
    print("  🎉 CHAPTER 02 V3 CINEMATIC MASTER RENDER COMPLETE!")
    print("=" * 80)
    print(f"Local Master:   {master_mp4.resolve().as_posix()}")
    print(f"Central Master: {central_mp4.resolve().as_posix()}")
    print(f"Total processing time: {time.time() - t_start_all:.1f}s")

if __name__ == "__main__":
    main()
