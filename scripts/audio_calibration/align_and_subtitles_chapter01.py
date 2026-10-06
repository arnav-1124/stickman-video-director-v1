import json
import math
import re
import subprocess
from pathlib import Path

CHAPTER_DIR = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox")
AUDIO_FILE = CHAPTER_DIR / "audio" / "google_tts" / "master_narration_ludo.wav"
SCRIPT_FILE = CHAPTER_DIR / "script_upgraded.txt"
SUBTITLES_FILE = CHAPTER_DIR / "subtitles_16_9.ass"
CONCAT_FILE = CHAPTER_DIR / "concat_slides.txt"

def get_audio_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]
    return float(subprocess.check_output(cmd).decode().strip())

def get_silence_intervals(audio_path):
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", "silencedetect=noise=-30dB:d=0.25",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, check=True)
    lines = res.stderr.splitlines()
    
    silences = []
    for line in lines:
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([0-9.]+)", line)
            if m:
                s_start = float(m.group(1))
        elif "silence_end:" in line:
            m = re.search(r"silence_end:\s*([0-9.]+)", line)
            if m:
                s_end = float(m.group(1))
                silences.append((s_start, s_end))
    return silences

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - math.floor(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_ass(sentence_timings, output_path):
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
Style: ExplainerWordSub,Arial Black,50,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.0,2.0,2,80,80,110,1
Style: Default,Arial Black,50,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.0,0,1,5.0,2.0,2,80,80,110,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for s_start, s_end, text in sentence_timings:
        words = text.split()
        if not words:
            continue
        dur = s_end - s_start
        word_dur = dur / len(words)
        
        # 3-word kinetic bursts
        chunk_size = 3
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i+chunk_size]
            chunk_start = s_start + (i * word_dur)
            chunk_end = min(s_end, s_start + ((i + len(chunk_words)) * word_dur))
            
            for j, w in enumerate(chunk_words):
                w_start = chunk_start + (j * (chunk_end - chunk_start) / len(chunk_words))
                w_end = chunk_start + ((j + 1) * (chunk_end - chunk_start) / len(chunk_words))
                
                display_parts = []
                for k, cw in enumerate(chunk_words):
                    clean_w = cw.upper()
                    if k == j:
                        # Golden amber pop highlight
                        display_parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)}" + clean_w + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        display_parts.append(clean_w)
                        
                line_text = " ".join(display_parts)
                events.append(f"Dialogue: 0,{format_ass_time(w_start)},{format_ass_time(w_end)},ExplainerWordSub,,0,0,0,,{line_text}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Generated {len(events)} kinetic subtitle events -> {output_path}")

def main():
    if not AUDIO_FILE.exists():
        print(f"Audio file {AUDIO_FILE} does not exist yet.")
        return
        
    total_dur = get_audio_duration(AUDIO_FILE)
    print(f"Master Audio Duration: {total_dur:.2f}s")
    
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
        
    print(f"Loaded {len(lines)} script sentences.")
    
    # Calculate proportional durations based on word lengths
    total_words = sum(len(l.split()) for l in lines)
    sentence_timings = []
    cur_t = 0.0
    for l in lines:
        w_cnt = len(l.split())
        line_dur = (w_cnt / total_words) * total_dur
        end_t = min(total_dur, cur_t + line_dur)
        sentence_timings.append((round(cur_t, 3), round(end_t, 3), l))
        cur_t = end_t
        
    generate_ass(sentence_timings, SUBTITLES_FILE)
    print(f"[OK] Subtitle generation complete!")

if __name__ == "__main__":
    main()
