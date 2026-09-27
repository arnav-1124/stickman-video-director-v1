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
RATE = "+8%"

SHOTS = [
    {
        "shot_id": 1,
        "text": "The Alpha needs constant applause to survive. The quiet Sigma walks alone, fueled by self-reliance.",
        "start_offset": 0.0
    },
    {
        "shot_id": 2,
        "text": "In class, the Alpha demands to lead the project. The quiet Sigma says nothing, and carries the entire grade.",
        "start_offset": 8.0
    },
    {
        "shot_id": 3,
        "text": "In the canteen, the Alpha needs an entourage to feel safe. The Sigma eats alone, immune to judgment.",
        "start_offset": 16.0
    },
    {
        "shot_id": 4,
        "text": "When tested, the Alpha explodes into rage. The Sigma gives a cold three-second stare, and returns to work.",
        "start_offset": 24.0
    },
    {
        "shot_id": 5,
        "text": "The Alpha desperately flexes for female approval. The Sigma needs nothing from the room, creating effortless mystery.",
        "start_offset": 32.0
    },
    {
        "shot_id": 6,
        "text": "At graduation, the loud guy is burnt out. The quiet observer built his future. Own your frame.",
        "start_offset": 40.0
    }
]

async def generate_shot_speech(text, out_mp3):
    communicate = edge_tts.Communicate(text, VOICE, pitch=PITCH, rate=RATE, boundary="WordBoundary")
    words = []
    with open(out_mp3, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = (chunk["offset"] / 10000) / 1000.0
                end_sec = ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                words.append({
                    "word": chunk["text"],
                    "start_sec": round(start_sec, 3),
                    "end_sec": round(end_sec, 3),
                    "duration_sec": round(end_sec - start_sec, 3)
                })
    return words

async def main():
    project_dir = Path("projects/ep02_alpha_vs_sigma_student")
    audio_dir = project_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    
    all_words = []
    dialogue_timings = []
    
    print("[1/3] Generating per-shot TTS with word timestamps...")
    for shot in SHOTS:
        sid = shot["shot_id"]
        offset = shot["start_offset"]
        text = shot["text"]
        out_mp3 = audio_dir / f"shot_{sid}.mp3"
        words = await generate_shot_speech(text, out_mp3)
        
        # probe duration
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(out_mp3)]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        dur = float(res.stdout.strip())
        print(f"  ✓ Shot {sid} ({dur:.2f}s, start: {offset:.1f}s): {text[:45]}...")
        
        # Global word timings
        for w in words:
            all_words.append({
                "word": w["word"],
                "start_sec": round(offset + w["start_sec"], 3),
                "end_sec": round(offset + w["end_sec"], 3),
                "duration_sec": w["duration_sec"]
            })
            
        dialogue_timings.append({
            "shot_id": sid,
            "speaker": "Narrator",
            "text": text,
            "file": f"shot_{sid}.mp3",
            "start_time": offset,
            "end_time": round(offset + dur, 3),
            "duration": round(dur, 3),
            "words": words
        })
        
    # Save word_timestamps.json and dialogue_timings.json
    with open(audio_dir / "word_timestamps.json", "w", encoding="utf-8") as f:
        json.dump(all_words, f, indent=2)
    with open(audio_dir / "dialogue_timings.json", "w", encoding="utf-8") as f:
        json.dump(dialogue_timings, f, indent=2)
        
    print("\n[2/3] Assembling frame-locked master narration track (48.0s)...")
    # Build filter complex to position each shot audio at its exact timestamp
    filter_parts = []
    inputs = []
    for idx, shot in enumerate(SHOTS):
        out_mp3 = audio_dir / f"shot_{shot['shot_id']}.mp3"
        inputs.extend(['-i', str(out_mp3.resolve())])
        delay_ms = int(shot["start_offset"] * 1000)
        filter_parts.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms}[a{idx}]")
        
    mix_inputs = "".join(f"[a{i}]" for i in range(len(SHOTS)))
    filter_parts.append(f"{mix_inputs}amix=inputs={len(SHOTS)}:duration=longest:normalize=0[mixed]")
    filter_parts.append("[mixed]apad=whole_dur=48[a_out]")
    
    master_mp3 = audio_dir / "master_narration.mp3"
    cmd = [
        'ffmpeg', '-y', *inputs,
        '-filter_complex', ';'.join(filter_parts),
        '-map', '[a_out]',
        '-c:a', 'libmp3lame', '-b:a', '192k',
        '-t', '48.0',
        str(master_mp3.resolve())
    ]
    subprocess.run(cmd, check=True)
    print(f"  ✓ Master narration saved: {master_mp3} (48.0s)")

if __name__ == "__main__":
    asyncio.run(main())
