import json
import os

sb_path = 'projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_03_the_economy_of_availability/storyboard.json'
with open(sb_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total Shots in Chapter 3: {len(data['shots'])}")
for s in data['shots']:
    sid = s['shot_id']
    title = s.get('title', '')
    clause = s.get('spoken_clause', '')
    comp = s.get('visual_composition_16_9', '').replace('\n', ' ')
    print(f"Shot {sid} [{title}]:")
    print(f"  Clause: \"{clause}\"")
    print(f"  Visual: {comp[:110]}...")
    print("-" * 50)
