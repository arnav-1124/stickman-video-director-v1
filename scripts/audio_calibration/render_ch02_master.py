import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import math
import wave
import struct
import shutil
import subprocess
from pathlib import Path

def format_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

# Narrative breakdown for all 30 shots across Act 1, Act 2, and Act 3
# (Shot ID, Slide File, Narration Text, Relative Start in Act, Relative End in Act)
ACT1_DATA = [
    (37, "slide_37.jpg", "Chapter Two: The Casino Effect. The Dopamine of Uncertainty.", 0.23, 4.50),
    (38, "slide_38.jpg", "To see this principle in action, we have to look inside a psychology laboratory from the nineteen fifties.", 4.73, 9.56),
    (39, "slide_39.jpg", "The behavioral scientist B.F. Skinner conducted a famous series of experiments with animals.", 9.87, 14.43),
    (40, "slide_40.jpg", "In the first setup, a pigeon was placed inside a box with a lever.", 14.95, 18.25),
    (41, "slide_41.jpg", "Every single time the pigeon pressed the lever, a food pellet dropped into the bowl. Press the lever, get food. Press the lever, get food.", 18.79, 25.08),
    (42, "slide_42.jpg", "What happened? The pigeon pressed the lever when it was hungry, ate its food, and then completely ignored the lever. The food was completely predictable.", 25.66, 33.54),
    (43, "slide_43.jpg", "It was reliable, safe, and boring.", 33.80, 36.54),
    (44, "slide_44.jpg", "Then, Skinner changed the rules. He introduced what psychologists call a variable-ratio schedule of reinforcement.", 36.96, 45.57),
    (45, "slide_45.jpg", "Now, when the pigeon pressed the lever, food only dropped out sometimes.", 46.08, 51.18),
    (46, "slide_46.jpg", "Sometimes it took one press. Sometimes it took five presses. Sometimes it took twelve presses with nothing, and then suddenly two pellets dropped at once. The reward was completely unpredictable.", 51.36, 61.27),
    (47, "slide_47.jpg", "What did the pigeon do? It became completely obsessed.", 61.49, 64.62),
    (48, "slide_48.jpg", "It stood in front of the lever for hours, pressing it frantically, ignoring its sleep, and ignoring other birds.", 65.09, 68.84),
    (49, "slide_49.jpg", "The unpredictability hijacked the animal's neurological reward circuitry.", 69.20, 73.80)
]

ACT2_DATA = [
    (50, "slide_50.jpg", "Modern neuroscientists now know why this happens.", 0.19, 3.32),
    (51, "slide_51.jpg", "Dopamine is not the chemical of pleasure.", 3.79, 6.09),
    (52, "slide_52.jpg", "Dopamine is the chemical of anticipation.", 6.62, 9.02),
    (53, "slide_53.jpg", "Your brain does not release its biggest spike of dopamine when you receive a prize. It releases its biggest spike of dopamine when it does not know whether a prize is coming or not.", 9.93, 19.39),
    (54, "slide_54.jpg", "This is the exact psychological mechanism behind slot machines, lottery tickets, and social media notifications.", 20.35, 26.59),
    (55, "slide_55.jpg", "When you pull the lever on a slot machine, the thrilling tension is in the spinning reels. Will three cherries align, or will you lose everything?", 27.53, 35.02),
    (56, "slide_56.jpg", "That unresolved gap between hope and fear floods your brain with dopamine.", 35.71, 40.28)
]

ACT3_DATA = [
    (57, "slide_57.jpg", "Now, bring this back to human interaction. The person who is always available operates like the first lever.", 0.20, 5.70),
    (58, "slide_58.jpg", "Text them, and they reply within thirty seconds. Compliment them, and they shower you with praise. Ask them to meet, and they immediately say yes.", 6.21, 13.57),
    (59, "slide_59.jpg", "Their behavior is a hundred percent predictable. There is no mystery. There is no tension.", 14.19, 20.92),
    (60, "slide_60.jpg", "And because there is no anticipation, there is no dopamine.", 21.31, 24.33),
    (61, "slide_61.jpg", "Their attention is comfortable, but it creates zero gravitational pull.", 24.60, 29.88),
    (62, "slide_62.jpg", "The person who is slightly aloof, however, operates like the slot machine.", 30.08, 35.51),
    (63, "slide_63.jpg", "When they look at you, it feels meaningful because they rarely look around.", 36.14, 42.59),
    (64, "slide_64.jpg", "When they pay you a compliment, it sticks in your memory for three weeks because compliments from them are virtually impossible to get.", 43.34, 48.32),
    (65, "slide_65.jpg", "When they text you back, your phone lights up and your heart skips a beat—not because the text is poetic, but because you genuinely didn't know if they would reply at all.", 48.67, 54.55),
    (66, "slide_66.jpg", "You are not necessarily falling in love with the person. You are falling in love with the chemical cocktail created by their unpredictability.", 55.02, 59.25)
]

def main():
    print("=" * 80)
    print("  🎬 RENDERING CHAPTER 02 MASTER FILM: THE CASINO EFFECT")
    print("=" * 80)

    ch02_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_02_the_casino_effect")
    ch03_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_03_the_economy_of_availability")
    slides_dir = ch02_dir / "slides"
    tts_dir = ch02_dir / "audio" / "google_tts"
    logo = Path("assets/branding/channel_logo.png")
    bgm = Path("assets/bgm/dark_contemplation.mp3")

    temp_dir = Path("temp/ch02_master_build")
    temp_dir.mkdir(parents=True, exist_ok=True)

    master_mp4 = ch02_dir / "renders" / "WHY_UNPREDICTABLE_PEOPLE_ARE_ADDICTIVE_Chapter_02_MASTER.mp4"
    central_mp4 = Path("renders/long/ep01_why_people_fall_for_who_ignores_them/WHY_UNPREDICTABLE_PEOPLE_ARE_ADDICTIVE_Chapter_02_MASTER.mp4")
    master_mp4.parent.mkdir(parents=True, exist_ok=True)
    central_mp4.parent.mkdir(parents=True, exist_ok=True)

    # 1. Measure and Concat Audio (Act 1 + Act 2 + Act 3 + Outro)
    act1_wav = tts_dir / "act1_ludo.wav"
    act2_wav = tts_dir / "act2_ludo.wav"
    act3_wav = tts_dir / "act3_ludo.wav"
    outro_wav = tts_dir / "outro_ludo.wav"

    def get_wav_dur(p):
        with wave.open(str(p), "rb") as w:
            return w.getnframes() / float(w.getframerate())

    dur_act1 = get_wav_dur(act1_wav)
    dur_act2 = get_wav_dur(act2_wav)
    dur_act3 = get_wav_dur(act3_wav)
    dur_outro = get_wav_dur(outro_wav)

    print(f"Act Durations: Act 1={dur_act1:.3f}s, Act 2={dur_act2:.3f}s, Act 3={dur_act3:.3f}s, Outro={dur_outro:.3f}s")

    # Master audio assembly
    combined_raw_wav = temp_dir / "ch02_combined_raw.wav"
    audio_concat_txt = temp_dir / "concat_audio.txt"
    with open(audio_concat_txt, "w", encoding="utf-8") as f:
        f.write(f"file '{act1_wav.resolve().as_posix()}'\n")
        f.write(f"file '{act2_wav.resolve().as_posix()}'\n")
        f.write(f"file '{act3_wav.resolve().as_posix()}'\n")
        f.write(f"file '{outro_wav.resolve().as_posix()}'\n")

    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(audio_concat_txt),
        "-c", "copy", str(combined_raw_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Master through Studio DSP (-11.9 LUFS)
    mastered_wav = temp_dir / "ch02_master_audio.wav"
    dsp_filter = (
        "highpass=f=80,"
        "equalizer=f=115:t=q:w=1.2:g=4.2,"
        "equalizer=f=250:t=q:w=1.5:g=2.0,"
        "equalizer=f=3500:t=q:w=1.0:g=2.5,"
        "acompressor=threshold=-18dB:ratio=2.5:attack=15:release=120,"
        "loudnorm=I=-11.9:TP=-1.5:LRA=7.0"
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(combined_raw_wav),
        "-af", dsp_filter,
        "-ar", "48000", str(mastered_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Build Timeline for all 31 shots
    act1_offset = 0.0
    act2_offset = dur_act1
    act3_offset = dur_act1 + dur_act2
    outro_offset = dur_act1 + dur_act2 + dur_act3

    timeline = []
    # Act 1 Shots
    for sid, slide, text, s_rel, e_rel in ACT1_DATA:
        timeline.append({
            "shot_id": sid,
            "slide_path": slides_dir / slide,
            "text": text,
            "speech_start": act1_offset + s_rel,
            "speech_end": act1_offset + e_rel
        })

    # Act 2 Shots
    for sid, slide, text, s_rel, e_rel in ACT2_DATA:
        timeline.append({
            "shot_id": sid,
            "slide_path": slides_dir / slide,
            "text": text,
            "speech_start": act2_offset + s_rel,
            "speech_end": act2_offset + e_rel
        })

    # Act 3 Shots
    for sid, slide, text, s_rel, e_rel in ACT3_DATA:
        timeline.append({
            "shot_id": sid,
            "slide_path": slides_dir / slide,
            "text": text,
            "speech_start": act3_offset + s_rel,
            "speech_end": act3_offset + e_rel
        })

    # Outro Shot 67 (Slide 67 from Chapter 3)
    slide_67_path = ch03_dir / "slides" / "slide_67.jpg"
    timeline.append({
        "shot_id": 67,
        "slide_path": slide_67_path,
        "text": "In Chapter Three, we reveal why the most powerful move in any room is having somewhere else to be: The Economy of Availability. Subscribe to Sticky in Dark.",
        "speech_start": outro_offset + 0.20,
        "speech_end": outro_offset + dur_outro - 0.20
    })

    # Calculate cut boundaries (halfway between speech ends)
    total_timeline_shots = len(timeline)
    for i in range(total_timeline_shots):
        if i == 0:
            c_start = 0.0
        else:
            prev_end = timeline[i-1]["speech_end"]
            curr_start = timeline[i]["speech_start"]
            c_start = (prev_end + curr_start) / 2.0

        if i == total_timeline_shots - 1:
            c_end = outro_offset + dur_outro + 1.50 # 1.5s visual hold at end
        else:
            curr_end = timeline[i]["speech_end"]
            next_start = timeline[i+1]["speech_start"]
            c_end = (curr_end + next_start) / 2.0

        timeline[i]["cut_start"] = c_start
        timeline[i]["cut_end"] = c_end
        timeline[i]["cut_dur"] = c_end - c_start

    total_video_dur = timeline[-1]["cut_end"]
    print(f"\nTimeline Assembled: {len(timeline)} shots across {total_video_dur:.3f}s ({int(total_video_dur//60):02d}:{total_video_dur%60:05.2f})")

    # 3. Build Concat Script for Video Slides
    video_concat_txt = temp_dir / "video_concat_ch02.txt"
    with open(video_concat_txt, "w", encoding="utf-8") as f:
        accum = 0.0
        for t in timeline:
            dur = t["cut_dur"]
            sp = t["slide_path"].resolve().as_posix()
            f.write(f"file '{sp}'\n")
            f.write(f"duration {dur:.3f}\n")
            accum += dur
        # Final repeat for concat demuxer boundary
        f.write(f"file '{timeline[-1]['slide_path'].resolve().as_posix()}'\n")

    # 4. Generate Kinetic Highlighted ASS Subtitles
    sub_file = ch02_dir / "subtitles_ch02_kinetic.ass"
    header = """[Script Info]
Title: Sticky in Dark 16:9 Kinetic Subtitles - Chapter 02
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
    for t in timeline:
        sp_start = t["speech_start"]
        sp_end = t["speech_end"]
        sp_dur = sp_end - sp_start
        words = t["text"].split()
        if not words: continue

        sub_style = "OutroWordSub" if t["shot_id"] == 67 else "ExplainerWordSub"
        w_dur = sp_dur / len(words)

        for i in range(0, len(words), chunk_size):
            chunk = words[i:i+chunk_size]
            c_start = sp_start + (i * w_dur)
            c_end = min(sp_end, sp_start + ((i + len(chunk)) * w_dur))
            for j in range(len(chunk)):
                w_start = c_start + (j * (c_end - c_start) / len(chunk))
                w_end = c_start + ((j + 1) * (c_end - c_start) / len(chunk))

                parts = []
                for k, cw in enumerate(chunk):
                    clean_w = cw.upper()
                    if k == j:
                        parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)}" + clean_w + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        parts.append(clean_w)
                events.append(f"Dialogue: 0,{format_ass(w_start)},{format_ass(w_end)},{sub_style},,0,0,0,,{' '.join(parts)}")

    with open(sub_file, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Generated {len(events)} kinetic subtitle events in {sub_file.name}")

    # 5. Render Master Video (CFR 25fps, 1080p, Ducked BGM, Subtitles, Watermark)
    print("\nRendering Master Video Deliverable via FFmpeg...")
    filter_complex = (
        "[0:v]fps=25,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_fps];"
        "[1:v]scale=110:110[logo];"
        "[v_fps][logo]overlay=1800:960[v_masked];"
        f"[v_masked]subtitles={sub_file.as_posix()}[v_out];"
        "[2:a]aresample=48000,aformat=channel_layouts=stereo[voice];"
        f"[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.08,afade=t=in:st=0:d=1.5,afade=t=out:st={total_video_dur-3.0:.2f}:d=3.0[bgm_ducked];"
        "[voice][bgm_ducked]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(video_concat_txt),
        "-loop", "1", "-i", str(logo.resolve()),
        "-i", str(mastered_wav.resolve()),
        "-stream_loop", "-1", "-i", str(bgm.resolve()),
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-t", f"{total_video_dur:.3f}",
        str(master_mp4)
    ]

    subprocess.run(cmd, check=True)
    shutil.copy2(master_mp4, central_mp4)
    print(f"\n[MASTER RENDER COMPLETE]")
    print(f"  Local Deliverable: {master_mp4} ({master_mp4.stat().st_size / (1024*1024):.2f} MB)")
    print(f"  Central Channel Copy: {central_mp4} ({central_mp4.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
