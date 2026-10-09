import json
import math
import re
from pathlib import Path

def format_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

ep_dir = Path("projects/sticky_in_dark/shorts/ep06_when_you_make_eye_contact_in_public")
sync_file = ep_dir / "audio" / "snapped_21_slides_sync.json"
ass_file = ep_dir / "subtitles.ass"

with open(sync_file, "r", encoding="utf-8") as f:
    sync_data = json.load(f)

header = """[Script Info]
Title: Stickman Ink Explainer Kinetic Subtitles
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

for item in sync_data:
    st = item["start_time"]
    et = item["end_time"]
    total_dur = et - st
    raw_words = item["words"].split()
    if not raw_words: continue
    
    words = [w.upper() for w in raw_words]
    n_words = len(words)
    word_dur = total_dur / n_words
    
    group_size = 3 if n_words > 4 else n_words
    for i in range(0, n_words, group_size):
        chunk_words = words[i:i+group_size]
        chunk_start = st + (i * word_dur)
        chunk_end = min(et, st + ((i + len(chunk_words)) * word_dur))
        
        for w_idx, active_word in enumerate(chunk_words):
            w_st = chunk_start + (w_idx * word_dur)
            w_et = min(chunk_end, w_st + word_dur)
            
            line_parts = []
            for other_idx, other_word in enumerate(chunk_words):
                if other_idx == w_idx:
                    tag = "{\\c&H0000D7FF&\\3c&H000A0D14&\\t(0,60,\\fscx112\\fscy112)\\t(60,120,\\fscx100\\fscy100)}"
                    untag = "{\\c&H00FFFFFF&\\3c&H000A0D14&}"
                    line_parts.append(f"{tag}{active_word}{untag}")
                else:
                    line_parts.append(other_word)
            
            line_text = " ".join(line_parts)
            events.append(f"Dialogue: 0,{format_ass(w_st)},{format_ass(w_et)},ExplainerWordSub,,0,0,0,,{line_text}")

with open(ass_file, "w", encoding="utf-8") as f:
    f.write(header + "\n".join(events) + "\n")

print(f"Generated subtitles.ass with {len(events)} kinetic dialogue events!")
