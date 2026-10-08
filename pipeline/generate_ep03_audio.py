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
acts_dir = ep_dir / "acts"
master_audio_dir = ep_dir / "audio"
master_assets_dir = ep_dir / "master_assets"

# Ensure root directories exist
master_audio_dir.mkdir(parents=True, exist_ok=True)
master_assets_dir.mkdir(parents=True, exist_ok=True)

# Define the 5 Acts
acts_data = [
    {
        "id": "act01_the_animal_standard",
        "title": "Act 1: The Animal Standard",
        "script": """In ninety-seven percent of all mammal species on Earth... "romance" does not exist.
A male grizzly bear or a lion mates for thirty seconds, turns around, and disappears into the forest forever.
No awkward text messages. No second dates. No staying awake until three in the morning wondering what they're thinking.
In the wild, nature values speed, efficiency, and moving on.
So why on Earth did human beings evolve this sweaty-palmed, obsessive, heart-pounding insanity called falling in love?
If nature only cared about survival, love is an absolute disaster.
It makes you clumsy. It makes you reckless. It makes grown adults write terrible poetry and stare blankly at their phones."""
    },
    {
        "id": "act02_the_savanna_baby_crisis",
        "title": "Act 2: The Savanna Baby Crisis",
        "script": """To understand why your brain does this, you have to travel back four million years ago, to the sun-scorched African savanna.
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
    },
    {
        "id": "act03_the_first_spark",
        "title": "Act 3: The First Spark (Kael & Mira)",
        "script": """Picture two ancient humans named Kael and Mira, two million years ago.
Kael was a hardened hunter who had survived leopard ambushes and bone-crushing cold.
He wasn't sentimental. He was built for survival.
Until one afternoon near a freshwater stream, Mira glanced up from gathering berries.
And Kael’s brain completely crashed.
His hands went numb. His heart slammed against his ribs like a war drum. He suddenly forgot how to speak.
What was actually happening inside Kael wasn't magic. It was evolution activating three subconscious scanning radars:
First was the Scent Radar. Without knowing it, Kael was inhaling microscopic immune peptides from Mira’s skin—what biologists call the Major Histocompatibility Complex.
His olfactory bulb instantly calculated that her immune system filled the exact genetic gaps in his own, ensuring their offspring would survive ancient plagues.
Second was the Symmetry Scanner. His visual cortex mapped her facial features in milliseconds, reading facial symmetry as proof of zero parasites and robust nutrition.
And then, Kael did something no living animal in history had ever done:
He knelt down in the riverbed, picked up a glowing, smooth translucent blue river stone... and awkwardly handed it to her.
The world’s very first romantic gift."""
    },
    {
        "id": "act04_the_brain_on_love",
        "title": "Act 4: The Brain On Love (The Chemical Hijack)",
        "script": """If you put Kael into a modern brain scanner at that exact second, doctors would be stunned.
Because neurologically, being in love is not an emotion. It is a temporary biochemical hijacking.
First, dopamine flooded his Ventral Tegmental Area—the exact same neural circuit hijacked by high-stakes gambling and cocaine. Every glance from Mira gave him an addictive rush.
Second, his serotonin levels crashed by forty percent—dropping into the exact chemical range seen in patients with severe Obsessive-Compulsive Disorder.
That’s why Kael couldn't stop replaying her smile over and over in his head.
And third: evolution pulled off its most ruthless trick.
It completely shut down his amygdala and prefrontal cortex.
The rational parts of his brain that detect danger, spot red flags, and make sensible decisions? Completely switched off.
Nature deliberately blinded Kael so he couldn't talk himself out of staying."""
    },
    {
        "id": "act05_the_eternal_echo",
        "title": "Act 5: The Eternal Echo",
        "script": """When the sun set, Kael didn't vanish into the savanna like a bear.
He sat by the cave entrance through freezing rains.
He carried heavy meat through blizzards to feed Mira.
He held the fragile baby in his scarred hands.
Love wasn't poetry. Love was the biological survival shield that kept human civilization from dying in the dark.
So the next time your heart skips a beat when someone walks into the room...
When your palms sweat, your voice trembles, and your brain goes blank...
Don't feel foolish.
You are feeling the two-million-year-old survival spell that kept the entire human race alive."""
    }
]

print("=========================================================")
print("  EPISODE 03: MODULAR ACT PIPELINE SETUP & AUDIO GEN")
print("=========================================================\n")

act_wav_files = []

for idx, act in enumerate(acts_data, 1):
    act_folder = acts_dir / act["id"]
    slides_folder = act_folder / "slides"
    audio_folder = act_folder / "audio"
    renders_folder = act_folder / "renders"
    
    # Create act directories
    slides_folder.mkdir(parents=True, exist_ok=True)
    audio_folder.mkdir(parents=True, exist_ok=True)
    renders_folder.mkdir(parents=True, exist_ok=True)
    
    # Save Act script
    script_path = act_folder / "script.txt"
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(act["script"].strip() + "\n")
    
    raw_wav_path = audio_folder / "voiceover_raw.wav"
    mastered_wav_path = audio_folder / "voiceover.wav"
    
    print(f"\n--- [{idx}/5] Generating Audio for {act['title']} ---")
    
    prompt = f"""## Style: Warm, reflective, deep, conversational storytelling with crisp natural cadence (approx 145-150 words per minute), subtle dry wit, emotional vulnerability, and resonant authority. Voice of an experienced psychologist or grounded older brother.

## Transcript:
{act['script'].strip()}
"""
    # Generate TTS
    generate_tts(prompt, str(raw_wav_path), voice_name="Ludo")
    
    # Master Act Audio with our signature masculine EQ & loudnorm chain
    # 0.350s inter-sentence pacing preserved
    dsp_filter = (
        "equalizer=f=115:width_type=o:w=1.2:g=4.2,"
        "equalizer=f=250:width_type=o:w=1.0:g=2.0,"
        "equalizer=f=3500:width_type=o:w=1.2:g=2.5,"
        "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
        "loudnorm=I=-11.9:TP=-1.0:LRA=6.0"
    )
    
    cmd_dsp = [
        "ffmpeg", "-y", "-i", str(raw_wav_path),
        "-af", dsp_filter,
        "-ar", "44100", "-ac", "2",
        str(mastered_wav_path)
    ]
    subprocess.run(cmd_dsp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  -> Act audio mastered: {mastered_wav_path}")
    act_wav_files.append(mastered_wav_path)

# Build the Full Master Audio by concatenating all 5 acts with exact 0.350s pause buffer
print("\n--- Assembling Full-Fledged Master Audio Track ---")

# Create a 0.350s silence wav
silence_wav = master_audio_dir / "silence_035s.wav"
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
    "-t", "0.350", str(silence_wav)
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# Create concat list
concat_list_file = master_audio_dir / "concat_list.txt"
with open(concat_list_file, "w", encoding="utf-8") as f:
    for i, act_wav in enumerate(act_wav_files):
        f.write(f"file '{act_wav.as_posix()}'\n")
        if i < len(act_wav_files) - 1:
            f.write(f"file '{silence_wav.as_posix()}'\n")

final_master_wav = master_audio_dir / "master_voiceover.wav"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", str(concat_list_file),
    "-c", "copy",
    str(final_master_wav)
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

print(f"\n[SUCCESS] Master Full-Fledged Audio Created at: {final_master_wav}")

# Check final master audio duration
probe_cmd = [
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", str(final_master_wav)
]
result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
duration_sec = float(result.stdout.strip())
minutes = int(duration_sec // 60)
seconds = int(duration_sec % 60)

print(f"Master Audio Duration: {duration_sec:.2f} seconds ({minutes}m {seconds:02d}s)")
print("=========================================================")
