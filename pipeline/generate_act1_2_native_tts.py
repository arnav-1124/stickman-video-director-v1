import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir / "pipeline"))

from generate_gemini_tts import generate_tts

load_dotenv(root_dir / ".env")

ep_dir = root_dir / "projects/long/ep03_how_humans_first_fell_in_love"
test_output_dir = ep_dir / "audio/act1_2_tests"
test_output_dir.mkdir(parents=True, exist_ok=True)
temp_dir = root_dir / "temp/act1_2_native"
temp_dir.mkdir(parents=True, exist_ok=True)

# Act 1 & 2 combined transcript
transcript = """In ninety-seven percent of all mammal species on Earth... "romance" does not exist.
A male grizzly bear or a lion mates for thirty seconds, turns around, and disappears into the forest forever.
No awkward text messages. No second dates. No staying awake until three in the morning wondering what they're thinking.
In the wild, nature values speed, efficiency, and moving on.
So why on Earth did human beings evolve this sweaty-palmed, obsessive, heart-pounding insanity called falling in love?
If nature only cared about survival, love is an absolute disaster.
It makes you clumsy. It makes you reckless. It makes grown adults write terrible poetry and stare blankly at their phones.
To understand why your brain does this, you have to travel back four million years ago, to the sun-scorched African savanna.
Back then, our ape-like ancestors made a monumental decision: they stood up on two feet.
Walking upright was brilliant for spotting predators and traveling long distances.
There was only one catastrophic catch: it narrowed the female pelvis.
At the exact same time, hominid brains were rapidly ballooning in size.
And that created an evolutionary nightmare known as the Obstetric Dilemma.
If a human baby stayed inside the womb until its brain was fully developed... it would physically kill the mother during birth.
So nature was forced into a desperate compromise:
Human babies must be born prematurely. Completely, utterly helpless.
A baby horse can stand and run thirty minutes after birth.
A human newborn cannot even support the weight of its own neck for four months.
Now put that helpless baby into an ancient savanna crawling with saber-toothed cats, hyenas, and lethal droughts.
A mother carrying a crying, defenseless infant could not hunt, run, or dig for roots alone. Without constant help, she would starve.
And the male hunters? In the animal world, a male has zero incentive to share his food. You eat your kill, and you survive.
Evolution hit a biological dead end:
Either human beings would go completely extinct... or nature had to invent an emotional superglue so powerful it could force a selfish hunter to stay for years.
That superglue was romantic love."""

dsp_filter = (
    "equalizer=f=115:width_type=o:w=1.2:g=4.2,"
    "equalizer=f=250:width_type=o:w=1.0:g=2.0,"
    "equalizer=f=3500:width_type=o:w=1.2:g=2.5,"
    "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
    "loudnorm=I=-11.9:TP=-1.0:LRA=6.0"
)

# Test Variant 1: Brisk & Punchy Cadence (~160 WPM, tight natural sentence flow)
prompt_v1 = f"""## Style: Crisp, energetic, brisk conversational storytelling with rapid natural cadence (approx 160 words per minute), tight punchy delivery, and minimal breathing pauses between sentences. Zero sluggishness, high vocal momentum, deep masculine warmth.

## Transcript:
{transcript}
"""

# Test Variant 2: Fast & Dynamic Momentum (~168 WPM, eager cadence, rapid seamless flow)
prompt_v2 = f"""## Style: Fast-paced, high-energy, dynamic narration (approx 168-170 words per minute), eager and punchy cadence, continuous vocal momentum with rapid, seamless transitions between sentences. Deep, warm, authoritative masculine voice with no slow pauses.

## Transcript:
{transcript}
"""

variants = [
    ("native_v1_brisk_160wpm", prompt_v1, "Variant 1 (Brisk 160 WPM Native Cadence)"),
    ("native_v2_fast_168wpm", prompt_v2, "Variant 2 (Fast 168 WPM High-Momentum Native)")
]

for label, p, desc in variants:
    print(f"\n=======================================================")
    print(f"Generating {desc}...")
    print(f"=======================================================")
    
    raw_wav = temp_dir / f"{label}_raw.wav"
    mastered_wav = test_output_dir / f"{label}.wav"
    mastered_mp3 = test_output_dir / f"{label}.mp3"
    
    # 1. Generate clean single-take native audio
    generate_tts(p, str(raw_wav), voice_name="Ludo")
    
    # 2. Apply master DSP chain (no slicing, no micro-fades, 100% natural vocal prosody)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_wav),
        "-af", dsp_filter,
        "-ar", "44100", "-ac", "2",
        str(mastered_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Export high-quality MP3 for quick review
    subprocess.run([
        "ffmpeg", "-y", "-i", str(mastered_wav),
        "-b:a", "192k",
        str(mastered_mp3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Measure duration
    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(mastered_wav)
    ]).decode().strip())
    
    m, s = int(dur // 60), int(dur % 60)
    print(f"[SUCCESS] {label} ready: {dur:.2f}s ({m}m {s:02d}s)")
    print(f"  -> WAV: {mastered_wav}")
    print(f"  -> MP3: {mastered_mp3}")

print("\nAll native variants generated successfully!")
