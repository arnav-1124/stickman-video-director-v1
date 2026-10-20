import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import struct
import subprocess
from google import genai
from google.genai import types

load_dotenv()

PROJECT_DIR = Path("projects/sticky_in_dark/shorts/ep08_the_toothbrush_protocol")
SCRIPT_FILE = PROJECT_DIR / "script.txt"
AUDIO_DIR = PROJECT_DIR / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

RAW_LUDO_WAV = AUDIO_DIR / "voiceover_ludo_raw.wav"

def convert_pcm_to_wav(audio_data: bytes, sample_rate: int = 24000, bits_per_sample: int = 16) -> bytes:
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", chunk_size, b"WAVE", b"fmt ",
        16, 1, num_channels, sample_rate, byte_rate, block_align, bits_per_sample,
        b"data", data_size
    )
    return header + audio_data

def synthesize_script():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=api_key)

    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        script_text = f.read().strip()

    print(f"Synthesizing script with Google TTS Ludo voice ({len(script_text.split())} words)...")

    response = client.models.generate_content(
        model="gemini-3.8-flash-tts",
        contents=script_text,
        config=types.GenerateContentConfig(
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Ludo")
                )
            )
        )
    )

    audio_bytes = None
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            audio_bytes = part.inline_data.data
            break

    if not audio_bytes:
        raise RuntimeError("No audio data returned from Gemini TTS!")

    wav_data = convert_pcm_to_wav(audio_bytes, sample_rate=24000)
    with open(RAW_LUDO_WAV, "wb") as f:
        f.write(wav_data)

    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(RAW_LUDO_WAV)]
    dur = float(subprocess.check_output(cmd).decode().strip())
    print(f"[OK] Raw Google TTS Ludo audio saved to: {RAW_LUDO_WAV} ({dur:.2f}s)")
    return dur

if __name__ == "__main__":
    synthesize_script()
