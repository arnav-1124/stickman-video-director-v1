import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import argparse
import json
import math
import os
import sys
from pathlib import Path

# SubStation Alpha (.ass) template optimized for Stickman / Ink Explainer
def get_ass_header(is_vertical=True, style_choice="gold"):
    res_x = 1080 if is_vertical else 1920
    res_y = 1920 if is_vertical else 1080
    font_size = 56 if is_vertical else 44
    margin_v = 350 if is_vertical else 85  # Safe zone: sits cleanly in open lower third above YouTube Shorts UI

    # Gold active word with thick black outline (universally legible on paper or dark backgrounds)
    primary_color = "&H00FFFFFF&"
    secondary_color = "&H0000D7FF&"  # Vivid Gold/Amber
    outline_color = "&H000A0D14&"
    back_color = "&HA0000000&"
    
    header = f"""[Script Info]
Title: Stickman Ink Explainer Kinetic Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: {res_x}
PlayResY: {res_y}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ExplainerWordSub,Arial Black,{font_size},{primary_color},{secondary_color},{outline_color},{back_color},-1,0,0,0,100,100,1.2,0,1,5.0,2.0,2,60,60,{margin_v},1
Style: Default,Arial Black,{font_size},{primary_color},{secondary_color},{outline_color},{back_color},-1,0,0,0,100,100,1.0,0,1,4.5,2.0,2,60,60,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    return header

def format_ass_time(seconds):
    """Converts seconds into ASS timestamp format: H:MM:SS.cc"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - math.floor(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def split_into_short_chunks(text, max_words=3):
    """Splits text into short 2-3 word phrases for high-retention kinetic pacing."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i+max_words])
        chunks.append(chunk)
    return chunks

def build_subtitles_from_words(words_list, output_ass_path, is_vertical=True, chunk_size=3):
    """Generates word-level active highlighted karaoke subtitles from a flat word timestamp array."""
    events = []
    for i in range(0, len(words_list), chunk_size):
        chunk = words_list[i:i + chunk_size]
        chunk_start = chunk[0].get("start_sec", 0.0)
        chunk_end = chunk[-1].get("end_sec", chunk_start + 1.0)
        if i + chunk_size < len(words_list):
            next_start = words_list[i + chunk_size].get("start_sec", chunk_end)
            if next_start > chunk_start:
                chunk_end = min(chunk_end, next_start)
        
        for active_idx, target_word in enumerate(chunk):
            w_start = target_word.get("start_sec", chunk_start)
            if active_idx < len(chunk) - 1:
                w_end = chunk[active_idx + 1].get("start_sec", chunk_end)
            else:
                w_end = chunk_end
                
            w_end = min(w_end, chunk_end)
            if w_end <= w_start:
                w_end = w_start + 0.08
                
            start_str = format_ass_time(w_start)
            end_str = format_ass_time(w_end)
            
            parts = []
            for idx, w in enumerate(chunk):
                raw_word = w.get("word", "").upper()
                if idx == active_idx:
                    # Highlight active word in Gold with subtle pop scale
                    parts.append(f"{{\\c&H0000D7FF&\\3c&H000A0D14&\\t(0,70,\\fscx108\\fscy108)\\t(70,140,\\fscx100\\fscy100)}}{raw_word}{{\\c&H00FFFFFF&\\3c&H000A0D14&}}")
                else:
                    parts.append(f"{raw_word}")
                    
            line_text = " ".join(parts)
            events.append(f"Dialogue: 0,{start_str},{end_str},ExplainerWordSub,,0,0,0,,{line_text}")

    with open(output_ass_path, 'w', encoding='utf-8') as f:
        f.write(get_ass_header(is_vertical=is_vertical))
        for ev in events:
            f.write(f"{ev}\n")
            
    print(f"[SUBTITLES] Generated kinetic ASS subtitles at: {output_ass_path}")
    return output_ass_path

def build_subtitles(project_dir, aspect="9:16"):
    """
    Builds .ass subtitles from dialogue_timings.json, shot word files, or storyboard.json.
    """
    project_dir = Path(project_dir).resolve()
    is_vertical = (aspect == "9:16")
    output_ass_path = project_dir / ("subtitles.ass" if is_vertical else "subtitles_16x9.ass")
    timings_path = project_dir / "audio" / "dialogue_timings.json"
    single_words_path = project_dir / "audio" / "word_timestamps.json"
    storyboard_path = project_dir / "storyboard.json"

    # Strategy 0: Check for master word_timestamps.json in audio/
    if single_words_path.exists():
        with open(single_words_path, 'r', encoding='utf-8') as f:
            words_data = json.load(f)
        if words_data and isinstance(words_data, list):
            print(f"[SUBTITLES] Using master word timestamps from {single_words_path.name} ({len(words_data)} words)")
            return build_subtitles_from_words(words_data, output_ass_path, is_vertical=is_vertical)

    # Strategy 1: Check for dialogue_timings.json with word boundaries
    if timings_path.exists():
        with open(timings_path, 'r', encoding='utf-8') as f:
            timings = json.load(f)
            
        all_words = []
        for item in timings:
            item_offset = item.get("start_time", 0.0)
            if "words" in item and item["words"]:
                for w in item["words"]:
                    all_words.append({
                        "word": w.get("word", ""),
                        "start_sec": item_offset + w.get("start_sec", 0.0),
                        "end_sec": item_offset + w.get("end_sec", 0.0)
                    })
            else:
                # Approximate word timings if word list not explicit
                text = item.get("text", "")
                words = text.split()
                dur = item.get("duration", 2.0)
                step = dur / max(1, len(words))
                for w_idx, w in enumerate(words):
                    w_s = item_offset + (w_idx * step)
                    w_e = w_s + step
                    all_words.append({"word": w, "start_sec": w_s, "end_sec": w_e})

        if all_words:
            return build_subtitles_from_words(all_words, output_ass_path, is_vertical=is_vertical)

    # Strategy 2: Check for individual shot word json files in audio/
    audio_dir = project_dir / "audio"
    word_files = sorted(audio_dir.glob("shot_*_words.json"))
    if word_files:
        all_words = []
        curr_time = 0.0
        for wf in word_files:
            with open(wf, 'r', encoding='utf-8') as f:
                shot_words = json.load(f)
            for w in shot_words:
                all_words.append({
                    "word": w.get("word", ""),
                    "start_sec": curr_time + w.get("start_sec", 0.0),
                    "end_sec": curr_time + w.get("end_sec", 0.0)
                })
            if shot_words:
                curr_time += shot_words[-1].get("end_sec", 0.0) + 0.35
        if all_words:
            return build_subtitles_from_words(all_words, output_ass_path, is_vertical=is_vertical)

    # Strategy 3: Fallback to storyboard.json
    print("[Warning] Timings files not found, generating fallback subtitles from storyboard.json...")
    if not storyboard_path.exists():
        print(f"[Error] storyboard.json not found in {project_dir}")
        return None

    with open(storyboard_path, 'r', encoding='utf-8') as f:
        sb = json.load(f)

    events = []
    current_time = 0.3
    for shot in sb.get("shots", []):
        dur = shot.get("duration_sec", 4.0)
        narration = ""
        if isinstance(shot.get("audio"), dict):
            narration = shot["audio"].get("narration", "")
        elif isinstance(shot.get("narration"), str):
            narration = shot["narration"]

        if narration:
            chunks = split_into_short_chunks(narration, max_words=3)
            chunk_dur = (dur - 0.5) / max(1, len(chunks))
            c_start = current_time
            for chunk in chunks:
                c_end = c_start + chunk_dur
                start_str = format_ass_time(c_start)
                end_str = format_ass_time(c_end)
                styled_text = f"{{\\c&H0000D7FF&\\3c&H000A0D14&\\t(0,80,\\fscx108\\fscy108)\\t(80,160,\\fscx100\\fscy100)}}{chunk.upper()}"
                events.append(f"Dialogue: 0,{start_str},{end_str},ExplainerWordSub,,0,0,0,,{styled_text}")
                c_start = c_end
        current_time += dur

    with open(output_ass_path, 'w', encoding='utf-8') as f:
        f.write(get_ass_header(is_vertical=is_vertical))
        for ev in events:
            f.write(f"{ev}\n")

    print(f"[SUBTITLES] Generated fallback subtitles at: {output_ass_path}")
    return output_ass_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stickman / Ink Explainer Subtitle Generator")
    parser.add_argument("project_dir", help="Path to project directory")
    parser.add_argument("--aspect", choices=["9:16", "16:9"], default="9:16", help="Aspect ratio (default: 9:16)")
    args = parser.parse_args()

    build_subtitles(args.project_dir, aspect=args.aspect)
