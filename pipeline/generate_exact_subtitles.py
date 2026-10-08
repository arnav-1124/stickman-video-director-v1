import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import json
from pathlib import Path
from calculate_exact_timeline import get_exact_slide_cuts

def format_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def clean_word(w):
    return w.replace('"', '').replace('“', '').replace('”', '').strip()

def build_subtitles(words, cuts, show_on_markers=False):
    # Header for ASS subtitles
    header = """[Script Info]
Title: How Humans Invented the First Lie - Kinetic Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ExplainerWordSub,Arial Black,50,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.0,2.0,2,80,80,110,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []

    # Assign each word to the slide cut it falls into
    # Word center = (w['start'] + w['end']) / 2
    slide_words = {cid: [] for cid, _, _, _ in cuts}
    
    for w in words:
        w_mid = (w['start'] + w['end']) / 2
        assigned = False
        for cid, st, en, note in cuts:
            if st <= w_mid < en:
                slide_words[cid].append(w)
                assigned = True
                break
        if not assigned:
            # Fallback to closest slide
            min_dist = float('inf')
            best_cid = cuts[0][0]
            for cid, st, en, note in cuts:
                dist = min(abs(w_mid - st), abs(w_mid - en))
                if dist < min_dist:
                    min_dist = dist
                    best_cid = cid
            slide_words[best_cid].append(w)

    for cid, st, en, note in cuts:
        is_marker = "[Marker:" in note or "[Tally:" in note or "[Prop:" in note
        if is_marker and not show_on_markers:
            # Marker cards have huge prominent text drawn into the image, 
            # so we keep subtitles clean or optional
            continue

        c_words = slide_words[cid]
        if not c_words:
            continue

        # Group words in this slide into chunks of 2 to 4 words
        # Split on commas/periods if chunk >= 2
        chunks = []
        cur_chunk = []
        for w in c_words:
            cur_chunk.append(w)
            text = clean_word(w['word'])
            has_punct = text.endswith(',') or text.endswith('.') or text.endswith('?') or text.endswith('!')
            if len(cur_chunk) >= 4 or (len(cur_chunk) >= 2 and has_punct):
                chunks.append(cur_chunk)
                cur_chunk = []
        if cur_chunk:
            chunks.append(cur_chunk)

        # For each chunk, generate events for each active word
        for chunk in chunks:
            chunk_start = chunk[0]['start']
            chunk_end = chunk[-1]['end']
            
            # Pad slightly so subtitle appears right on start
            for idx, active_w in enumerate(chunk):
                w_st = active_w['start']
                w_en = active_w['end']
                
                # Make sure consecutive words in chunk have no visual gap
                if idx < len(chunk) - 1:
                    next_st = chunk[idx+1]['start']
                    # If gap is small (< 0.25s), stretch active highlight to next word start
                    if next_st > w_en and (next_st - w_en) < 0.25:
                        w_en = next_st
                
                parts = []
                for k, w_item in enumerate(chunk):
                    w_text = clean_word(w_item['word']).upper()
                    if k == idx:
                        # Gold pop highlight with subtle bounce scale
                        parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,60,\fscx108\fscy108)\t(60,120,\fscx100\fscy100)}" + w_text + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        parts.append(w_text)
                
                text_line = " ".join(parts)
                events.append(f"Dialogue: 0,{format_ass(w_st)},{format_ass(w_en)},ExplainerWordSub,,0,0,0,,{text_line}")

    return header + "\n".join(events) + "\n"

def main():
    root_dir = Path(".").resolve()
    ep_dir = root_dir / "projects/long/ep02_how_humans_invented_the_first_lie"
    words_file = ep_dir / "audio/exact_word_timestamps.json"
    sub_file = ep_dir / "subtitles_16_9.ass"

    with open(words_file, "r", encoding="utf-8") as f:
        words = json.load(f)

    cuts = get_exact_slide_cuts()
    # Don't show subtitles on marker/tally cards that already contain large hand-drawn titles
    ass_content = build_subtitles(words, cuts, show_on_markers=False)

    with open(sub_file, "w", encoding="utf-8") as f:
        f.write(ass_content)

    print(f"✓ Successfully generated exact kinetic subtitles: {sub_file.name}")
    print(f"Total word events processed: {len(words)}")

if __name__ == "__main__":
    main()
