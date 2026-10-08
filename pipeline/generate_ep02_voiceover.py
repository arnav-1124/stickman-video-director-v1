import sys
from pathlib import Path
from generate_gemini_tts import generate_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
ep_dir = root_dir / "projects/long/ep02_how_humans_invented_the_first_lie"
script_file = ep_dir / "script.txt"
output_wav = ep_dir / "audio/voiceover.wav"

with open(script_file, "r", encoding="utf-8") as f:
    script_text = f.read().strip()

prompt = f"""## Style: High-energy, curious, witty, suspenseful storytelling with crisp natural cadence (approx 145 words per minute), slight dramatic pauses between revelatory beats, mimicking the signature Ink Explainer storytelling style.

## Transcript:
{script_text}
"""

print("[EP02] Generating Gemini Flash TTS for 'How Humans Invented the First Lie'...")
out_path = generate_tts(prompt, str(output_wav), voice_name="Ludo")
print(f"[EP02] Successfully saved voiceover to: {out_path}")
