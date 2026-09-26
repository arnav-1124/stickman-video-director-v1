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
    pitch="-4Hz", 
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

    # Subtitles: Small, elegant, anchored strictly at bottom edge (MarginV: 120, well below floor line)
    if output_ass_path and words:
        ass_path = Path(output_ass_path).resolve()
        ass_header = """[Script Info]
Title: Ink Noir Kinetic Subtitles
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: InkSub, Arial Black, 38, &H00FFFFFF, &H000000FF, &H00000000, &H80000000, -1, 0, 0, 0, 100, 100, 1, 0, 1, 3, 1, 2, 60, 60, 120, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        events = []
        chunk_size = 3
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            start_t = format_ass_time(chunk[0]["start_sec"])
            end_t = format_ass_time(chunk[-1]["end_sec"] + 0.05)
            chunk_text = " ".join([w["word"] for w in chunk]).upper()
            events.append(f"Dialogue: 0,{start_t},{end_t},InkSub,,0,0,0,,{chunk_text}")

        with open(ass_path, "w", encoding="utf-8") as f:
            f.write(ass_header + "\n".join(events) + "\n")
        print(f"[Audio] Subtitles generated at safe bottom margin: {ass_path}")

    print(f"[Audio] Voiceover generated: {output_audio_path}")
    print(f"[Audio] Timestamps mapped: {len(words)} words saved to {output_json_path}")
    return words
