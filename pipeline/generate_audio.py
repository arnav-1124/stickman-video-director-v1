import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import argparse
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path
import edge_tts

DEFAULT_VOICE = "en-US-ChristopherNeural"
NARRATOR_VOICES = {
    "christopher": {"voice": "en-US-ChristopherNeural", "pitch": "-2Hz", "rate": "+2%"},
    "guy": {"voice": "en-US-GuyNeural", "pitch": "+0Hz", "rate": "+4%"},
    "brian": {"voice": "en-US-BrianNeural", "pitch": "-1Hz", "rate": "+0%"},
    "eric": {"voice": "en-US-EricNeural", "pitch": "-3Hz", "rate": "+1%"}
}

def format_ass_time(seconds):
    """Converts seconds to ASS timestamp H:MM:SS.cc"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

def get_audio_duration(file_path):
    """Returns duration in seconds using ffprobe."""
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(result.stdout.strip())

async def generate_speech_with_timestamps(
    text, 
    output_audio_path, 
    output_json_path=None, 
    voice=DEFAULT_VOICE, 
    pitch="-2Hz", 
    rate="+2%"
):
    """Generates an MP3 audio file with word-level boundary timestamps."""
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

async def build_episode_audio(project_dir, voice_key="christopher"):
    """
    Builds audio for an episode from storyboard.json:
    - Generates shot narration clips into audio/
    - Extracts word boundary timestamps for each shot
    - Generates combined audio/dialogue_timings.json
    """
    project_dir = Path(project_dir).resolve()
    storyboard_path = project_dir / "storyboard.json"
    audio_dir = project_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    if not storyboard_path.exists():
        print(f"[Error] storyboard.json not found in {project_dir}")
        return

    with open(storyboard_path, 'r', encoding='utf-8') as f:
        sb = json.load(f)

    voice_cfg = NARRATOR_VOICES.get(voice_key, NARRATOR_VOICES["christopher"])
    voice = voice_cfg["voice"]
    pitch = voice_cfg["pitch"]
    rate = voice_cfg["rate"]

    timings = []
    cumulative_time = 0.0

    print(f"\n[TTS] Generating voiceover for {len(sb.get('shots', []))} shots using voice {voice}...")
    for idx, shot in enumerate(sb.get("shots", []), start=1):
        sid = shot.get("shot_id", idx)
        narration = ""
        if isinstance(shot.get("audio"), dict):
            narration = shot["audio"].get("narration", "")
        elif isinstance(shot.get("narration"), str):
            narration = shot["narration"]

        if not narration:
            continue

        shot_audio = audio_dir / f"shot_{sid}.mp3"
        shot_words_json = audio_dir / f"shot_{sid}_words.json"
        
        words = await generate_speech_with_timestamps(
            narration,
            shot_audio,
            shot_words_json,
            voice=voice,
            pitch=pitch,
            rate=rate
        )

        dur = get_audio_duration(shot_audio)
        start_time = cumulative_time
        end_time = cumulative_time + dur

        timings.append({
            "shot_id": sid,
            "speaker": "Narrator",
            "text": narration,
            "file": str(shot_audio.name),
            "start_time": round(start_time, 3),
            "end_time": round(end_time, 3),
            "duration": round(dur, 3),
            "words": words
        })

        cumulative_time = end_time + 0.35  # Subtle pause between shots

    timings_path = audio_dir / "dialogue_timings.json"
    with open(timings_path, 'w', encoding='utf-8') as f:
        json.dump(timings, f, indent=2)

    print(f"\n✓ Episode voiceover completed! Total narration duration: {round(cumulative_time, 1)}s")
    print(f"✓ Shot audios saved to: {audio_dir}")
    print(f"✓ Dialogue timings saved to: {timings_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stickman / Ink Explainer Audio Generator")
    parser.add_argument("project_dir", nargs="?", default=None, help="Path to episode directory")
    parser.add_argument("--voice", default="christopher", choices=["christopher", "guy", "brian", "eric"], help="Voice profile")
    parser.add_argument("--text", default=None, help="Generate single test audio with given text")
    parser.add_argument("--output", default="audio_output.mp3", help="Output file for single test")
    args = parser.parse_args()

    if args.text:
        asyncio.run(generate_speech_with_timestamps(
            args.text,
            args.output,
            args.output.replace('.mp3', '_words.json'),
            voice=NARRATOR_VOICES[args.voice]["voice"]
        ))
    elif args.project_dir:
        asyncio.run(build_episode_audio(args.project_dir, voice_key=args.voice))
    else:
        parser.print_help()
