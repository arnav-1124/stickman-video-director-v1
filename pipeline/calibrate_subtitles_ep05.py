import json
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

# Exact speech onsets and cut durations derived from 52.76s audio:
# cut_id, text, speech_start, speech_end, cut_duration
CUT_SPEECH_DATA = [
    (1, "What do you actually do when someone makes a slick joke at your expense", 0.28, 3.30, 3.35),
    (2, "in front of everyone at a friend’s house?", 3.35, 5.89, 2.85),
    (3, "Most guys freeze.", 6.55, 7.35, 1.40),
    (4, "You either laugh along nervously to keep the peace,", 7.90, 10.02, 2.65),
    (5, "or you get angry and ruin the whole vibe.", 10.52, 12.33, 2.40),
    (6, "Look, both reactions hand all your power to them.", 13.03, 15.59, 3.30),
    (7, "Fake-laughing says you accept disrespect.", 16.31, 18.29, 2.50),
    (8, "Getting angry shows they rattled you.", 18.65, 20.29, 2.30),
    (9, "Here’s what an experienced senior will tell you.", 21.21, 22.66, 2.30),
    (10, "Don’t get mad, and don’t raise your voice.", 23.50, 25.39, 2.60),
    (11, "Just look at them calmly,", 25.95, 27.14, 1.60),
    (12, "and ask with quiet curiosity:", 27.39, 29.09, 2.05),
    (13, '"Wait, I didn’t get it."', 29.53, 30.52, 1.55),
    (14, 'Something like, "What’s the joke?"', 31.15, 32.54, 2.10),
    (15, "Notice what happens next.", 33.40, 34.49, 1.85),
    (16, "The whole room goes quiet.", 35.13, 36.31, 1.85),
    (17, "Sarcasm only survives on quick laughter.", 37.03, 39.15, 2.80),
    (18, "The moment you force someone to explain their insult,", 39.74, 41.91, 2.65),
    (19, "they have to admit they were just being petty.", 42.31, 43.86, 2.10),
    (20, "They'll mumble, backpedal, and fold on the spot.", 44.52, 46.92, 3.10),
    (21, "You don’t need to fight to command respect.", 47.71, 49.21, 2.15),
    (22, "Just hold up the mirror,", 49.70, 50.67, 1.40),
    (23, "and let them dismantle themselves.", 51.01, 52.44, 1.91),
]

def generate_subtitles(output_path: Path):
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
CHUNK_OVERRIDE = {
    1: [
        ["What", "do", "you"],
        ["actually", "do", "when"],
        ["someone", "makes"],
        ["a", "slick", "joke"],
        ["at", "your", "expense"],
    ],
    2: [
        ["in", "front", "of"],
        ["everyone", "at"],
        ["a", "friend’s", "house?"],
    ],
    3: [
        ["Most", "guys", "freeze."],
    ],
    4: [
        ["You", "either", "laugh"],
        ["along", "nervously"],
        ["to", "keep", "the", "peace,"],
    ],
    5: [
        ["or", "you", "get", "angry"],
        ["and", "ruin"],
        ["the", "whole", "vibe."],
    ],
    6: [
        ["Look,", "both", "reactions"],
        ["hand", "all", "your", "power"],
        ["to", "them."],
    ],
    7: [
        ["Fake-laughing", "says"],
        ["you", "accept", "disrespect."],
    ],
    8: [
        ["Getting", "angry", "shows"],
        ["they", "rattled", "you."],
    ],
    9: [
        ["Here’s", "what", "an"],
        ["experienced", "senior"],
        ["will", "tell", "you."],
    ],
    10: [
        ["Don’t", "get", "mad,"],
        ["and", "don’t", "raise"],
        ["your", "voice."],
    ],
    11: [
        ["Just", "look", "at"],
        ["them", "calmly,"],
    ],
    12: [
        ["and", "ask", "with"],
        ["quiet", "curiosity:"],
    ],
    13: [
        ['"Wait,', "I", "didn’t"],
        ["get", 'it."'],
    ],
    14: [
        ["Something", "like,"],
        ['"What’s', "the", 'joke?"'],
    ],
    15: [
        ["Notice", "what"],
        ["happens", "next."],
    ],
    16: [
        ["The", "whole", "room"],
        ["goes", "quiet."],
    ],
    17: [
        ["Sarcasm", "only", "survives"],
        ["on", "quick", "laughter."],
    ],
    18: [
        ["The", "moment", "you", "force"],
        ["someone", "to", "explain"],
        ["their", "insult,"],
    ],
    19: [
        ["they", "have", "to", "admit"],
        ["they", "were", "just"],
        ["being", "petty."],
    ],
    20: [
        ["They'll", "mumble,", "backpedal,"],
        ["and", "fold", "on"],
        ["the", "spot."],
    ],
    21: [
        ["You", "don’t", "need", "to", "fight"],
        ["to", "command", "respect."],
    ],
    22: [
        ["Just", "hold", "up"],
        ["the", "mirror,"],
    ],
    23: [
        ["and", "let", "them"],
        ["dismantle", "themselves."],
    ],
}

def generate_subtitles(output_path: Path):
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
    # Perceptual sync delay: shifts animated highlight +0.07s so words highlight exactly on spoken vowels
    SYNC_DELAY = 0.07

    for cid, text, speech_start, speech_end, cut_dur in CUT_SPEECH_DATA:
        words = text.split()
        if not words:
            continue

        chunks = CHUNK_OVERRIDE.get(cid)
        if not chunks:
            # fallback to 3 words
            chunks = [words[i:i + 3] for i in range(0, len(words), 3)]

        total_words = sum(len(c) for c in chunks)
        total_speech_dur = max(0.4, speech_end - speech_start)
        word_dur = total_speech_dur / total_words

        word_counter = 0
        for chunk in chunks:
            chunk_word_count = len(chunk)
            chunk_start = speech_start + SYNC_DELAY + (word_counter * word_dur)
            chunk_end = chunk_start + (chunk_word_count * word_dur)

            for active_idx, active_word in enumerate(chunk):
                w_start = chunk_start + (active_idx * word_dur)
                w_end = w_start + word_dur
                start_str = format_ass_time(w_start)
                end_str = format_ass_time(w_end)

                parts = []
                for idx, w in enumerate(chunk):
                    raw_w = w.upper().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
                    if idx == active_idx:
                        # Highlight active word in Gold with subtle pop animation
                        parts.append(f"{{\\c&H0000D7FF&\\3c&H000A0D14&\\t(0,70,\\fscx110\\fscy110)\\t(70,140,\\fscx100\\fscy100)}}{raw_w}{{\\c&H00FFFFFF&\\3c&H000A0D14&}}")
                    else:
                        parts.append(raw_w)

                line_text = " ".join(parts)
                events.append(f"Dialogue: 0,{start_str},{end_str},ExplainerWordSub,,0,0,0,,{line_text}")

            word_counter += chunk_word_count

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header)
        for ev in events:
            f.write(f"{ev}\n")

    print(f"Generated {len(events)} calibrated subtitle events in {output_path.name}")

def update_manifests_and_storyboard(project_dir: Path):
    manifest_p = project_dir / "build_manifest.json"
    storyboard_p = project_dir / "storyboard.json"
    concat_p = project_dir / "concat_en_23.txt"
    script_p = project_dir / "script.txt"

    # 1. Update script.txt with "Something like"
    script_lines = [
        "What do you actually do when someone makes a slick joke at your expense in front of everyone at a friend’s house?",
        "Most guys freeze.",
        "You either laugh along nervously to keep the peace,",
        "or you get angry and ruin the whole vibe.",
        "Look, both reactions hand all your power to them.",
        "Fake-laughing says you accept disrespect.",
        "Getting angry shows they rattled you.",
        "Here’s what an experienced senior will tell you.",
        "Don’t get mad, and don’t raise your voice.",
        "Just look at them calmly, and ask with quiet curiosity:",
        '"Wait, I didn’t get it."',
        'Something like, "What’s the joke?"',
        "Notice what happens next.",
        "The whole room goes quiet.",
        "Sarcasm only survives on quick laughter.",
        "The moment you force someone to explain their insult,",
        "they have to admit they were just being petty.",
        "They'll mumble, backpedal, and fold on the spot.",
        "You don’t need to fight to command respect.",
        "Just hold up the mirror, and let them dismantle themselves."
    ]
    script_p.write_text("\n".join(script_lines) + "\n", encoding="utf-8")
    print("Updated script.txt with 'Something like'")

    # 2. Update build_manifest.json
    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest["total_duration"] = 52.76
    clips = []
    accum_dur = 0.0
    for cid, text, s_start, s_end, dur in CUT_SPEECH_DATA:
        accum_dur += dur
        clips.append({
            "cut_id": cid,
            "beat_id": cid,
            "sub_beat": "a",
            "file_path": f"slides/slide_{cid:02d}.jpg",
            "duration": dur,
            "text": text
        })
    manifest["clips"] = clips

    with open(manifest_p, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Updated build_manifest.json: total duration {accum_dur:.2f}s across {len(clips)} cuts")

    # 3. Update concat_en_23.txt
    concat_lines = []
    for c in clips:
        concat_lines.append(f"file '{c['file_path']}'")
        concat_lines.append(f"duration {c['duration']:.3f}")
    # repeat last image per concat demuxer convention
    concat_lines.append(f"file '{clips[-1]['file_path']}'")
    concat_p.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    print("Updated concat_en_23.txt")

    # 4. Update storyboard.json
    with open(storyboard_p, "r", encoding="utf-8") as f:
        sb = json.load(f)

    for i, cut in enumerate(sb.get("cuts", [])):
        if i < len(CUT_SPEECH_DATA):
            cid, text, _, _, dur = CUT_SPEECH_DATA[i]
            cut["duration"] = dur
            cut["text"] = text

    with open(storyboard_p, "w", encoding="utf-8") as f:
        json.dump(sb, f, indent=2)
    print("Updated storyboard.json")

if __name__ == "__main__":
    p_dir = Path("projects/shorts/ep05_how_to_handle_disrespect").resolve()
    generate_subtitles(p_dir / "subtitles.ass")
    update_manifests_and_storyboard(p_dir)
