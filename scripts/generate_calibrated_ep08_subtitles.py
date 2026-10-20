import json
import math
from pathlib import Path

PROJECT_DIR = Path("projects/sticky_in_dark/shorts/ep08_the_toothbrush_protocol")
BEATS_FILE = PROJECT_DIR / "audio" / "calibrated_beats_timing.json"
ASS_PATH = PROJECT_DIR / "subtitles.ass"

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - math.floor(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate():
    with open(BEATS_FILE, "r", encoding="utf-8") as f:
        beats = json.load(f)

    header = """[Script Info]
Title: Stickman Ink Explainer Kinetic Subtitles - Ep08 Ludo Voice
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ExplainerWordSub,Arial Black,58,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.5,2.0,2,60,60,400,1
Style: Default,Arial Black,58,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.0,0,1,5.0,2.0,2,60,60,400,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []

    for beat in beats:
        raw_words = beat["line"].split()
        if not raw_words:
            continue
            
        words = [w.upper().replace('"', '').replace(',', '').replace('...', '').replace('—', '') for w in raw_words]
        n_words = len(words)
        s_start = beat["start_sec"]
        s_end = beat["end_sec"]
        dur = s_end - s_start
        word_dur = dur / n_words

        chunk_size = 3 if n_words > 4 else n_words
        for i in range(0, n_words, chunk_size):
            chunk_words = words[i:i+chunk_size]
            chunk_start = s_start + (i * word_dur)
            chunk_end = min(s_end, s_start + ((i + len(chunk_words)) * word_dur))
            chunk_dur = chunk_end - chunk_start
            w_step = chunk_dur / len(chunk_words)

            for j, active_word in enumerate(chunk_words):
                w_st = chunk_start + (j * w_step)
                w_et = chunk_start + ((j + 1) * w_step)

                display_parts = []
                for k, cw in enumerate(chunk_words):
                    if k == j:
                        tag = r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,60,\fscx112\fscy112)\t(60,120,\fscx100\fscy100)}"
                        untag = r"{\c&H00FFFFFF&\3c&H000A0D14&}"
                        display_parts.append(f"{tag}{cw}{untag}")
                    else:
                        display_parts.append(cw)

                line_text = " ".join(display_parts)
                events.append(f"Dialogue: 0,{format_ass_time(w_st)},{format_ass_time(w_et)},ExplainerWordSub,,0,0,0,,{line_text}")

    with open(ASS_PATH, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    print(f"Generated calibrated subtitles with {len(events)} kinetic word events at {ASS_PATH}!")

if __name__ == "__main__":
    generate()
