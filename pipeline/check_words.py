import json

with open('projects/long/ep02_how_humans_invented_the_first_lie/audio/exact_word_timestamps.json', 'r', encoding='utf-8') as f:
    words = json.load(f)

print('=== SLIDE 24 (48.14 - 52.52) ===')
for w in words:
    if 47.5 <= w['start'] <= 53.0:
        print(f"{w['start']:6.3f} - {w['end']:6.3f}: {w['word']}")

print('\n=== SLIDE 41 (94.32 - 101.02) ===')
for w in words:
    if 93.5 <= w['start'] <= 101.5:
        print(f"{w['start']:6.3f} - {w['end']:6.3f}: {w['word']}")

print('\n=== SLIDE 52 (123.68 - 127.83) ===')
for w in words:
    if 123.0 <= w['start'] <= 128.5:
        print(f"{w['start']:6.3f} - {w['end']:6.3f}: {w['word']}")
