import os
import subprocess
from pathlib import Path

def format_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def main():
    raw_audio = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/audio/google_tts/act1_ludo.wav")
    slides_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/slides")
    logo = Path("assets/branding/channel_logo.png")
    bgm = Path("assets/bgm/dark_contemplation.mp3")
    
    out_audio_mp3 = Path("sample_01_ludo_040s_calibrated.mp3")
    out_video_mp4 = Path("sample_video_first_35s.mp4")
    out_video_alt = Path("sample_video_040s_perfect_sync.mp4")
    
    temp_dir = Path("temp/calibrated_040s")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Precise acoustic speech intervals extracted from raw act1_ludo.wav:
    segments = [
        (0.29, 2.81, "The person who texts you back in three seconds flat.", 3),
        (3.56, 5.46, "The person who agrees with everything you say.", 4),
        (6.21, 10.10, "The person who rearranges their entire schedule just to see you for twenty minutes.", 5),
        (10.87, 12.96, "On paper, they are doing everything right.", 6),
        (13.51, 16.49, "They are kind, attentive, and consistently present.", 7),
        (17.51, 20.25, "Yet, almost instinctively, you feel yourself pulling away.", 8),
        (21.10, 22.56, "Their messages start to feel heavy.", 9),
        (23.04, 24.77, "Their enthusiasm feels exhausting.", 10),
        (25.76, 28.63, "And without even wanting to, you begin to take them for granted.", 11),
        (29.83, 31.45, "Now, consider the opposite scenario.", 12),
        (32.22, 33.71, "There is another person in your life.", 13),
        (34.44, 35.60, "They rarely check their phone.", 14)
    ]
    
    # 1. Extract each clean speech segment
    print("Step 1: Extracting clean speech clips...")
    clip_files = []
    for i, (st, en, txt, s_idx) in enumerate(segments, 1):
        dur = en - st
        c_path = temp_dir / f"clip_{i:02d}.wav"
        # Extract with micro fade-in and fade-out to prevent clicks
        cmd = [
            "ffmpeg", "-y", "-ss", f"{st:.3f}", "-i", str(raw_audio),
            "-t", f"{dur:.3f}",
            "-af", "afade=t=in:st=0:d=0.015,afade=t=out:st=" + f"{dur-0.015:.3f}" + ":d=0.015",
            str(c_path)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clip_files.append(c_path)
        
    # 2. Create 0.400s silence buffer
    silence_file = temp_dir / "silence_040s.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
        "-t", "0.400", str(silence_file)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Build stitch list with exact 0.400s pauses
    print("Step 2: Stitching speech with exact 0.400s pauses...")
    concat_list = temp_dir / "audio_concat.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        # Start with small 0.15s pre-roll silence
        f.write(f"file '{clip_files[0].resolve().as_posix()}'\n")
        for c in clip_files[1:]:
            f.write(f"file '{silence_file.resolve().as_posix()}'\n")
            f.write(f"file '{c.resolve().as_posix()}'\n")
            
    stitched_raw = temp_dir / "stitched_raw.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy", str(stitched_raw)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 4. Apply deep masculine mastering (chest resonance EQ + broadcast compression + loudnorm)
    print("Step 3: Mastering audio with deep masculine chest resonance and vocal pressure...")
    mastered_wav = temp_dir / "ludo_040s_mastered.wav"
    dsp = (
        "equalizer=f=115:width_type=o:w=1.2:g=4.2,"
        "equalizer=f=250:width_type=o:w=1.0:g=2.0,"
        "equalizer=f=3500:width_type=o:w=1.2:g=2.5,"
        "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
        "loudnorm=I=-11.9:TP=-1.0:LRA=6.0"
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(stitched_raw),
        "-af", dsp, str(mastered_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Export MP3
    subprocess.run([
        "ffmpeg", "-y", "-i", str(mastered_wav),
        "-c:a", "libmp3lame", "-b:a", "320k", str(out_audio_mp3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    total_master_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(mastered_wav)
    ]).decode().strip())
    print(f"Created {out_audio_mp3} ({total_master_dur:.2f}s)")

    # 5. Compute exact timeline for each speech and each visual cut
    # Each pause is exactly 0.400s.
    # The visual transition occurs at pause_start + 0.200s (right in the middle of the breath).
    print("Step 4: Computing exact acoustic frame timeline...")
    current_time = 0.0
    timeline = []
    for i, (st, en, txt, s_idx) in enumerate(segments):
        clip_dur = en - st
        speech_start = current_time
        speech_end = speech_start + clip_dur
        
        # Cut start and end
        if i == 0:
            cut_start = 0.0
        else:
            cut_start = speech_start - 0.200 # transition in middle of preceding pause
            
        if i == len(segments) - 1:
            cut_end = total_master_dur
        else:
            cut_end = speech_end + 0.200 # transition in middle of succeeding pause
            
        timeline.append({
            "index": i + 1,
            "text": txt,
            "slide_idx": s_idx,
            "speech_start": speech_start,
            "speech_end": speech_end,
            "speech_dur": clip_dur,
            "cut_start": cut_start,
            "cut_end": cut_end,
            "cut_dur": cut_end - cut_start
        })
        
        current_time = speech_end + 0.400 # advance past speech + 0.400s pause
        
    print(f"Timeline calculated for {len(timeline)} segments:")
    for t in timeline:
        print(f"  Cut {t['index']:02d}: Slide {t['slide_idx']:02d} ({t['cut_dur']:4.2f}s) | Speech [{t['speech_start']:5.2f}s -> {t['speech_end']:5.2f}s]: \"{t['text'][:38]}...\"")
        
    # 6. Write Concat Demuxer for Slides
    video_concat = temp_dir / "video_concat.txt"
    with open(video_concat, "w", encoding="utf-8") as f:
        for t in timeline:
            p = (slides_dir / f"slide_{t['slide_idx']:02d}.jpg").resolve().as_posix()
            f.write(f"file '{p}'\n")
            f.write(f"duration {t['cut_dur']:.3f}\n")
        # Final hold frame
        p_last = (slides_dir / f"slide_{timeline[-1]['slide_idx']:02d}.jpg").resolve().as_posix()
        f.write(f"file '{p_last}'\n")
        
    # 7. Write ASS Subtitles with 100% exact timing
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

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for t in timeline:
        words = t["text"].split()
        dur = t["speech_dur"]
        w_dur = dur / len(words)
        chunk_size = 3
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
                        parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)}" + clean_w + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        parts.append(clean_w)
                events.append(f"Dialogue: 0,{format_ass(w_start)},{format_ass(w_end)},ExplainerWordSub,,0,0,0,,{' '.join(parts)}")

    ass_path = temp_dir / "subtitles_exact_040s.ass"
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Generated {len(events)} exact acoustic subtitles in {ass_path}")

    # 8. Render Master 0.40s Synchronized Video
    print("Step 5: Rendering Master Video...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(video_concat),
        "-i", str(logo.resolve()),
        "-i", str(mastered_wav.resolve()),
        "-stream_loop", "-1", "-i", str(bgm.resolve()),
        "-filter_complex", (
            "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_base];"
            "[1:v]scale=110:110[logo];"
            "[v_base][logo]overlay=1800:960[v_masked];"
            f"[v_masked]subtitles={ass_path.as_posix()}[v_out];"
            f"[3:a]volume=0.08,afade=t=in:st=0:d=1.5,afade=t=out:st={total_master_dur-2.5:.2f}:d=2.5[bgm_ducked];"
            "[2:a][bgm_ducked]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
        ),
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k",
        "-t", f"{total_master_dur:.3f}",
        str(out_video_mp4)
    ]
    subprocess.run(cmd, check=True)
    
    # Also save copy to out_video_alt
    import shutil
    shutil.copyfile(out_video_mp4, out_video_alt)
    print(f"\n[DONE] Rendered {out_video_mp4} ({out_video_mp4.stat().st_size / (1024*1024):.2f} MB)")
    print(f"[DONE] Created audio {out_audio_mp3} ({out_audio_mp3.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
