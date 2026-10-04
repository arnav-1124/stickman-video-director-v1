import subprocess
import json
import numpy as np
import wave
from pathlib import Path

AUDIO_PATH = Path("projects/shorts/ep05_how_to_handle_disrespect/audio/voiceover_googleTTS.wav")

with wave.open(str(AUDIO_PATH), "rb") as wf:
    num_channels = wf.getnchannels()
    sample_width = wf.getsampwidth()
    frame_rate = wf.getframerate()
    num_frames = wf.getnframes()
    raw_bytes = wf.readframes(num_frames)

audio_data = np.frombuffer(raw_bytes, dtype=np.int16)
total_sec = num_frames / frame_rate

print(f"Sample Rate: {frame_rate}Hz | Channels: {num_channels} | Duration: {total_sec:.3f}s")

# Let's inspect energy profiles across 0.5s windows
window_size = int(frame_rate * 0.25)
energies = []
for i in range(0, len(audio_data), window_size):
    chunk = audio_data[i:i+window_size]
    if len(chunk) > 0:
        rms = np.sqrt(np.mean(chunk.astype(float)**2))
        t_mid = (i + len(chunk)/2) / frame_rate
        energies.append((round(t_mid, 2), round(rms, 1)))

# Find peaks and deep valleys (pauses)
silence_threshold = 400.0  # RMS threshold for pauses
pause_regions = []
in_pause = False
p_start = 0.0

for t, rms in energies:
    if rms < silence_threshold and not in_pause:
        in_pause = True
        p_start = t
    elif rms >= silence_threshold and in_pause:
        in_pause = False
        if t - p_start >= 0.25:
            pause_regions.append((round(p_start, 2), round(t, 2), round(t - p_start, 2)))

print(f"\nDetected {len(pause_regions)} noticeable pauses (>= 0.25s):")
for p in pause_regions:
    print(f"  Pause at {p[0]:5.2f}s - {p[1]:5.2f}s (duration: {p[2]:4.2f}s)")
