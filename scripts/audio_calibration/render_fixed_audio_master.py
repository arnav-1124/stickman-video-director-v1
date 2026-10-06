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

SHOTS = [
    (1, "slide_03.jpg", "The person who texts you back in three seconds flat."),
    (2, "slide_04.jpg", "The person who agrees with everything you say."),
    (3, "slide_05.jpg", "The person who rearranges their entire schedule just to see you for twenty minutes."),
    (4, "slide_06.jpg", "On paper, they are doing everything right."),
    (5, "slide_07.jpg", "They are kind, attentive, and consistently present."),
    (6, "slide_08.jpg", "Yet, almost instinctively, you feel yourself pulling away."),
    (7, "slide_09.jpg", "Their messages start to feel heavy."),
    (8, "slide_10.jpg", "Their enthusiasm feels exhausting."),
    (9, "slide_11.jpg", "And without even wanting to, you begin to take them for granted."),
    (10, "slide_12.jpg", "Now, consider the opposite scenario."),
    (11, "slide_13.jpg", "There is another person in your life."),
    (12, "slide_14.jpg", "They rarely check their phone."),
    (13, "slide_15.jpg", "When you ask them a question, they give a calm, brief answer."),
    (14, "slide_16.jpg", "They don't jump through hoops to make you laugh."),
    (15, "slide_17.jpg", "They don't laugh at jokes that aren't funny."),
    (16, "slide_18.jpg", 'And when you invite them out, they might simply say: "I can\'t make it today, I have work to finish."'),
    (17, "slide_19.jpg", "By all conventional logic, you should forget them."),
    (18, "slide_20.jpg", "You should feel annoyed."),
    (19, "slide_21.jpg", "Instead, you find yourself staring at your screen at two in the morning, wondering why they haven't replied."),
    (20, "slide_22.jpg", "You replay your last conversation in your head. You wonder what they are doing, who they are with, and why you couldn't get a read on them."),
    (21, "slide_02.jpg", "Why does the human mind do this?"),
    (22, "slide_01.jpg", "Why do we instinctively run away from unconditional adoration, and chase after the person who seems completely indifferent to our existence?"),
    (23, "slide_23.jpg", "This isn't an accident."),
    (24, "slide_24.jpg", "It is not bad luck, and it is not because you are secretly attracted to toxic behavior."),
    (25, "slide_25.jpg", "It is the result of deeply wired evolutionary mechanics that dictate how the human brain calculates value, status, and desire."),
    (26, "slide_26.jpg", "Look at what happens when you place another human being on a pedestal."),
    (27, "slide_27.jpg", "The moment you put someone above you, you are forced to look up at them."),
    (28, "slide_28.jpg", "And more importantly, they are forced to look down at you."),
    (29, "slide_29.jpg", "When you treat someone like a celebrity, you force them to treat you like a fan."),
    (30, "slide_30.jpg", "When someone gives away their attention too cheaply, the receiving brain makes an automatic, unconscious calculation:"),
    (31, "slide_31.jpg", '"If this person is offering me their complete devotion without me having to earn it, their time must not be worth very much."'),
    (32, "slide_32.jpg", "It sounds brutal, but human beings rarely value what comes without cost."),
    (33, "slide_33.jpg", "When water is free from the kitchen tap, nobody stops to admire its purity."),
    (34, "slide_34.jpg", "When a rare mineral is buried five miles beneath solid rock, wars are fought over a single ounce."),
    (35, "slide_35.jpg", "Value is never an inherent property of an object or a person."),
    (36, "slide_36.jpg", "Value is created by scarcity, and the effort required to obtain it.")
]

def main():
    base_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox")
    slides_dir = base_dir / "slides"
    raw_clips_dir = Path("temp/perfect_clips_038s")
    tight_clips_dir = Path("temp/tight_clips_clean")
    tight_clips_dir.mkdir(parents=True, exist_ok=True)
    
    logo = Path("assets/branding/channel_logo.png")
    bgm = Path("assets/bgm/dark_contemplation.mp3")
    
    out_master_mp4 = base_dir / "renders" / "YOU_REPLIED_INSTANTLY_Chapter_01_MASTER.mp4"
    central_master_mp4 = Path("renders/long/ep01_why_people_fall_for_who_ignores_them/YOU_REPLIED_INSTANTLY_Chapter_01_MASTER.mp4")
    out_master_mp4.parent.mkdir(parents=True, exist_ok=True)
    central_master_mp4.parent.mkdir(parents=True, exist_ok=True)

    PAUSE = 0.380 # EXACT locked standard

    # 1. Cleanly trim leading and trailing silence without the buggy st=0 fade
    print("Step 1: Trimming silence cleanly with 100% full audio volume...")
    clips_data = []
    for idx, slide_name, text in SHOTS:
        pattern = f"shot_{idx:02d}_*.wav"
        matching = list(raw_clips_dir.glob(pattern))
        if not matching:
            raise FileNotFoundError(f"Missing raw clip for shot {idx}: {pattern}")
        raw_clip = matching[0]
        tight_clip = tight_clips_dir / f"shot_{idx:02d}_{slide_name.replace('.jpg', '')}.wav"
        
        # Double silenceremove (forward and reverse) without any fade bug
        cmd_trim = [
            "ffmpeg", "-y", "-i", str(raw_clip),
            "-af", (
                "silenceremove=start_periods=1:start_duration=0.01:start_threshold=-35dB,"
                "areverse,"
                "silenceremove=start_periods=1:start_duration=0.01:start_threshold=-35dB,"
                "areverse"
            ),
            str(tight_clip)
        ]
        subprocess.run(cmd_trim, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        dur = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(tight_clip)
        ]).decode().strip())
        
        clips_data.append({
            "idx": idx,
            "slide_name": slide_name,
            "text": text,
            "clip_wav": tight_clip,
            "speech_dur": dur
        })
        print(f"  Shot {idx:02d}: {slide_name} -> {dur:.3f}s speech")

    # Verify Shot 01 volume
    cmd_vol = ["ffmpeg", "-i", str(clips_data[0]["clip_wav"]), "-af", "volumedetect", "-f", "null", "-"]
    res_vol = subprocess.run(cmd_vol, capture_output=True, text=True)
    for l in res_vol.stderr.splitlines():
        if "max_volume" in l or "mean_volume" in l:
            print(f"  [Volume Check Shot 01] {l}")

    # 2. Create the exact 0.380s silence buffer (matching sample rate 24000)
    silence_wav = tight_clips_dir / "silence_038s.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", f"{PAUSE:.3f}", str(silence_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Stitch master audio
    print("\nStep 2: Stitching master audio track...")
    audio_concat = tight_clips_dir / "audio_concat.txt"
    with open(audio_concat, "w", encoding="utf-8") as f:
        for c in clips_data:
            f.write(f"file '{c['clip_wav'].resolve().as_posix()}'\n")
            f.write(f"file '{silence_wav.resolve().as_posix()}'\n")

    raw_stitched = tight_clips_dir / "raw_stitched.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(audio_concat),
        "-c", "copy", str(raw_stitched)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 4. Master audio with Deep Masculine EQ and loudnorm to -11.9 LUFS
    print("\nStep 3: Mastering audio to -11.9 LUFS with Deep Masculine EQ...")
    mastered_wav = base_dir / "audio" / "ch01_full_master_narration_mastered.wav"
    dsp = (
        "equalizer=f=115:width_type=o:w=1.2:g=4.2,"
        "equalizer=f=250:width_type=o:w=1.0:g=2.0,"
        "equalizer=f=3500:width_type=o:w=1.2:g=2.5,"
        "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
        "loudnorm=I=-11.9:TP=-1.0:LRA=6.0,"
        "aresample=48000"
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_stitched),
        "-af", dsp, str(mastered_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_audio_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(mastered_wav)
    ]).decode().strip())
    print(f"Master Audio Duration: {total_audio_dur:.3f}s ({int(total_audio_dur//60):02d}:{int(total_audio_dur%60):02d})")

    # Volume check on mastered audio
    cmd_vol_m = ["ffmpeg", "-i", str(mastered_wav), "-af", "volumedetect", "-f", "null", "-"]
    res_vol_m = subprocess.run(cmd_vol_m, capture_output=True, text=True)
    for l in res_vol_m.stderr.splitlines():
        if "max_volume" in l or "mean_volume" in l:
            print(f"  [Master Volume Check] {l}")

    # Export high-bitrate MP3
    master_mp3 = base_dir / "audio" / "ch01_master_ludo_full.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(mastered_wav),
        "-c:a", "libmp3lame", "-b:a", "320k", str(master_mp3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 5. Build timeline with EXACT pause center cuts (speech_end + 0.190s)
    print("\nStep 4: Computing timeline and slide transitions...")
    timeline = []
    current_time = 0.0
    for i, c in enumerate(clips_data):
        speech_start = current_time
        speech_end = speech_start + c["speech_dur"]
        
        if i == 0:
            cut_start = 0.0
        else:
            cut_start = speech_start - 0.190
            
        if i == len(clips_data) - 1:
            cut_end = total_audio_dur
        else:
            cut_end = speech_end + 0.190
            
        timeline.append({
            "idx": c["idx"],
            "slide_name": c["slide_name"],
            "text": c["text"],
            "speech_start": speech_start,
            "speech_end": speech_end,
            "speech_dur": c["speech_dur"],
            "cut_start": cut_start,
            "cut_end": cut_end,
            "cut_dur": cut_end - cut_start
        })
        current_time = speech_end + PAUSE

    # Write video concat demuxer
    video_concat = base_dir / "concat_master.txt"
    total_slide_dur = 0.0
    with open(video_concat, "w", encoding="utf-8") as f:
        for t in timeline:
            p = (slides_dir / t["slide_name"]).resolve().as_posix()
            f.write(f"file '{p}'\n")
            f.write(f"duration {t['cut_dur']:.3f}\n")
            total_slide_dur += t["cut_dur"]
        p_last = (slides_dir / timeline[-1]["slide_name"]).resolve().as_posix()
        f.write(f"file '{p_last}'\n")
    print(f"Total Visual Slides Duration: {total_slide_dur:.3f}s (Diff from audio: {abs(total_slide_dur - total_audio_dur)*1000:.2f}ms)")

    # 6. Generate Kinetic Animated Word-by-Word ASS Subtitles
    print("\nStep 5: Generating KINETIC ANIMATED Word-by-Word ASS subtitles...")
    sub_file = base_dir / "subtitles_16_9.ass"
    header = """[Script Info]
Title: Sticky in Dark 16:9 Kinetic Animated Subtitles (Exact 0.38s Sync)
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ExplainerWordSub,Arial Black,54,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.5,2.0,2,80,80,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    chunk_size = 3
    for t in timeline:
        words = t["text"].split()
        dur = t["speech_dur"]
        w_dur = dur / len(words)
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i+chunk_size]
            c_start = t["speech_start"] + (i * w_dur)
            c_end = min(t["speech_end"], t["speech_start"] + ((i + len(chunk)) * w_dur))
            for j, w in enumerate(chunk):
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

    # 7. Render Final Master Video (CFR 25fps) with Broadcast Stereo AAC Audio
    print("\nStep 6: Rendering Final Master Video with Broadcast Stereo AAC (48kHz, 320k)...")
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
    print("\n[SUCCESS] Rendered Final Master Film with FULL LOUD STEREO AUDIO:")
    print(f"  Chapter 1: {out_master_mp4} ({out_master_mp4.stat().st_size / (1024*1024):.2f} MB)")
    print(f"  Central:   {central_master_mp4} ({central_master_mp4.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
