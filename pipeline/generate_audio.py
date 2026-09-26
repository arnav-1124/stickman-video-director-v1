import asyncio
import json
from pathlib import Path
import edge_tts

DEFAULT_VOICE = "en-US-ChristopherNeural"

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

async def generate_speech_with_timestamps(
    text, 
    output_audio_path, 
    output_json_path, 
    output_ass_path=None, 
    voice=DEFAULT_VOICE, 
    pitch="-2Hz", 
    rate="+0%"
):
    output_audio_path = Path(output_audio_path).resolve()
    output_json_path = Path(output_json_path).resolve()
    output_audio_path.parent.mkdir(parents=True, exist_ok=True)

    communicate = edge_tts.Communicate(
        text, 
        voice, 
        pitch=pitch, 
        rate=rate, 
        boundary="WordBoundary"
    )
    
    words = []
    with open(output_audio_path, "wb") as audio_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = (chunk["offset"] / 10000) / 1000.0
                end_sec = ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                words.append({
                    "word": chunk["text"],
                    "start_sec": round(start_sec, 3),
                    "end_sec": round(end_sec, 3),
                    "duration_sec": round(end_sec - start_sec, 3)
                })

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)

    # High-retention word-by-word active highlighted subtitles (Karaoke glow effect)
    if output_ass_path and words:
        ass_path = Path(output_ass_path).resolve()
        
        # Color codes in ASS format (&HAABBGGRR):
        # Active Word: Vivid Glowing Gold &H0000D7FF& (BGR: 00, D7, FF -> Amber/Gold)
        # Inactive Words: Crisp White &H00FFFFFF&
        # Outline: Deep Black &H000A0D14&
        ass_header = """[Script Info]
Title: Dynamic Word-Level Highlight Captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: FinanceWordSub, Arial Black, 42, &H00FFFFFF, &H0000D7FF, &H000E121B, &HA0000000, -1, 0, 0, 0, 100, 100, 1.2, 0, 1, 3.5, 1.5, 2, 60, 60, 110, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events = []
        chunk_size = 3  # 3 words per line for optimal smartphone readability
        
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            chunk_start = chunk[0]["start_sec"]
            chunk_end = chunk[-1]["end_sec"] + 0.12
            
            # Emit an event for each active word inside this chunk
            for active_idx, target_word in enumerate(chunk):
                w_start = target_word["start_sec"]
                # Active word ends when next word begins, or chunk ends
                if active_idx < len(chunk) - 1:
                    w_end = chunk[active_idx + 1]["start_sec"]
                else:
                    w_end = chunk_end
                    
                if w_end <= w_start:
                    w_end = w_start + 0.08
                    
                start_t = format_ass_time(w_start)
                end_t = format_ass_time(w_end)
                
                # Build styled phrase where active word is highlighted in vivid Gold/Amber
                parts = []
                for idx, w in enumerate(chunk):
                    raw_word = w["word"].upper()
                    if idx == active_idx:
                        # Highlight active word in Gold with clean outline
                        parts.append(f"{{\\c&H0000D7FF&\\3c&H000A0D14&\\b1}}{raw_word}{{\\c&H00FFFFFF&\\3c&H000A0D14&\\b1}}")
                    else:
                        parts.append(f"{raw_word}")
                        
                line_text = " ".join(parts)
                events.append(f"Dialogue: 0,{start_t},{end_t},FinanceWordSub,,0,0,0,,{line_text}")

        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(ass_header + "\n".join(events) + "\n")
        print(f"[Audio] Active word-by-word highlighted captions generated: {ass_path}")

    print(f"[Audio] Voiceover generated: {output_audio_path}")
    print(f"[Audio] Timestamps mapped: {len(words)} words saved to {output_json_path}")
    return words

if __name__ == "__main__":
    test_text = "If you improve by just one percent every single day for a year, you end up thirty-seven times better."
    asyncio.run(generate_speech_with_timestamps(
        test_text,
        "scratch/test_audio.mp3",
        "scratch/test_words.json",
        "scratch/test_subs.ass"
    ))
