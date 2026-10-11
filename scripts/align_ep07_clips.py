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

clips_plan = [
    {"clip_id": 1, "text": "Before you scroll, dopamine is not the pleasure chemical you think it is. You think it makes you feel happy. It doesn't."},
    {"clip_id": 2, "text": "If dopamine was pleasure, you'd feel satisfied after scrolling for two hours. Instead, you feel completely empty, foggy, and drained."},
    {"clip_id": 3, "text": "Neuroscientists proved this decades ago. Dopamine doesn't spike when you get a reward. It spikes right before—during the anticipation."},
    {"clip_id": 4, "text": "It's not satisfaction. It's an itch. An itch that whispers: just one more video, just one more click, maybe the next one is better."},
    {"clip_id": 5, "text": "Cheap apps hijacked this hunting reflex, turning your focus into a slot machine in your pocket. Here’s how to fix it."},
    {"clip_id": 6, "text": "Put twenty seconds of friction between you and cheap dopamine. Put the phone in another room, take five deep breaths, and let the craving burn out."},
    {"clip_id": 7, "text": "Real power isn't feeding the itch—it's having the strength to sit in stillness the second..."}
]

print("Uploading audio to Gemini 3.5 Flash Lite...")
uploaded = client.files.upload(file=str(audio_file))

prompt = f"""You are an expert audio alignment engineer. Below is the list of 7 animation video clips for a 53.66s voiceover:

{json.dumps(clips_plan, indent=2)}

Listen to this 53.66s voiceover. Identify the exact start_time and end_time (in seconds) for each of the 7 clips.
Constraints:
- clip 1 starts at 0.00
- clip 7 ends at 53.66
- end_time of clip N equals start_time of clip N+1
- Return valid raw JSON array of 7 objects with keys: clip_id, text, start_time, end_time, duration."""

resp = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=[uploaded, prompt],
    config=types.GenerateContentConfig(response_mime_type="application/json")
)

out_json = Path("projects/sticky_in_dark/shorts/ep07_dopamine_is_not_what_you_think/audio/exact_7_clips_sync.json")
with open(out_json, "w", encoding="utf-8") as f:
    f.write(resp.text)

print("SUCCESS! Wrote exact_7_clips_sync.json!")
