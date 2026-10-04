import mimetypes
import os
import struct
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

def generate_tts(text: str, output_file: str, voice_name: str = "Ludo"):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment or .env!")

    client = genai.Client(api_key=api_key)
    model = "gemini-3.8-flash-tts"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text)
            ]
        )
    ]

    config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
            )
        ),
    )

    print(f"[Gemini TTS] Requesting voice '{voice_name}' from {model}...")
    audio_data = bytearray()
    mime_type = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if chunk.parts and chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
            audio_data.extend(chunk.parts[0].inline_data.data)
            mime_type = chunk.parts[0].inline_data.mime_type
        elif chunk.text:
            print(f"[Gemini TTS Text]: {chunk.text}")

    if not audio_data:
        raise RuntimeError("No audio data received from Gemini TTS!")

    data_bytes = bytes(audio_data)
    if "wav" not in mime_type.lower():
        data_bytes = convert_to_wav(data_bytes, mime_type)

    out_p = Path(output_file).resolve()
    out_p.parent.mkdir(parents=True, exist_ok=True)
    with open(out_p, "wb") as f:
        f.write(data_bytes)

    print(f"[Gemini TTS] Saved {len(data_bytes)} bytes to: {out_p}")
    return out_p

if __name__ == "__main__":
    prompt_text = """## Style: Crisp, steady, calm, confident narration with brisk natural pacing (approx 155 words per minute), quiet elder-brother authority.

## Transcript:
What do you actually do when someone makes a slick joke at your expense in front of everyone at a friend’s house?
Most guys freeze.
You either laugh along nervously to keep the peace,
or you get angry and ruin the whole vibe.
Look, both reactions hand all your power to them.
Fake-laughing says you accept disrespect.
Getting angry shows they rattled you.
Here’s what an experienced senior will tell you.
Don’t get mad, and don’t raise your voice.
Just look at them calmly, and ask with quiet curiosity:
"Wait, I didn’t get it."
Something like, "What’s the joke?"
Notice what happens next.
The whole room goes quiet.
Sarcasm only survives on quick laughter.
The moment you force someone to explain their insult,
they have to admit they were just being petty.
They'll mumble, backpedal, and fold on the spot.
You don’t need to fight to command respect.
Just hold up the mirror, and let them dismantle themselves.
"""
    generate_tts(prompt_text, "projects/shorts/ep05_how_to_handle_disrespect/audio/voiceover_googleTTS.wav", voice_name="Ludo")
