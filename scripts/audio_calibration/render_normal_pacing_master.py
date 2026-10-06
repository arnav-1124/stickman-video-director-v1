import os
import math
import subprocess
import shutil
from pathlib import Path

def format_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

# 36 visual shots with verified acoustic intervals in natural audio
# Act 1 offset: 0.000s
# Act 2 offset: 43.760s
# Act 3 offset: 43.760s + 53.406s = 97.166s

ACT1_OFFSET = 0.000
ACT2_OFFSET = 43.760
ACT3_OFFSET = 43.760 + 53.406 # 97.166s

RAW_INTERVALS = [
    # Act 1 (Shots 1 to 15)
    (1, "slide_03.jpg", "The person who texts you back in three seconds flat.", ACT1_OFFSET + 0.295, ACT1_OFFSET + 2.814),
    (2, "slide_04.jpg", "The person who agrees with everything you say.", ACT1_OFFSET + 3.556, ACT1_OFFSET + 5.457),
    (3, "slide_05.jpg", "The person who rearranges their entire schedule just to see you for twenty minutes.", ACT1_OFFSET + 6.207, ACT1_OFFSET + 10.100),
    (4, "slide_06.jpg", "On paper, they are doing everything right.", ACT1_OFFSET + 10.869, ACT1_OFFSET + 12.962),
    (5, "slide_07.jpg", "They are kind, attentive, and consistently present.", ACT1_OFFSET + 13.513, ACT1_OFFSET + 16.486),
    (6, "slide_08.jpg", "Yet, almost instinctively, you feel yourself pulling away.", ACT1_OFFSET + 17.513, ACT1_OFFSET + 20.248),
    (7, "slide_09.jpg", "Their messages start to feel heavy.", ACT1_OFFSET + 21.098, ACT1_OFFSET + 22.564),
    (8, "slide_10.jpg", "Their enthusiasm feels exhausting.", ACT1_OFFSET + 23.041, ACT1_OFFSET + 24.766),
    (9, "slide_11.jpg", "And without even wanting to, you begin to take them for granted.", ACT1_OFFSET + 25.763, ACT1_OFFSET + 28.628),
    (10, "slide_12.jpg", "Now, consider the opposite scenario.", ACT1_OFFSET + 29.828, ACT1_OFFSET + 31.448),
    (11, "slide_13.jpg", "There is another person in your life.", ACT1_OFFSET + 32.222, ACT1_OFFSET + 33.713),
    (12, "slide_14.jpg", "They rarely check their phone.", ACT1_OFFSET + 34.437, ACT1_OFFSET + 35.604),
    (13, "slide_15.jpg", "When you ask them a question, they give a calm, brief answer.", ACT1_OFFSET + 36.329, ACT1_OFFSET + 39.085),
    (14, "slide_16.jpg", "They don't jump through hoops to make you laugh.", ACT1_OFFSET + 39.872, ACT1_OFFSET + 41.444),
    (15, "slide_17.jpg", "They don't laugh at jokes that aren't funny.", ACT1_OFFSET + 42.072, ACT1_OFFSET + 43.470),

    # Act 2 (Shots 16 to 25)
    (16, "slide_18.jpg", 'And when you invite them out, they might simply say: "I can\'t make it today, I have work to finish."', ACT2_OFFSET + 0.255, ACT2_OFFSET + 5.443),
    (17, "slide_19.jpg", "By all conventional logic, you should forget them.", ACT2_OFFSET + 6.276, ACT2_OFFSET + 8.359),
    (18, "slide_20.jpg", "You should feel annoyed.", ACT2_OFFSET + 8.985, ACT2_OFFSET + 9.823),
    (19, "slide_21.jpg", "Instead, you find yourself staring at your screen at two in the morning, wondering why they haven't replied.", ACT2_OFFSET + 10.853, ACT2_OFFSET + 16.395),
    (20, "slide_22.jpg", "You replay your last conversation in your head. You wonder what they are doing, who they are with, and why you couldn't get a read on them.", ACT2_OFFSET + 17.318, ACT2_OFFSET + 24.895),
    (21, "slide_02.jpg", "Why does the human mind do this?", ACT2_OFFSET + 26.126, ACT2_OFFSET + 27.900),
    (22, "slide_01.jpg", "Why do we instinctively run away from unconditional adoration, and chase after the person who seems completely indifferent to our existence?", ACT2_OFFSET + 28.601, ACT2_OFFSET + 36.609),
    (23, "slide_23.jpg", "This isn't an accident.", ACT2_OFFSET + 37.596, ACT2_OFFSET + 38.581),
    (24, "slide_24.jpg", "It is not bad luck, and it is not because you are secretly attracted to toxic behavior.", ACT2_OFFSET + 39.109, ACT2_OFFSET + 43.890),
    (25, "slide_25.jpg", "It is the result of deeply wired evolutionary mechanics that dictate how the human brain calculates value, status, and desire.", ACT2_OFFSET + 44.566, ACT2_OFFSET + 52.951),

    # Act 3 (Shots 26 to 36)
    (26, "slide_26.jpg", "Look at what happens when you place another human being on a pedestal.", ACT3_OFFSET + 0.299, ACT3_OFFSET + 4.019),
    (27, "slide_27.jpg", "The moment you put someone above you, you are forced to look up at them.", ACT3_OFFSET + 5.040, ACT3_OFFSET + 8.375),
    (28, "slide_28.jpg", "And more importantly, they are forced to look down at you.", ACT3_OFFSET + 9.196, ACT3_OFFSET + 11.682),
    (29, "slide_29.jpg", "When you treat someone like a celebrity, you force them to treat you like a fan.", ACT3_OFFSET + 12.772, ACT3_OFFSET + 16.547),
    (30, "slide_30.jpg", "When someone gives away their attention too cheaply, the receiving brain makes an automatic, unconscious calculation:", ACT3_OFFSET + 17.645, ACT3_OFFSET + 24.181),
    (31, "slide_31.jpg", '"If this person is offering me their complete devotion without me having to earn it, their time must not be worth very much."', ACT3_OFFSET + 24.946, ACT3_OFFSET + 31.043),
    (32, "slide_32.jpg", "It sounds brutal, but human beings rarely value what comes without cost.", ACT3_OFFSET + 32.110, ACT3_OFFSET + 35.872),
    (33, "slide_33.jpg", "When water is free from the kitchen tap, nobody stops to admire its purity.", ACT3_OFFSET + 36.702, ACT3_OFFSET + 40.473),
    (34, "slide_34.jpg", "When a rare mineral is buried five miles beneath solid rock, wars are fought over a single ounce.", ACT3_OFFSET + 41.337, ACT3_OFFSET + 47.081),
    (35, "slide_35.jpg", "Value is never an inherent property of an object or a person.", ACT3_OFFSET + 48.149, ACT3_OFFSET + 51.470),
    (36, "slide_36.jpg", "Value is created by scarcity, and the effort required to obtain it.", ACT3_OFFSET + 52.316, ACT3_OFFSET + 56.060)
]

def main():
    base_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox")
    slides_dir = base_dir / "slides"
    audio_dir = base_dir / "audio" / "google_tts"
    logo = Path("assets/branding/channel_logo.png")
    bgm = Path("assets/bgm/dark_contemplation.mp3")
    
    out_master_mp4 = base_dir / "renders" / "YOU_REPLIED_INSTANTLY_Chapter_01_MASTER.mp4"
    central_master_mp4 = Path("renders/long/ep01_why_people_fall_for_who_ignores_them/YOU_REPLIED_INSTANTLY_Chapter_01_MASTER.mp4")
    out_master_mp4.parent.mkdir(parents=True, exist_ok=True)
    central_master_mp4.parent.mkdir(parents=True, exist_ok=True)

    # 1. Master Audio: Unbroken natural narration with Deep Masculine EQ
    raw_master_wav = audio_dir / "master_narration_ludo.wav"
    total_audio_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(raw_master_wav)
    ]).decode().strip())
    print(f"Master Raw Narration Duration: {total_audio_dur:.3f}s (Natural Cadence, Zero Artificial Cuts)")

    mastered_wav = base_dir / "audio" / "ch01_full_master_narration_mastered.wav"
    print("\nMastering natural audio track with Deep Masculine EQ & Loudnorm (-11.9 LUFS)...")
    dsp = (
        "equalizer=f=115:width_type=o:w=1.2:g=4.2,"
        "equalizer=f=250:width_type=o:w=1.0:g=2.0,"
        "equalizer=f=3500:width_type=o:w=1.2:g=2.5,"
        "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
        "loudnorm=I=-11.9:TP=-1.0:LRA=6.0,"
        "aresample=48000"
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_master_wav),
        "-af", dsp, str(mastered_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Export high-bitrate MP3
    master_mp3 = base_dir / "audio" / "ch01_master_ludo_full.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(mastered_wav),
        "-c:a", "libmp3lame", "-b:a", "320k", str(master_mp3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Build Slide Cut Timings: Visual cuts happen right in the center of natural pauses
    print("\nCalculating visual slide transition boundaries...")
    timeline = []
    for i, (shot_id, slide_name, text, sp_start, sp_end) in enumerate(RAW_INTERVALS):
        # Cut start
        if i == 0:
            c_start = 0.0
        else:
            prev_end = RAW_INTERVALS[i-1][4]
            c_start = round((prev_end + sp_start) / 2.0, 3)
            
        # Cut end
        if i == len(RAW_INTERVALS) - 1:
            c_end = total_audio_dur
        else:
            next_start = RAW_INTERVALS[i+1][3]
            c_end = round((sp_end + next_start) / 2.0, 3)

        timeline.append({
            "shot_id": shot_id,
            "slide_name": slide_name,
            "text": text,
            "speech_start": sp_start,
            "speech_end": sp_end,
            "cut_start": c_start,
            "cut_end": c_end,
            "cut_dur": round(c_end - c_start, 3)
        })

    # Correct boundary alignment so each cut_start matches previous cut_end
    for i in range(1, len(timeline)):
        timeline[i]["cut_start"] = timeline[i-1]["cut_end"]
        timeline[i]["cut_dur"] = round(timeline[i]["cut_end"] - timeline[i]["cut_start"], 3)

    # Write video concat script
    temp_dir = Path("temp/normal_pacing")
    temp_dir.mkdir(parents=True, exist_ok=True)
    video_concat = temp_dir / "video_concat.txt"
    with open(video_concat, "w", encoding="utf-8") as f:
        for t in timeline:
            slide_path = slides_dir / t["slide_name"]
            f.write(f"file '{slide_path.resolve().as_posix()}'\n")
            f.write(f"duration {t['cut_dur']:.3f}\n")
        # Final image repeat for ffmpeg concat bug prevention
        last_slide = slides_dir / timeline[-1]["slide_name"]
        f.write(f"file '{last_slide.resolve().as_posix()}'\n")

    # 3. Generate Kinetic ASS Subtitles
    print("\nGenerating kinetic subtitles with word-by-word bouncing gold highlight...")
    sub_file = base_dir / "subtitles_16_9.ass"
    header = """[Script Info]
Title: Sticky in Dark 16:9 Kinetic Subtitles - Normal Pacing
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
    chunk_size = 4
    for t in timeline:
        sp_start = t["speech_start"]
        sp_end = t["speech_end"]
        sp_dur = sp_end - sp_start
        words = t["text"].split()
        if not words: continue
        
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
                        # Gold pop highlight on active word with bounce scale!
                        parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)}" + clean_w + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        parts.append(clean_w)
                events.append(f"Dialogue: 0,{format_ass(w_start)},{format_ass(w_end)},ExplainerWordSub,,0,0,0,,{' '.join(parts)}")

    with open(sub_file, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Generated {len(events)} animated word-level subtitle events in {sub_file.name}")

    # 4. Render Final Master Video (CFR 25fps) with Broadcast Stereo AAC Audio
    print("\nRendering Final Master Video with Broadcast Stereo AAC (48kHz, 320k) at Normal Pacing...")
    filter_complex = (
        "[0:v]fps=25,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_fps];"
        "[1:v]scale=110:110[logo];"
        "[v_fps][logo]overlay=1800:960[v_masked];"
        f"[v_masked]subtitles={sub_file.as_posix()}[v_out];"
        "[2:a]aresample=48000,aformat=channel_layouts=stereo[voice];"
        f"[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.08,afade=t=in:st=0:d=1.5,afade=t=out:st={total_audio_dur-2.5:.2f}:d=2.5[bgm_ducked];"
        "[voice][bgm_ducked]amix=inputs=2:duration=first:weights=1.0 1.0[a_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(video_concat),
        "-i", str(logo.resolve()),
        "-i", str(mastered_wav.resolve()),
        "-stream_loop", "-1", "-i", str(bgm.resolve()),
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
        "-t", f"{total_audio_dur:.3f}",
        str(out_master_mp4)
    ]

    subprocess.run(cmd, check=True)
    shutil.copyfile(out_master_mp4, central_master_mp4)
    print("\n[SUCCESS] Rendered Final Master Film at Normal Pacing:")
    print(f"  Chapter 1: {out_master_mp4} ({out_master_mp4.stat().st_size / (1024*1024):.2f} MB)")
    print(f"  Central:   {central_master_mp4} ({central_master_mp4.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
