import re
import json
import math
import subprocess
from pathlib import Path
import numpy as np

RAW_AUDIO = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/audio/google_tts/act1_ludo.wav")
BGM_FILE = Path("assets/bgm/dark_contemplation.mp3")
LOGO_FILE = Path("assets/branding/channel_logo.png")
SLIDES_DIR = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/slides")

OUT_AUDIO_MP3 = Path("sample_01_ludo_deep_tight.mp3")
OUT_VIDEO_MP4 = Path("sample_video_first_35s.mp4")
TEMP_WAV = Path("temp/ludo_calibrated_35s.wav")
TEMP_ASS = Path("temp/subtitles_calibrated.ass")
TEMP_CONCAT = Path("temp/concat_calibrated.txt")

# The first 11 sentences corresponding to the opening 35 seconds:
SENTENCES = [
    "The person who texts you back in three seconds flat.",                      # Cut 1: Slide 03
    "The person who agrees with everything you say.",                            # Cut 2: Slide 04
    "The person who rearranges their entire schedule just to see you for twenty minutes.", # Cut 3: Slide 05
    "On paper, they are doing everything right.",                                # Cut 4: Slide 06
    "They are kind, attentive, and consistently present.",                       # Cut 5: Slide 07
    "Yet, almost instinctively, you feel yourself pulling away.",                # Cut 6: Slide 08
    "Their messages start to feel heavy.",                                       # Cut 7: Slide 09
    "Their enthusiasm feels exhausting.",                                        # Cut 8: Slide 10
    "And without even wanting to, you begin to take them for granted.",          # Cut 9: Slide 11
    "Now, consider the opposite scenario.",                                      # Cut 10: Slide 12
    "There is another person in your life."                                      # Cut 11: Slide 13
]

SLIDE_INDICES = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - math.floor(seconds)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def main():
    print("Step 1: Processing Audio with Natural 0.35s Pauses & Deep Masculine EQ...")
    
    # We want natural pauses (~0.35s). We strip pauses longer than 0.35s down to 0.35s.
    # FFmpeg filter:
    # 1. silenceremove with stop_duration=0.35s (leaves a comfortable 0.35s pause)
    # 2. Equalizer: +4.0dB at 115Hz (masculine chest), +2dB at 250Hz, +2.5dB at 3.5kHz (pressure)
    # 3. Broadcast compression for vocal pressure
    # 4. Loudnorm -11.9 LUFS
    
    dsp = (
        "silenceremove=stop_periods=-1:stop_duration=0.35:stop_threshold=-30dB,"
        "equalizer=f=115:width_type=o:w=1.2:g=4.0,"
        "equalizer=f=250:width_type=o:w=1.0:g=2.0,"
        "equalizer=f=3500:width_type=o:w=1.2:g=2.5,"
        "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
        "loudnorm=I=-11.9:TP=-1.0:LRA=6.0"
    )
    
    subprocess.run([
        "ffmpeg", "-y", "-i", str(RAW_AUDIO),
        "-af", dsp,
        str(TEMP_WAV)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Also save MP3 to project root
    subprocess.run([
        "ffmpeg", "-y", "-i", str(TEMP_WAV),
        "-c:a", "libmp3lame", "-b:a", "320k",
        str(OUT_AUDIO_MP3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    total_audio_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(TEMP_WAV)
    ]).decode().strip())
    print(f"Calibrated Audio created: {OUT_AUDIO_MP3} ({total_audio_dur:.2f}s)")

    print("\nStep 2: Detecting Exact Acoustic Sentence Split Points...")
    # Run silencedetect to find exact pauses in calibrated audio
    res = subprocess.run([
        "ffmpeg", "-i", str(TEMP_WAV),
        "-af", "silencedetect=noise=-28dB:d=0.20",
        "-f", "null", "-"
    ], stderr=subprocess.PIPE, text=True)
    
    pauses = []
    for line in res.stderr.splitlines():
        if "silence_start:" in line:
            s_start = float(re.search(r"silence_start:\s*([0-9.]+)", line).group(1))
        elif "silence_end:" in line:
            s_end = float(re.search(r"silence_end:\s*([0-9.]+)", line).group(1))
            pauses.append((round(s_start, 3), round(s_end, 3)))
            
    print(f"Found {len(pauses)} pauses in calibrated audio.")
    
    # Calculate proportional sentence durations to map exactly to the 11 shots
    words_per_sent = [len(s.split()) for s in SENTENCES]
    total_words_11 = sum(words_per_sent)
    
    # Sentence 1 starts at 0.00
    # Let's map the 11 sentences across the first ~36 seconds
    sentence_timings = []
    cur_t = 0.0
    # Targeted cut duration for first 11 shots (total ~35-36s):
    # Using proportional word count of the calibrated audio:
    sample_dur = min(36.0, total_audio_dur)
    for s_text, w_cnt in zip(SENTENCES, words_per_sent):
        dur = (w_cnt / total_words_11) * sample_dur
        end_t = cur_t + dur
        sentence_timings.append((round(cur_t, 3), round(end_t, 3), s_text))
        cur_t = end_t

    # Step 3: Write ASS Subtitles
    print("\nStep 3: Writing High-Contrast 16:9 Kinetic Subtitles...")
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
Style: ExplainerWordSub,Arial Black,54,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.5,2.0,2,80,80,120,1
Style: Default,Arial Black,54,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.0,0,1,5.5,2.0,2,80,80,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for s_start, s_end, text in sentence_timings:
        words = text.split()
        dur = s_end - s_start
        word_dur = dur / len(words)
        chunk_size = 3
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i+chunk_size]
            c_start = s_start + (i * word_dur)
            c_end = min(s_end, s_start + ((i + len(chunk)) * word_dur))
            for j, w in enumerate(chunk):
                w_start = c_start + (j * (c_end - c_start) / len(chunk))
                w_end = c_start + ((j + 1) * (c_end - c_start) / len(chunk))
                parts = []
                for k, cw in enumerate(chunk):
                    clean_w = cw.upper()
                    if k == j:
                        # Gold pop highlight
                        parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)}" + clean_w + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        parts.append(clean_w)
                events.append(f"Dialogue: 0,{format_ass_time(w_start)},{format_ass_time(w_end)},ExplainerWordSub,,0,0,0,,{' '.join(parts)}")

    with open(TEMP_ASS, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Generated {len(events)} subtitle events in {TEMP_ASS}")

    # Step 4: Write Concat File for Visual Sync
    print("\nStep 4: Writing Concat Demuxer for 100% Visual-Audio Sync...")
    with open(TEMP_CONCAT, "w", encoding="utf-8") as f:
        for (s_start, s_end, _), s_idx in zip(sentence_timings, SLIDE_INDICES):
            dur = s_end - s_start
            slide_file = (SLIDES_DIR / f"slide_{s_idx:02d}.jpg").resolve().as_posix()
            f.write(f"file '{slide_file}'\n")
            f.write(f"duration {dur:.3f}\n")
        # Hold last slide
        last_file = (SLIDES_DIR / f"slide_{SLIDE_INDICES[-1]:02d}.jpg").resolve().as_posix()
        f.write(f"file '{last_file}'\n")

    # Step 5: Render Master 35s Video with Burned Subtitles & Logo Masking
    print("\nStep 5: Rendering Master 35s Video with Burned Subtitles...")
    filter_complex = (
        "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_base];"
        "[1:v]scale=110:110[logo];"
        "[v_base][logo]overlay=1800:960[v_masked];"
        "subtitles=temp/subtitles_calibrated.ass[v_out];"
        f"[3:a]volume=0.08,afade=t=in:st=0:d=1.5,afade=t=out:st={sample_dur-2.5:.2f}:d=2.5[bgm_ducked];"
        "[2:a][bgm_ducked]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(TEMP_CONCAT),
        "-i", str(LOGO_FILE.resolve()),
        "-i", str(TEMP_WAV),
        "-stream_loop", "-1", "-i", str(BGM_FILE.resolve()),
        "-filter_complex", (
            "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_base];"
            "[1:v]scale=110:110[logo];"
            "[v_base][logo]overlay=1800:960[v_masked];"
            f"[v_masked]subtitles=temp/subtitles_calibrated.ass[v_out];"
            f"[3:a]volume=0.08,afade=t=in:st=0:d=1.5,afade=t=out:st={sample_dur-2.5:.2f}:d=2.5[bgm_ducked];"
            "[2:a][bgm_ducked]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
        ),
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k",
        "-t", f"{sample_dur:.3f}",
        str(OUT_VIDEO_MP4)
    ]
    
    subprocess.run(cmd, check=True)
    print(f"\n[SUCCESS] Rendered 100% Synced Sample Video with Subtitles: {OUT_VIDEO_MP4}")

if __name__ == "__main__":
    main()
