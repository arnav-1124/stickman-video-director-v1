import re
import json
import math
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
    # Acoustic split points (in seconds):
    # Each cut transitions right in the pause gap (at pause center)
    # Speech 1: 0.294 -> 5.013, pause 2: 5.013 -> 5.254 (center: 5.134)
    # Speech 2: 5.254 -> 9.173, pause 3: 9.173 -> 9.471 (center: 9.322)
    # Speech 3: 9.471 -> 11.557, pause 4: 11.557 -> 11.778 (center: 11.668)
    # Speech 4: 11.778 -> 12.519, pause 5: 12.519 -> 12.725 (center: 12.622)
    # Speech 5: 12.725 -> 17.474, pause 6: 17.474 -> 17.750 (center: 17.612)
    # Speech 6: 17.750 -> 19.337, pause 7: 19.337 -> 19.533 (center: 19.435)
    # Speech 7: 19.533 -> 24.269, pause 8: 24.269 -> 24.512 (center: 24.390)
    # Speech 8: 24.512 -> 28.741, pause 9: 28.741 -> 28.965 (center: 28.853)
    # Speech 9: 28.965 -> 31.772, pause 10: 31.772 -> 31.992 (center: 31.882)
    # Speech 10: 31.992 -> 35.256, end: 35.514

    cuts = [
        (3, 5.134),            # Cut 1: Slide 03 (0.000 to 5.134) -> dur: 5.134s
        (4, 9.322 - 5.134),    # Cut 2: Slide 04 -> dur: 4.188s
        (5, 11.668 - 9.322),   # Cut 3: Slide 05 -> dur: 2.346s
        (6, 12.622 - 11.668),  # Cut 4: Slide 06 -> dur: 0.954s
        (7, 17.612 - 12.622),  # Cut 5: Slide 07 -> dur: 4.990s
        (8, 19.435 - 17.612),  # Cut 6: Slide 08 -> dur: 1.823s
        (9, 24.390 - 19.435),  # Cut 7: Slide 09 -> dur: 4.955s
        (10, 28.853 - 24.390), # Cut 8: Slide 10 -> dur: 4.463s
        (11, 31.882 - 28.853), # Cut 9: Slide 11 -> dur: 3.029s
        (12, 35.514 - 31.882)  # Cut 10: Slide 12 -> dur: 3.632s
    ]

    slides_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/slides")
    concat_file = Path("temp/concat_038s_sync.txt")

    with open(concat_file, "w", encoding="utf-8") as f:
        for s_idx, dur in cuts:
            p = (slides_dir / f"slide_{s_idx:02d}.jpg").resolve().as_posix()
            f.write(f"file '{p}'\n")
            f.write(f"duration {dur:.3f}\n")
        # Final frame hold
        last_p = (slides_dir / "slide_12.jpg").resolve().as_posix()
        f.write(f"file '{last_p}'\n")

    print("Wrote exact concat file!")

    sentences_acoustic = [
        (0.294, 5.013, "The person who texts you back in three seconds flat."),
        (5.254, 9.173, "The person who agrees with everything you say."),
        (9.471, 11.557, "The person who rearranges their entire schedule just to see you for twenty minutes."),
        (11.778, 12.519, "On paper, they are doing everything right."),
        (12.725, 17.474, "They are kind, attentive, and consistently present."),
        (17.750, 19.337, "Yet, almost instinctively, you feel yourself pulling away."),
        (19.533, 24.269, "Their messages start to feel heavy."),
        (24.512, 28.741, "Their enthusiasm feels exhausting."),
        (28.965, 31.772, "And without even wanting to, you begin to take them for granted."),
        (31.992, 35.256, "Now, consider the opposite scenario. There is another person in your life.")
    ]

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
    for s_start, s_end, text in sentences_acoustic:
        words = text.split()
        dur = s_end - s_start
        w_dur = dur / len(words)
        chunk_size = 3
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i+chunk_size]
            c_start = s_start + (i * w_dur)
            c_end = min(s_end, s_start + ((i + len(chunk)) * w_dur))
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

    ass_path = Path("temp/subtitles_exact_038s.ass")
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Wrote {len(events)} exact acoustic subtitles!")

    # Step 3: Run FFmpeg render
    out_video = Path("sample_video_first_35s.mp4")
    raw_wav = Path("temp/ludo_calibrated_038s.wav")
    logo = Path("assets/branding/channel_logo.png")
    bgm = Path("assets/bgm/dark_contemplation.mp3")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(logo.resolve()),
        "-i", str(raw_wav.resolve()),
        "-stream_loop", "-1", "-i", str(bgm.resolve()),
        "-filter_complex", (
            "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_base];"
            "[1:v]scale=110:110[logo];"
            "[v_base][logo]overlay=1800:960[v_masked];"
            "[v_masked]subtitles=temp/subtitles_exact_038s.ass[v_out];"
            "[3:a]volume=0.08,afade=t=in:st=0:d=1.5,afade=t=out:st=33.0:d=2.5[bgm_ducked];"
            "[2:a][bgm_ducked]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
        ),
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k",
        "-t", "35.514",
        str(out_video)
    ]

    print("Rendering sample_video_first_35s.mp4 with 100% exact acoustic sync...")
    subprocess.run(cmd, check=True)
    print(f"DONE! File size: {out_video.stat().st_size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    main()
