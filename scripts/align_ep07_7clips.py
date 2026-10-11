import os
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

audio_file = Path("projects/sticky_in_dark/shorts/ep07_dopamine_is_not_what_you_think/audio/master_voiceover.wav")
uploaded = client.files.upload(file=str(audio_file))

acts = [
    {"clip_id": 1, "text": "Before you scroll, dopamine is not the pleasure chemical you think it is. You think it makes you feel happy, but it doesn't."},
    {"clip_id": 2, "text": "If dopamine was pleasure, you would feel satisfied after scrolling for two hours. Instead, you feel completely empty, foggy, and exhausted."},
    {"clip_id": 3, "text": "Neuroscientists proved this decades ago: dopamine doesn't spike when you get a reward. It spikes right before—during the anticipation."},
    {"clip_id": 4, "text": "It is not satisfaction. It is an itch. A biological itch that whispers: just one more video, just one more click, maybe the next one is better."},
    {"clip_id": 5, "text": "Every time you refresh, your brain floods with craving, not fulfillment. Cheap apps hijacked this ancient hunting reflex, turning your focus into a slot machine in your pocket."},
    {"clip_id": 6, "text": "Here’s how you take control. Put twenty seconds of friction between you and cheap dopamine. Put the phone in another room, take ten deep breaths, and let the craving burn out."},
    {"clip_id": 7, "text": "Real power isn't feeding the itch every five seconds—it's having the strength to sit in stillness the second..."}
]

prompt = f"""You are an audio alignment engineer. Below are the 7 narrative acts for this 52.50s voiceover:

{json.dumps(acts, indent=2)}

Listen to the audio. Identify the exact start_time and end_time (in seconds) for each of the 7 acts.
Rules:
- Act 1 starts at 0.00
- Act 7 ends at 52.50
- end_time of Act N = start_time of Act N+1
- Return JSON array of 7 objects with keys: clip_id, start_time, end_time, duration, text."""

res = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=[uploaded, prompt],
    config=types.GenerateContentConfig(response_mime_type="application/json")
)

out_f = Path("projects/sticky_in_dark/shorts/ep07_dopamine_is_not_what_you_think/audio/exact_7_clips_sync.json")
out_f.write_text(res.text, encoding="utf-8")
print("SUCCESS! Wrote exact_7_clips_sync.json:")
print(res.text)
