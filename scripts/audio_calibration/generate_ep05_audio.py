import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import asyncio
import json
import subprocess
from pathlib import Path
import edge_tts

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"
RATE = "+1%"

PROJECT_DIR = Path("projects/shorts/ep05_how_to_handle_disrespect")
AUDIO_DIR = PROJECT_DIR / "audio"
SCRIPT_FILE = PROJECT_DIR / "script.txt"

def get_audio_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(result.stdout.strip())

async def generate_speech_with_timestamps(text, output_audio_path, output_json_path=None, voice=VOICE, pitch=PITCH, rate=RATE):
    output_audio_path = Path(output_audio_path).resolve()
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

    if output_json_path:
        output_json_path = Path(output_json_path).resolve()
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(words, f, indent=2)

    return words

async def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
        
    print(f"Loaded {len(lines)} beats from {SCRIPT_FILE}")
    
    # 1. Generate full continuous master voiceover
    full_text = "\n".join(lines)
    master_audio = AUDIO_DIR / "voiceover.mp3"
    master_json = AUDIO_DIR / "word_timestamps.json"
    
    print("\n[1/2] Generating master continuous voiceover.mp3...")
    master_words = await generate_speech_with_timestamps(full_text, master_audio, master_json)
    master_dur = get_audio_duration(master_audio)
    print(f"[OK] Master audio generated: {master_audio} ({master_dur:.2f}s, {len(master_words)} words)")
    
    # 2. Generate per-beat audio to get individual durations and clean splits
    print("\n[2/2] Generating per-beat individual audio clips...")
    beat_timings = []
    for i, line in enumerate(lines, 1):
        shot_audio = AUDIO_DIR / f"shot_{i:02d}.mp3"
        shot_json = AUDIO_DIR / f"shot_{i:02d}_words.json"
        words = await generate_speech_with_timestamps(line, shot_audio, shot_json)
        dur = get_audio_duration(shot_audio)
        beat_timings.append({
            "beat_id": i,
            "text": line,
            "duration": round(dur, 2),
            "words_count": len(words)
        })
        print(f"  Beat {i:02d}: ({dur:4.2f}s) \"{line[:45]}...\"")
        
    with open(AUDIO_DIR / "beat_timings.json", "w", encoding="utf-8") as f:
        json.dump(beat_timings, f, indent=2)
        
    total_beat_dur = sum(b["duration"] for b in beat_timings)
    print(f"\n[OK] Completed! Master Duration: {master_dur:.2f}s | Sum of individual beats: {total_beat_dur:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
