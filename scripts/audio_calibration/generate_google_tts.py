# Reusable Google AI Studio TTS Generator (Gemini 3.8 Flash TTS)
# Voice: Ludo (Confident and clear. Low pitch)

import mimetypes
import os
import re
import struct
from pathlib import Path
from google import genai
from google.genai import types

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

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    bits_per_sample = 16
    rate = 24000

    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass

    return {"bits_per_sample": bits_per_sample, "rate": rate}

def generate_voiceover(script_text: str, output_path: str, voice_name: str = "Ludo", style_prompt: str = "Style: Confident, calm, unhurried elder brother speaking with quiet wisdom and relaxed authority."):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set. Get your key from Google AI Studio.")

    client = genai.Client(api_key=api_key)
    model = "gemini-3.8-flash-tts"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(
                    text=f"## Transcript:\n{script_text}\n",
                    speech_metadata=types.SpeechMetadata(
                        style=style_prompt,
                    ),
                ),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=voice_name
                )
            )
        ),
    )

    audio_data = bytearray()
    mime_type = ""
    print(f"Calling Gemini 3.8 Flash TTS with voice: {voice_name}...")
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.parts is None:
            continue
        if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
            inline_data = chunk.parts[0].inline_data
            audio_data.extend(inline_data.data)
            mime_type = inline_data.mime_type
        elif text := chunk.text:
            print(text)

    if audio_data:
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        data_buffer = convert_to_wav(bytes(audio_data), mime_type) if out_file.suffix.lower() == ".wav" else bytes(audio_data)
        with open(out_file, "wb") as f:
            f.write(data_buffer)
        print(f"Saved generated audio to: {out_file}")
        return out_file
    else:
        raise RuntimeError("No audio data returned from Gemini TTS.")

if __name__ == "__main__":
    import sys
    script_file = Path("projects/shorts/ep05_how_to_handle_disrespect/script.txt")
    if script_file.exists():
        with open(script_file, "r", encoding="utf-8") as f:
            text = f.read().strip()
        generate_voiceover(text, "projects/shorts/ep05_how_to_handle_disrespect/audio/voiceover_googleTTS.wav", voice_name="Ludo")
