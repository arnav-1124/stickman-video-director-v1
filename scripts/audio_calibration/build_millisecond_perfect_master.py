import os
import re
import json
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

def main():
    base_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox")
    audio_dir = base_dir / "audio" / "google_tts"
    slides_dir = base_dir / "slides"
    alignment_file = Path("temp/exact_speech_alignment.json")
    
    with open(alignment_file, "r", encoding="utf-8") as f:
        align_data = json.load(f)

    # 36 shots mapped in exact narrative order
    # (shot_id, act_key, act_idx, slide_name, text)
    SHOT_MAP = [
        # Act 1 (15 shots)
        (1, "act1", 0, "slide_03.jpg", "The person who texts you back in three seconds flat."),
        (2, "act1", 1, "slide_04.jpg", "The person who agrees with everything you say."),
        (3, "act1", 2, "slide_05.jpg", "The person who rearranges their entire schedule just to see you for twenty minutes."),
        (4, "act1", 3, "slide_06.jpg", "On paper, they are doing everything right."),
        (5, "act1", 4, "slide_07.jpg", "They are kind, attentive, and consistently present."),
        (6, "act1", 5, "slide_08.jpg", "Yet, almost instinctively, you feel yourself pulling away."),
        (7, "act1", 6, "slide_09.jpg", "Their messages start to feel heavy."),
        (8, "act1", 7, "slide_10.jpg", "Their enthusiasm feels exhausting."),
        (9, "act1", 8, "slide_11.jpg", "And without even wanting to, you begin to take them for granted."),
        (10, "act1", 9, "slide_12.jpg", "Now, consider the opposite scenario."),
        (11, "act1", 10, "slide_13.jpg", "There is another person in your life."),
        (12, "act1", 11, "slide_14.jpg", "They rarely check their phone."),
        (13, "act1", 12, "slide_15.jpg", "When you ask them a question, they give a calm, brief answer."),
        (14, "act1", 13, "slide_16.jpg", "They don't jump through hoops to make you laugh."),
        (15, "act1", 14, "slide_17.jpg", "They don't laugh at jokes that aren't funny."),
        
        # Act 2 (10 shots)
        (16, "act2", 0, "slide_18.jpg", 'And when you invite them out, they might simply say: "I can\'t make it today, I have work to finish."'),
        (17, "act2", 1, "slide_19.jpg", "By all conventional logic, you should forget them."),
        (18, "act2", 2, "slide_20.jpg", "You should feel annoyed."),
        (19, "act2", 3, "slide_21.jpg", "Instead, you find yourself staring at your screen at two in the morning, wondering why they haven't replied."),
        (20, "act2", 4, "slide_22.jpg", "You replay your last conversation in your head. You wonder what they are doing, who they are with, and why you couldn't get a read on them."),
        (21, "act2", 5, "slide_02.jpg", "Why does the human mind do this?"),
        (22, "act2", 6, "slide_01.jpg", "Why do we instinctively run away from unconditional adoration, and chase after the person who seems completely indifferent to our existence?"),
        (23, "act2", 7, "slide_23.jpg", "This isn't an accident."),
        (24, "act2", 8, "slide_24.jpg", "It is not bad luck, and it is not because you are secretly attracted to toxic behavior."),
        (25, "act2", 9, "slide_25.jpg", "It is the result of deeply wired evolutionary mechanics that dictate how the human brain calculates value, status, and desire."),
        
        # Act 3 (11 shots)
        (26, "act3", 0, "slide_26.jpg", "Look at what happens when you place another human being on a pedestal."),
        (27, "act3", 1, "slide_27.jpg", "The moment you put someone above you, you are forced to look up at them."),
        (28, "act3", 2, "slide_28.jpg", "And more importantly, they are forced to look down at you."),
        (29, "act3", 3, "slide_29.jpg", "When you treat someone like a celebrity, you force them to treat you like a fan."),
        (30, "act3", 4, "slide_30.jpg", "When someone gives away their attention too cheaply, the receiving brain makes an automatic, unconscious calculation:"),
        (31, "act3", 5, "slide_31.jpg", '"If this person is offering me their complete devotion without me having to earn it, their time must not be worth very much."'),
        (32, "act3", 6, "slide_32.jpg", "It sounds brutal, but human beings rarely value what comes without cost."),
        (33, "act3", 7, "slide_33.jpg", "When water is free from the kitchen tap, nobody stops to admire its purity."),
        (34, "act3", 8, "slide_34.jpg", "When a rare mineral is buried five miles beneath solid rock, wars are fought over a single ounce."),
        (35, "act3", 9, "slide_35.jpg", "Value is never an inherent property of an object or a person."),
        (36, "act3", 10, "slide_36.jpg", "Value is created by scarcity, and the effort required to obtain it.")
    ]

    act_audio_files = {
        "act1": audio_dir / "act1_ludo.wav",
        "act2": audio_dir / "act2_ludo.wav",
        "act3": audio_dir / "act3_ludo.wav"
    }

    clips_dir = Path("temp/perfect_clips_038s")
    clips_dir.mkdir(parents=True, exist_ok=True)

    PAUSE = 0.380 # Locked standard

    print("=== Step 1: Slicing isolated sentence clips with micro-fades ===")
    shot_clips = []
    for shot_id, act_key, act_idx, slide_name, text in SHOT_MAP:
        timing = align_data[act_key][act_idx]
        st = timing["start_sec"]
        en = timing["end_sec"]
        raw_dur = en - st
        
        act_wav = act_audio_files[act_key]
        clip_wav = clips_dir / f"shot_{shot_id:02d}_{slide_name.replace('.jpg', '')}.wav"
        
        # Slice with 10ms micro-fade to prevent clicks
        cmd_slice = [
            "ffmpeg", "-y",
            "-ss", f"{st:.3f}",
            "-i", str(act_wav),
            "-t", f"{raw_dur:.3f}",
            "-af", f"afade=t=in:st=0:d=0.010,afade=t=out:st={raw_dur-0.010:.3f}:d=0.010",
            str(clip_wav)
        ]
        subprocess.run(cmd_slice, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Measure true exact duration
        actual_dur = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(clip_wav)
        ]).decode().strip())
        
        shot_clips.append({
            "shot_id": shot_id,
            "slide_name": slide_name,
            "text": text,
            "clip_wav": clip_wav,
            "speech_dur": actual_dur,
            "slide_dur": actual_dur + PAUSE
        })
        print(f"  Shot {shot_id:02d}: {slide_name} -> {actual_dur:.3f}s speech (+{PAUSE}s pause = {actual_dur+PAUSE:.3f}s)")

    # 2. Create the precise 0.380s silence buffer
    silence_wav = clips_dir / "silence_038s.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", f"{PAUSE:.3f}", str(silence_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Build speech + pause stitch list
    print("\n=== Step 2: Stitching master audio track with exact 0.380s pauses ===")
    audio_concat_txt = clips_dir / "audio_concat.txt"
    with open(audio_concat_txt, "w", encoding="utf-8") as f:
        for item in shot_clips:
            f.write(f"file '{item['clip_wav'].resolve().as_posix()}'\n")
            f.write(f"file '{silence_wav.resolve().as_posix()}'\n")

    raw_stitched_wav = clips_dir / "stitched_master_raw.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(audio_concat_txt),
        "-c", "copy", str(raw_stitched_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 4. Master audio with Deep Masculine EQ (-11.9 LUFS)
    print("\n=== Step 3: Mastering audio to -11.9 LUFS with Deep Masculine EQ ===")
    mastered_wav = base_dir / "audio" / "ch01_full_master_narration_mastered.wav"
    dsp = (
        "equalizer=f=115:width_type=o:w=1.2:g=4.2,"
        "equalizer=f=250:width_type=o:w=1.0:g=2.0,"
        "equalizer=f=3500:width_type=o:w=1.2:g=2.5,"
        "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
        "loudnorm=I=-11.9:TP=-1.0:LRA=6.0"
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_stitched_wav),
        "-af", dsp, str(mastered_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    total_audio_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(mastered_wav)
    ]).decode().strip())
    print(f"Mastered Audio Duration: {total_audio_dur:.3f}s ({int(total_audio_dur//60):02d}:{int(total_audio_dur%60):02d})")

    # Export 320k MP3
    master_mp3 = base_dir / "audio" / "ch01_master_ludo_full.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(mastered_wav),
        "-c:a", "libmp3lame", "-b:a", "320k", str(master_mp3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 5. Build 100% Mathematically Synchronized concat_master.txt
    print("\n=== Step 4: Writing 100% synchronized concat_master.txt ===")
    concat_master_txt = base_dir / "concat_master.txt"
    total_slide_dur = 0.0
    with open(concat_master_txt, "w", encoding="utf-8") as f:
        for item in shot_clips:
            slide_file = (slides_dir / item["slide_name"]).resolve().as_posix()
            dur = item["slide_dur"]
            f.write(f"file '{slide_file}'\n")
            f.write(f"duration {dur:.3f}\n")
            total_slide_dur += dur
        # Final image hold line required by FFmpeg concat demuxer
        last_slide_file = (slides_dir / shot_clips[-1]["slide_name"]).resolve().as_posix()
        f.write(f"file '{last_slide_file}'\n")
    print(f"Total Visual Slides Duration: {total_slide_dur:.3f}s (Diff from audio: {abs(total_slide_dur - total_audio_dur)*1000:.2f}ms)")

    # 6. Build 100% Mathematically Synchronized Subtitles (subtitles_16_9.ass)
    print("\n=== Step 5: Generating millisecond-exact ASS subtitles ===")
    sub_file = base_dir / "subtitles_16_9.ass"
    ass_header = """[Script Info]
Title: Sticky in Dark 16:9 Kinetic Subtitles - Master Perfect Sync
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,54,&H00FFFFFF,&H000000FF,&H000B0B0B,&H80000000,-1,0,0,0,100,100,1.0,0,1,5.5,0.0,2,80,80,95,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    dialogues = []
    timeline_cursor = 0.0
    
    # Key punchy phrases for radiant gold pop (&H0000D7FF&)
    highlight_phrases = [
        "three seconds flat", "agrees with everything", "twenty minutes",
        "everything right", "pulling away", "feel heavy", "exhausting",
        "for granted", "opposite scenario", "rarely check their phone",
        "calm, brief answer", "jump through hoops", "two in the morning",
        "haven't replied", "human mind", "indifferent", "not an accident",
        "pedestal", "look down on you", "like a fan", "too cheaply",
        "without cost", "scarcity", "mineral is buried", "Value is never",
        "Value is created"
    ]

    for item in shot_clips:
        start_t = timeline_cursor
        end_t = timeline_cursor + item["speech_dur"]
        
        text = item["text"]
        styled_text = text
        for hp in highlight_phrases:
            if hp.lower() in styled_text.lower():
                pattern = re.compile(re.escape(hp), re.IGNORECASE)
                styled_text = pattern.sub(lambda m: r"{\c&H0000D7FF&}" + m.group(0) + r"{\c&H00FFFFFF&}", styled_text)
                break
        
        dialogues.append(f"Dialogue: 0,{format_ass(start_t)},{format_ass(end_t)},Default,,0,0,0,,{styled_text}")
        
        # Advance timeline by speech + pause
        timeline_cursor += item["slide_dur"]

    with open(sub_file, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(dialogues) + "\n")
    print(f"Generated {len(dialogues)} subtitle events covering up to {timeline_cursor:.3f}s")

    # 7. Render Final Master Video with CFR 25fps
    print("\n=== Step 6: Rendering 100% Synchronized Final Master Film ===")
    logo_file = Path("assets/branding/channel_logo.png")
    bgm_file = Path("assets/bgm/dark_contemplation.mp3")
    out_master_mp4 = base_dir / "renders" / "YOU_REPLIED_INSTANTLY_Chapter_01_MASTER.mp4"
    central_master_mp4 = Path("renders/long/ep01_why_people_fall_for_who_ignores_them/YOU_REPLIED_INSTANTLY_Chapter_01_MASTER.mp4")
    out_master_mp4.parent.mkdir(parents=True, exist_ok=True)
    central_master_mp4.parent.mkdir(parents=True, exist_ok=True)

    filter_complex = (
        "[0:v]fps=25,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_fps];"
        "[1:v]scale=110:110[logo];"
        "[v_fps][logo]overlay=1800:960[v_masked];"
        f"[v_masked]subtitles={sub_file.as_posix()}[v_out];"
        f"[3:a]volume=0.08,afade=t=in:st=0:d=2.0,afade=t=out:st={total_audio_dur-3.0:.2f}:d=3.0[bgm_ducked];"
        "[2:a][bgm_ducked]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_master_txt),
        "-i", str(logo_file.resolve()),
        "-i", str(mastered_wav.resolve()),
        "-stream_loop", "-1", "-i", str(bgm_file.resolve()),
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k",
        "-t", f"{total_audio_dur:.3f}",
        str(out_master_mp4)
    ]

    subprocess.run(cmd, check=True)
    shutil.copyfile(out_master_mp4, central_master_mp4)
    print("\n[SUCCESS] Rendered Master Film with ZERO SYNC GAP:")
    print(f"  Chapter 1: {out_master_mp4} ({out_master_mp4.stat().st_size / (1024*1024):.2f} MB)")
    print(f"  Central:   {central_master_mp4} ({central_master_mp4.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
