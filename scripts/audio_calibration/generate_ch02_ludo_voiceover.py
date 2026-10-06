import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import struct
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

ACTS_TEXT = {
    "act1": """Chapter Two: The Casino Effect. The Dopamine of Uncertainty.

To see this principle in action, we have to look inside a psychology laboratory from the nineteen fifties. The behavioral scientist B.F. Skinner conducted a famous series of experiments with animals.

In the first setup, a pigeon was placed inside a box with a lever. Every single time the pigeon pressed the lever, a food pellet dropped into the bowl. Press the lever, get food. Press the lever, get food.

What happened? The pigeon pressed the lever when it was hungry, ate its food, and then completely ignored the lever. The food was completely predictable. It was reliable, safe, and boring.

Then, Skinner changed the rules. He introduced what psychologists call a variable-ratio schedule of reinforcement. Now, when the pigeon pressed the lever, food only dropped out sometimes.

Sometimes it took one press. Sometimes it took five presses. Sometimes it took twelve presses with nothing, and then suddenly two pellets dropped at once. The reward was completely unpredictable.

What did the pigeon do? It became completely obsessed. It stood in front of the lever for hours, pressing it frantically, ignoring its sleep, and ignoring other birds. The unpredictability hijacked the animal's neurological reward circuitry.""",

    "act2": """Modern neuroscientists now know why this happens. Dopamine is not the chemical of pleasure. Dopamine is the chemical of anticipation.

Your brain does not release its biggest spike of dopamine when you receive a prize. It releases its biggest spike of dopamine when it does not know whether a prize is coming or not.

This is the exact psychological mechanism behind slot machines, lottery tickets, and social media notifications. When you pull the lever on a slot machine, the thrilling tension is in the spinning reels. Will three cherries align, or will you lose everything? That unresolved gap between hope and fear floods your brain with dopamine.""",

    "act3": """Now, bring this back to human interaction. The person who is always available operates like the first lever. Text them, and they reply within thirty seconds. Compliment them, and they shower you with praise. Ask them to meet, and they immediately say yes.

Their behavior is a hundred percent predictable. There is no mystery. There is no tension. And because there is no anticipation, there is no dopamine. Their attention is comfortable, but it creates zero gravitational pull.

The person who is slightly aloof, however, operates like the slot machine. When they look at you, it feels meaningful because they rarely look around. When they pay you a compliment, it sticks in your memory for three weeks because compliments from them are virtually impossible to get.

When they text you back, your phone lights up and your heart skips a beat—not because the text is poetic, but because you genuinely didn't know if they would reply at all.

You are not necessarily falling in love with the person. You are falling in love with the chemical cocktail created by their unpredictability.""",

    "outro": """In Chapter Three, we reveal why the most powerful move in any room is having somewhere else to be: The Economy of Availability. Subscribe to Sticky in Dark."""
}

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

def synthesize_act(client, text, out_wav):
    response = client.models.generate_content(
        model="gemini-3.8-flash-tts",
        contents=text,
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
    with open(out_wav, "wb") as f:
        f.write(wav_data)

def main():
    print("=" * 70)
    print("  🎙️ GENERATING CHAPTER 02 GEMINI LUDO NARRATION (-11.9 LUFS)")
    print("=" * 70)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[Error] GEMINI_API_KEY missing from environment.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    ch02_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_02_the_casino_effect")
    tts_dir = ch02_dir / "audio" / "google_tts"
    tts_dir.mkdir(parents=True, exist_ok=True)

    # 1. Synthesize each act
    raw_files = {}
    for act_name, text in ACTS_TEXT.items():
        out_wav = tts_dir / f"{act_name}_ludo.wav"
        print(f"\nSynthesizing {act_name.upper()} ({len(text.split())} words)...")
        synthesize_act(client, text, out_wav)
        raw_files[act_name] = out_wav
        print(f"  ✓ Saved {out_wav.name} ({out_wav.stat().st_size / (1024*1024):.2f} MB)")

    # 2. Concat into master raw narration with natural breathing pauses (0.500s between acts)
    concat_txt = tts_dir / "concat_acts.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for act in ["act1", "act2", "act3"]:
            f.write(f"file '{raw_files[act].resolve().as_posix()}'\n")

    raw_master_wav = tts_dir / "master_narration_ludo_raw.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy", str(raw_master_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"\nConcatenated raw master narration to {raw_master_wav.name}")

    # 3. Master through Studio DSP Broadcast Chain (-11.9 LUFS)
    master_wav = ch02_dir / "audio" / "ch02_master_narration_ludo.wav"
    master_mp3 = ch02_dir / "audio" / "ch02_master_narration_ludo.mp3"

    dsp_filter = (
        "highpass=f=80,"
        "equalizer=f=115:t=q:w=1.2:g=4.2,"
        "equalizer=f=250:t=q:w=1.5:g=2.0,"
        "equalizer=f=3500:t=q:w=1.0:g=2.5,"
        "acompressor=threshold=-18dB:ratio=2.5:attack=15:release=120,"
        "loudnorm=I=-11.9:TP=-1.5:LRA=7.0"
    )

    print("\nApplying Deep Masculine Broadcast Standard DSP (-11.9 LUFS)...")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_master_wav),
        "-af", dsp_filter,
        "-ar", "48000", str(master_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        "ffmpeg", "-y", "-i", str(master_wav),
        "-c:a", "libmp3lame", "-b:a", "320k", str(master_mp3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n[DSP MASTERING COMPLETE]\n  WAV Deliverable: {master_wav}\n  MP3 Deliverable: {master_mp3}")

if __name__ == "__main__":
    main()
