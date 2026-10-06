import subprocess
import re
from pathlib import Path

def get_silence_events(wav_path):
    cmd = ['ffmpeg', '-i', str(wav_path), '-af', 'silencedetect=noise=-30dB:d=0.22', '-f', 'null', '-']
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    events = []
    for l in res.stderr.split('\n'):
        if 'silence_start:' in l:
            m = re.search(r'silence_start:\s*([0-9.]+)', l)
            if m: events.append(('start', float(m.group(1))))
        elif 'silence_end:' in l:
            m = re.search(r'silence_end:\s*([0-9.]+)', l)
            if m: events.append(('end', float(m.group(1))))
    
    # Pair silence ends with next silence starts -> speech
    speech_intervals = []
    for i in range(len(events)-1):
        if events[i][0] == 'end' and events[i+1][0] == 'start':
            st = events[i][1]
            en = events[i+1][1]
            if en - st > 0.2:
                speech_intervals.append((round(st, 3), round(en, 3), round(en - st, 3)))
    return speech_intervals

audio_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/audio/google_tts")
for act in ['act1_ludo.wav', 'act2_ludo.wav', 'act3_ludo.wav']:
    intervals = get_silence_events(audio_dir / act)
    print(f"=== {act}: {len(intervals)} speech intervals ===")
    for idx, (st, en, dur) in enumerate(intervals, 1):
        print(f"  [{idx:02d}] {st:6.3f}s -> {en:6.3f}s ({dur:5.3f}s)")
