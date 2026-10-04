import json
import math
from pathlib import Path

PROJECT_DIR = Path("projects/shorts/ep05_how_to_handle_disrespect")
AUDIO_FILE = PROJECT_DIR / "audio" / "voiceover_googleTTS.wav"
SCRIPT_FILE = PROJECT_DIR / "script.txt"
SUBTITLES_FILE = PROJECT_DIR / "subtitles.ass"

# Exact split boundaries for each sentence in Ludo's 53.36s audio:
sentence_timings = [
    (0.00, 5.73, "What do you actually do when someone makes a slick joke at your expense in front of everyone at a friend’s house?"),
    (5.73, 7.17, "Most guys freeze."),
    (7.17, 9.83, "You either laugh along nervously to keep the peace,"),
    (9.83, 12.17, "or you get angry and ruin the whole vibe."),
    (12.17, 15.51, "Look, both reactions hand all your power to them."),
    (15.51, 18.17, "Fake-laughing says you accept disrespect."),
    (18.17, 20.42, "Getting angry shows they rattled you."),
    (20.42, 23.45, "Here’s what an experienced senior will tell you."),
    (23.45, 26.11, "Don’t get mad, and don’t raise your voice."),
    (26.11, 29.68, "Just look at them calmly, and ask with quiet curiosity:"),
    (29.68, 32.20, "\"Wait, I didn’t get it. What’s the joke?\""),
    (32.20, 34.03, "Notice what happens next."),
    (34.03, 36.19, "The whole room goes quiet."),
    (36.19, 39.21, "Sarcasm only survives on quick laughter."),
    (39.21, 42.05, "The moment you force someone to explain their insult,"),
    (42.05, 44.30, "they have to admit they were just being petty."),
    (44.30, 47.27, "They'll mumble, backpedal, and fold on the spot."),
    (47.27, 50.00, "You don’t need to fight to command respect."),
    (50.00, 53.36, "Just hold up the mirror, and let them dismantle themselves.")
]

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - math.floor(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_subtitles():
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
Style: ExplainerWordSub,Arial Black,58,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.5,2.0,2,60,60,350,1
Style: Default,Arial Black,58,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.0,0,1,5.0,2.0,2,60,60,350,1

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
        
        # Group into 2-3 word chunks for kinetic display
        chunk_size = 3
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i+chunk_size]
            chunk_start = s_start + (i * word_dur)
            chunk_end = min(s_end, s_start + ((i + len(chunk_words)) * word_dur))
            
            # Sub-word kinetic highlight
            for j, w in enumerate(chunk_words):
                w_start = chunk_start + (j * (chunk_end - chunk_start) / len(chunk_words))
                w_end = chunk_start + ((j + 1) * (chunk_end - chunk_start) / len(chunk_words))
                
                # Format text with highlighted active word
                display_parts = []
                for k, cw in enumerate(chunk_words):
                    clean_w = cw.upper()
                    if k == j:
                        # Gold pop highlight
                        display_parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx110\fscy110)\t(70,140,\fscx100\fscy100)}" + clean_w + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        display_parts.append(clean_w)
                        
                line_text = " ".join(display_parts)
                events.append(f"Dialogue: 0,{format_ass_time(w_start)},{format_ass_time(w_end)},ExplainerWordSub,,0,0,0,,{line_text}")

    with open(SUBTITLES_FILE, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
        
    print(f"Generated {len(events)} kinetic subtitle events in {SUBTITLES_FILE}")

if __name__ == "__main__":
    generate_subtitles()
