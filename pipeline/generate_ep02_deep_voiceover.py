import os
import struct
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    bits_per_sample = 16
    rate = 24000
    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate = int(param.split("=", 1)[1])
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass
    return {"bits_per_sample": bits_per_sample, "rate": rate}

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        chunk_size,
        b"WAVE",
        b"fmt ",
        16,
        1,
        num_channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data",
        data_size
    )
    return header + audio_data

def generate_deep_motivational_voiceover():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment!")

    client = genai.Client(api_key=api_key)

    script_path = Path("projects/sticky_in_dark/long/ep02_the_consistency_paradox/script.txt")
    script_text = script_path.read_text(encoding="utf-8").strip()

    prompt = f"""## Style: Deep, resonant, cinematic, baritone male motivational voice. 
Authoritative, calm, grounded, deliberate pacing (around 150 words per minute). 
Powerful sub-bass presence, elder-brother guidance, zero rush, high emotional conviction.

## Script:
{script_text}
"""

    print("[Deep Voiceover] Calling Gemini TTS with voice 'Fenrir'...")
    config = types.GenerateContentConfig(
        temperature=0.75,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Fenrir")
            )
        ),
    )

    audio_data = bytearray()
    mime_type = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-3.8-flash-tts",
        contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])],
        config=config,
    ):
        if chunk.parts and chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
            audio_data.extend(chunk.parts[0].inline_data.data)
            mime_type = chunk.parts[0].inline_data.mime_type

    if not audio_data:
        raise RuntimeError("Failed to receive audio from Gemini TTS!")

    raw_wav_bytes = bytes(audio_data)
    if "wav" not in mime_type.lower():
        raw_wav_bytes = convert_to_wav(raw_wav_bytes, mime_type)

    raw_wav_path = Path("projects/sticky_in_dark/long/ep02_the_consistency_paradox/audio/raw_fenrir.wav")
    raw_wav_path.parent.mkdir(parents=True, exist_ok=True)
    raw_wav_path.write_bytes(raw_wav_bytes)
    print(f"[Deep Voiceover] Raw audio saved: {raw_wav_path} ({len(raw_wav_bytes)} bytes)")

    # FFmpeg deep motivational audio mastering:
    # 1. Highpass at 65Hz to remove rumble
    # 2. Resonant sub-bass boost at 115Hz (+6dB)
    # 3. Chest warmth at 220Hz (+3dB)
    # 4. Vocal definition at 3.2kHz (+2.5dB)
    # 5. Dynamic compression for rich, heavy, broadcasting presence
    # 6. Normalization to -12 LUFS
    mastered_mp3_path = Path("remotion/public/audio/ep02_voiceover.mp3")
    mastered_mp3_path.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg_filter = (
        "highpass=f=65,"
        "equalizer=f=115:width_type=o:width=1.5:g=6.5,"
        "equalizer=f=220:width_type=o:width=1.2:g=3.0,"
        "equalizer=f=3200:width_type=o:width=1.0:g=2.5,"
        "compand=attacks=0.02:decays=0.08:points=-70/-60|-40/-28|-20/-12|0/-4:gain=4:volume=-70:delay=0.02,"
        "loudnorm=I=-12:TP=-1.0:LRA=7"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_wav_path),
        "-af", ffmpeg_filter,
        "-b:a", "192k",
        str(mastered_mp3_path)
    ]
    print(f"[Deep Voiceover] Running FFmpeg motivational mastering chain...")
    subprocess.run(cmd, check=True)
    print(f"[Deep Voiceover] Successfully generated and mastered deep motivational audio at: {mastered_mp3_path}")

if __name__ == "__main__":
    generate_deep_motivational_voiceover()
