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
    slides_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/slides")
    logo = Path("assets/branding/channel_logo.png")
    bgm = Path("assets/bgm/dark_contemplation.mp3")
    mastered_wav = Path("temp/calibrated_038s/ludo_038s_mastered.wav")
    
    # Target output in project root
    out_video_mp4 = Path("sample_video_038s_with_subtitles.mp4")
    # Also update sample_video_038s_perfect_sync.mp4 so both point to the perfect subtitled version
    out_video_sync_mp4 = Path("sample_video_038s_perfect_sync.mp4")
    
    temp_dir = Path("temp/calibrated_038s")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 12 calibrated segments from act1_ludo.wav
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
    
    total_master_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(mastered_wav)
    ]).decode().strip())
    print(f"Master audio duration: {total_master_dur:.2f}s")

    # Compute timeline for 0.380s pauses
    # Pause center: speech_start - 0.190s, speech_end + 0.190s
    current_time = 0.0
    timeline = []
    for i, (st, en, txt, s_idx) in enumerate(segments):
        clip_dur = en - st
        speech_start = current_time
        speech_end = speech_start + clip_dur
        
        if i == 0:
            cut_start = 0.0
        else:
            cut_start = speech_start - 0.190
            
        if i == len(segments) - 1:
            cut_end = total_master_dur
        else:
            cut_end = speech_end + 0.190
            
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
        
        current_time = speech_end + 0.380

    # Write video concat demuxer
    video_concat = temp_dir / "video_concat_038s.txt"
    with open(video_concat, "w", encoding="utf-8") as f:
        for t in timeline:
            p = (slides_dir / f"slide_{t['slide_idx']:02d}.jpg").resolve().as_posix()
            f.write(f"file '{p}'\n")
            f.write(f"duration {t['cut_dur']:.3f}\n")
        p_last = (slides_dir / f"slide_{timeline[-1]['slide_idx']:02d}.jpg").resolve().as_posix()
        f.write(f"file '{p_last}'\n")

    # Generate ASS Subtitles
    header = """[Script Info]
Title: Sticky in Dark 16:9 Kinetic Subtitles (0.38s Sync)
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
                        # Gold pop highlight on active word
                        parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)}" + clean_w + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        parts.append(clean_w)
                events.append(f"Dialogue: 0,{format_ass(w_start)},{format_ass(w_end)},ExplainerWordSub,,0,0,0,,{' '.join(parts)}")

    ass_path = temp_dir / "subtitles_exact_038s.ass"
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Generated {len(events)} ASS subtitles in {ass_path}")

    # Render video with fps=25 filter so libass renders animated subtitles smoothly on every frame!
    print("Rendering video with burned kinetic subtitles...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(video_concat),
        "-i", str(logo.resolve()),
        "-i", str(mastered_wav.resolve()),
        "-stream_loop", "-1", "-i", str(bgm.resolve()),
        "-filter_complex", (
            "[0:v]fps=25,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_fps];"
            "[1:v]scale=110:110[logo];"
            "[v_fps][logo]overlay=1800:960[v_masked];"
            f"[v_masked]subtitles=temp/calibrated_038s/subtitles_exact_038s.ass[v_out];"
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
    
    # Also write out_video_sync_mp4
    import shutil
    shutil.copyfile(out_video_mp4, out_video_sync_mp4)

    print(f"\n[DONE] Rendered {out_video_mp4} ({out_video_mp4.stat().st_size / (1024*1024):.2f} MB)")
    print(f"[DONE] Synchronized {out_video_sync_mp4}")

if __name__ == "__main__":
    main()
