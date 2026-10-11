import os
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types

api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

slides_dir = Path('projects/sticky_in_dark/shorts/ep07_dopamine_is_not_what_you_think/slides')
storyboard_file = Path('projects/sticky_in_dark/shorts/ep07_dopamine_is_not_what_you_think/storyboard.json')
storyboard = json.loads(storyboard_file.read_text(encoding='utf-8'))['beats']

results = []
print('Analyzing all 20 slides via Gemini Vision...')

for beat in storyboard:
    s_id = beat['slide_id']
    s_file = slides_dir / f'slide_{s_id:02d}.jpg'
    if not s_file.exists():
        print(f'Slide {s_id} missing!')
        continue
    
    img_bytes = s_file.read_bytes()
    prompt = f"""You are a senior motion graphics director analyzing a 1080x1920 vertical comic slide for Remotion After Effects camera choreographies.
Spoken voiceover for this beat ({beat['time_window']}): "{beat['spoken_words']}"
Intended scene: {beat['visual_description']}

Analyze the image carefully and output valid JSON only with keys:
- "actual_visual": brief description of what is actually drawn in this image.
- "primary_element": name and description of the main focal element.
- "focal_point_1": [X, Y] pixel coordinates (integers, 0 to 1080 for X, 0 to 1920 for Y) of the primary element's center.
- "secondary_element": name and description of second focal element (or null if single focus).
- "focal_point_2": [X, Y] pixel coordinates (or null) of the secondary element.
- "recommended_motion": "zoom_in", "pan_across", "rack_focus", "slow_drift", or "punch_in".
- "start_zoom": float (e.g. 1.05 to 1.35)
- "end_zoom": float (e.g. 1.25 to 1.85)
"""

    try:
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=[
                types.Part.from_bytes(data=img_bytes, mime_type='image/jpeg'),
                prompt
            ],
            config=types.GenerateContentConfig(response_mime_type='application/json')
        )
        data = json.loads(response.text)
        data['slide_id'] = s_id
        data['time_window'] = beat['time_window']
        data['spoken_words'] = beat['spoken_words']
        results.append(data)
        print(f"Done Slide {s_id:02d}: {data.get('primary_element', '')} -> {data.get('focal_point_1')}")
    except Exception as e:
        print(f"Error Slide {s_id:02d}:", e)

out_file = Path('projects/sticky_in_dark/shorts/ep07_dopamine_is_not_what_you_think/slides_camera_analysis.json')
out_file.write_text(json.dumps(results, indent=2), encoding='utf-8')
print('SUCCESS! Analyzed all slides and saved to:', out_file)
