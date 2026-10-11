import math
from pathlib import Path

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - math.floor(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

# Exact 20 speech intervals measured from master_voiceover.wav waveform
SPEECH_BEATS = [
    (1, "Before you scroll,", 0.18, 0.95),
    (2, "dopamine is not the pleasure chemical you think it is.", 1.04, 3.80),
    (3, "You think it makes you feel happy, but it doesn't.", 4.10, 5.58),
    (4, "If dopamine was pleasure, you would feel satisfied after scrolling for two hours.", 5.65, 10.46),
    (5, "Instead, you feel completely empty, foggy, and exhausted.", 10.59, 13.68),
    (6, "Neuroscientists proved this decades ago:", 13.83, 15.71),
    (7, "dopamine doesn't spike when you get a reward.", 15.88, 17.95),
    (8, "It spikes right before—during the anticipation.", 18.13, 20.85),
    (9, "It is not satisfaction. It is an itch.", 20.99, 22.88),
    (10, "A biological itch that whispers:", 23.26, 24.88),
    (11, "just one more video, just one more click, maybe the next one is better.", 25.04, 28.58),
    (12, "Every time you refresh, your brain floods with craving, not fulfillment.", 28.73, 31.55),
    (13, "Cheap apps hijacked this ancient hunting reflex,", 31.65, 34.40),
    (14, "turning your focus into a slot machine in your pocket.", 34.40, 36.85),
    (15, "Here’s how you take control.", 36.85, 38.77),
    (16, "Put twenty seconds of friction between you and cheap dopamine.", 38.92, 41.86),
    (17, "Put the phone in another room,", 42.02, 43.55),
    (18, "take ten deep breaths, and let the craving burn out.", 43.65, 46.37),
    (19, "Real power isn't feeding the itch every five seconds—", 46.56, 49.29),
    (20, "it's having the strength to sit in stillness the second...", 49.38, 52.05),
]

def generate():
    project_dir = Path("projects/sticky_in_dark/shorts/ep07_dopamine_is_not_what_you_think")
    ass_path = project_dir / "subtitles.ass"

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

    for sid, text, s_start, s_end in SPEECH_BEATS:
        raw_words = text.split()
        if not raw_words:
            continue

        words = [w.upper() for w in raw_words]
        n_words = len(words)
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

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    print(f"Generated calibrated subtitles with {len(events)} kinetic word events at {ass_path}!")

if __name__ == "__main__":
    generate()
