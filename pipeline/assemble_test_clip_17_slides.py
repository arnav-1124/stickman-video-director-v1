import os
import sys
import math
import subprocess
from pathlib import Path

# Configure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path("f:/Arnav - YT/stickman-video-director")
EP_DIR = ROOT_DIR / "projects/long/ep02_how_humans_invented_the_first_lie"
SLIDES_DIR = EP_DIR / "slides"
AUDIO_DIR = EP_DIR / "audio"
RENDERS_DIR = EP_DIR / "renders"
RENDERS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Slide timeline definition matching detected speech intervals
SLIDES_DATA = [
    {
        "id": "slide_001",
        "file": "slide_001.jpg",
        "start": 0.00,
        "end": 3.90,
        "voiceover": "About two hundred thousand years ago, somewhere on the East African savanna,"
    },
    {
        "id": "slide_002_wide",
        "file": "slide_002.jpg",
        "start": 3.90,
        "end": 6.29,
        "voiceover": "an ancient human named Grog did something"
    },
    {
        "id": "slide_002_tight",
        "file": "../../scratch/slide_002_tight.jpg",
        "start": 6.29,
        "end": 9.35,
        "voiceover": "that would permanently alter the course of human evolution."
    },
    {
        "id": "slide_003",
        "file": "slide_003.jpg",
        "start": 9.35,
        "end": 11.35,
        "voiceover": "He wasn't hunting a saber-tooth tiger."
    },
    {
        "id": "slide_004",
        "file": "slide_004.jpg",
        "start": 11.35,
        "end": 12.77,
        "voiceover": "He wasn't inventing the wheel."
    },
    {
        "id": "slide_005",
        "file": "slide_005.jpg",
        "start": 12.77,
        "end": 16.00,
        "voiceover": "He had just eaten the tribe’s entire reserve of wild honey."
    },
    {
        "id": "slide_006",
        "file": "slide_006.jpg",
        "start": 16.00,
        "end": 16.70,
        "voiceover": "All of it."
    },
    {
        "id": "slide_007",
        "file": "slide_007.jpg",
        "start": 16.70,
        "end": 19.45,
        "voiceover": "And now, the tribe chief was walking around the corner."
    },
    {
        "id": "slide_008_wide",
        "file": "slide_008.jpg",
        "start": 19.45,
        "end": 21.28,
        "voiceover": "Under normal animal rules,"
    },
    {
        "id": "slide_008_tight",
        "file": "../../scratch/slide_008_tight.jpg",
        "start": 21.28,
        "end": 23.88,
        "voiceover": "Grog had two very simple biological options."
    },
    {
        "id": "slide_009",
        "file": "slide_009.jpg",
        "start": 23.88,
        "end": 26.11,
        "voiceover": "Fight the chief and get smashed with a club,"
    },
    {
        "id": "slide_010",
        "file": "slide_010.jpg",
        "start": 26.11,
        "end": 28.23,
        "voiceover": "or drop the honey and run for his life."
    },
    {
        "id": "slide_011",
        "file": "slide_011.jpg",
        "start": 28.23,
        "end": 29.50,
        "voiceover": "Both options were terrible."
    },
    {
        "id": "slide_012",
        "file": "slide_012.jpg",
        "start": 29.50,
        "end": 30.82,
        "voiceover": "Both guaranteed pain."
    },
    {
        "id": "slide_013",
        "file": "slide_013.jpg",
        "start": 30.82,
        "end": 33.95,
        "voiceover": "So Grog’s ancient brain did something unprecedented."
    },
    {
        "id": "slide_014",
        "file": "slide_014.jpg",
        "start": 33.95,
        "end": 34.97,
        "voiceover": "It didn’t run."
    },
    {
        "id": "slide_015",
        "file": "slide_015.jpg",
        "start": 34.97,
        "end": 35.89,
        "voiceover": "It didn’t fight."
    },
    {
        "id": "slide_016",
        "file": "slide_016.jpg",
        "start": 35.89,
        "end": 39.47,
        "voiceover": "Instead, it booted up a brand-new piece of mental software."
    },
    {
        "id": "slide_017_wide",
        "file": "slide_017.jpg",
        "start": 39.47,
        "end": 42.60,
        "voiceover": "Grog smeared a little honey"
    },
    {
        "id": "slide_017_tight",
        "file": "../../scratch/slide_017_tight.jpg",
        "start": 42.60,
        "end": 45.10,
        "voiceover": "on the nose"
    },
    {
        "id": "slide_017_resolve",
        "file": "slide_017.jpg",
        "start": 45.10,
        "end": 47.15,
        "voiceover": "of a sleeping hyena nearby."
    }
]

TOTAL_DURATION = SLIDES_DATA[-1]["end"]

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - math.floor(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_subtitles_ass(ass_path: Path):
    header = """[Script Info]
Title: Ink Explainer Test Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ExplainerSub,Arial Black,42,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,4.5,2.0,2,80,80,90,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for item in SLIDES_DATA:
        words = item["voiceover"].split()
        if not words:
            continue
        
        # Split words into 3-5 word chunks across the duration
        chunk_size = 4
        chunks = [words[i:i+chunk_size] for i in range(0, len(words), chunk_size)]
        total_chunks = len(chunks)
        dur = item["end"] - item["start"]
        chunk_dur = dur / total_chunks
        
        for c_idx, chunk in enumerate(chunks):
            c_start = item["start"] + c_idx * chunk_dur
            c_end = item["start"] + (c_idx + 1) * chunk_dur
            
            # Format text in upper case
            chunk_text = " ".join(chunk).upper()
            start_str = format_ass_time(c_start)
            end_str = format_ass_time(c_end)
            events.append(f"Dialogue: 0,{start_str},{end_str},ExplainerSub,,0,0,0,,{chunk_text}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        for ev in events:
            f.write(f"{ev}\n")
    print(f"✅ Generated ASS Subtitles: {ass_path}")

def build_clip():
    print(f"🎬 Building 17-Slide Video Clip ({TOTAL_DURATION:.2f}s total duration)...")
    
    # 1. Prepare audio slice
    src_audio = AUDIO_DIR / "00_prologue_the_first_lie.wav"
    out_audio = RENDERS_DIR / "temp_prologue_17_slides.wav"
    
    cmd_audio = [
        "ffmpeg", "-y",
        "-i", str(src_audio),
        "-t", f"{TOTAL_DURATION:.3f}",
        "-af", f"afade=t=out:st={TOTAL_DURATION-0.10:.3f}:d=0.10",
        str(out_audio)
    ]
    subprocess.run(cmd_audio, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"✅ Extracted trimmed voiceover audio: {out_audio.name}")

    # 2. Build subtitle file
    ass_path = RENDERS_DIR / "temp_prologue_17_slides.ass"
    generate_subtitles_ass(ass_path)

    # 3. Create concat demuxer list for slides
    concat_list_path = RENDERS_DIR / "concat_slides.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for idx, item in enumerate(SLIDES_DATA):
            slide_file = SLIDES_DIR / item["file"]
            if not slide_file.exists():
                print(f"⚠️ Warning: {slide_file.name} not found! Trying alternative names...")
                alt = SLIDES_DIR / f"{item['id']}.jpg"
                if alt.exists():
                    slide_file = alt
            
            dur = item["end"] - item["start"]
            f.write(f"file '{slide_file.resolve().as_posix()}'\n")
            f.write(f"duration {dur:.3f}\n")
        # Concat demuxer needs last file repeated with duration
        last_file = SLIDES_DIR / SLIDES_DATA[-1]["file"]
        dur_last = SLIDES_DATA[-1]["end"] - SLIDES_DATA[-1]["start"]
        f.write(f"file '{last_file.resolve().as_posix()}'\n")
        f.write(f"duration {dur_last:.3f}\n")
        f.write(f"file '{last_file.resolve().as_posix()}'\n")

    # 4. Check for background music
    bgm_path = ROOT_DIR / "assets/bgm/dark_contemplation.mp3"
    has_bgm = bgm_path.exists()
    
    out_mp4 = RENDERS_DIR / "ep02_prologue_17_slides_test.mp4"
    ass_escaped = str(ass_path.resolve()).replace('\\', '/').replace(':', r'\:')

    # Video filter chain:
    # Scale each image to 1920x1080 with high-quality lanczos, force 30fps, burn subtitles
    vf_chain = (
        f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,"
        f"fps=30,format=yuv420p,"
        f"subtitles='{ass_escaped}'"
    )

    if has_bgm:
        print(f"🎵 Mixing background music: {bgm_path.name} (-22dB ducked)...")
        # Audio filter: duck BGM to -22dB, loop it, mix with voiceover, master with loudnorm
        filter_complex = (
            f"[0:v]{vf_chain}[v_out];"
            f"[2:a]aloop=loop=-1:size=2e+09,volume=0.08[bgm];"
            f"[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2,"
            f"loudnorm=I=-11.9:TP=-1.0:LRA=7.0[a_out]"
        )
        cmd_render = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_list_path),
            "-i", str(out_audio),
            "-i", str(bgm_path),
            "-filter_complex", filter_complex,
            "-map", "[v_out]",
            "-map", "[a_out]",
            "-t", f"{TOTAL_DURATION:.3f}",
            "-c:v", "libx264",
            "-r", "30",
            "-fps_mode", "cfr",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            str(out_mp4)
        ]
    else:
        cmd_render = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(concat_list_path),
            "-i", str(out_audio),
            "-vf", vf_chain,
            "-af", "loudnorm=I=-11.9:TP=-1.0:LRA=7.0",
            "-t", f"{TOTAL_DURATION:.3f}",
            "-c:v", "libx264",
            "-r", "30",
            "-fps_mode", "cfr",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac",
            "-b:a", "192k",
            str(out_mp4)
        ]

    print("[FFmpeg] Rendering final test MP4...")
    res = subprocess.run(cmd_render, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ FFmpeg Error:\n{res.stderr}")
        sys.exit(1)

    # Check output file size and duration
    dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp4)]
    rendered_dur = float(subprocess.run(dur_cmd, capture_output=True, text=True).stdout.strip())
    size_mb = out_mp4.stat().st_size / (1024 * 1024)
    print(f"\n🎉 SUCCESS! Rendered Clip: {out_mp4.name}")
    print(f"📁 Path: {out_mp4}")
    print(f"⏱️ Duration: {rendered_dur:.2f}s")
    print(f"📦 Size: {size_mb:.2f} MB")
    print(f"🎞️ Slides included: 17 slides (Slide 001 to Slide 017)")

if __name__ == "__main__":
    build_clip()
