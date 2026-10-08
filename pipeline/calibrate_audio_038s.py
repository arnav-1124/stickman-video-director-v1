import os
import re
import subprocess
from pathlib import Path

raw_audio = Path("projects/long/ep02_how_humans_invented_the_first_lie/audio/voiceover.wav")
output_audio = Path("projects/long/ep02_how_humans_invented_the_first_lie/audio/voiceover_038s_calibrated.wav")
temp_dir = Path("temp/calibrated_038s_ep02")
temp_dir.mkdir(parents=True, exist_ok=True)

# 1. Detect silences
cmd = [
    "ffmpeg", "-i", str(raw_audio),
    "-af", "silencedetect=noise=-30dB:d=0.25",
    "-f", "null", "-"
]
res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
events = []
for l in res.stderr.split('\n'):
    if 'silence_start:' in l:
        m = re.search(r'silence_start:\s*([0-9.]+)', l)
        if m: events.append(('silence_start', float(m.group(1))))
    elif 'silence_end:' in l:
        m = re.search(r'silence_end:\s*([0-9.]+)', l)
        if m: events.append(('silence_end', float(m.group(1))))

dur = float(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", str(raw_audio)
]).decode().strip())

# Pair silences
silences = []
i = 0
while i < len(events):
    if events[i][0] == 'silence_start':
        s_start = events[i][1]
        if i + 1 < len(events) and events[i+1][0] == 'silence_end':
            s_end = events[i+1][1]
            silences.append((s_start, s_end))
            i += 2
            continue
    i += 1

speech_intervals = []
last_end = 0.0
for s_start, s_end in silences:
    if s_start > last_end + 0.15:
        speech_intervals.append((last_end, s_start))
    last_end = s_end

if last_end < dur - 0.15:
    speech_intervals.append((last_end, dur))

print(f"Extracted {len(speech_intervals)} distinct speech intervals.")

# 2. Extract speech chunks with 15ms anti-click micro-fades
clip_files = []
for idx, (st, en) in enumerate(speech_intervals, 1):
    chunk_dur = en - st
    clip_p = temp_dir / f"chunk_{idx:03d}.wav"
    fade_cmd = [
        "ffmpeg", "-y", "-ss", f"{st:.3f}", "-i", str(raw_audio),
        "-t", f"{chunk_dur:.3f}",
        "-af", f"afade=t=in:st=0:d=0.015,afade=t=out:st={chunk_dur-0.015:.3f}:d=0.015",
        str(clip_p)
    ]
    subprocess.run(fade_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    clip_files.append(clip_p)

# 3. Create exact 0.380s silence buffer
silence_file = temp_dir / "silence_038s.wav"
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
    "-t", "0.380", str(silence_file)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 4. Generate concat manifest
concat_list = temp_dir / "concat_038s.txt"
with open(concat_list, "w", encoding="utf-8") as f:
    for idx, cf in enumerate(clip_files):
        f.write(f"file '{cf.resolve().as_posix()}'\n")
        # Add 0.38s silence between chunks, but not after the last chunk
        if idx < len(clip_files) - 1:
            f.write(f"file '{silence_file.resolve().as_posix()}'\n")

# 5. Concat to master calibrated audio
concat_cmd = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", str(concat_list),
    "-c:a", "pcm_s16le", str(output_audio)
]
subprocess.run(concat_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Also export high-quality MP3 for quick playback/preview
output_mp3 = output_audio.with_suffix(".mp3")
subprocess.run([
    "ffmpeg", "-y", "-i", str(output_audio),
    "-b:a", "192k", str(output_mp3)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

new_dur = float(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", str(output_audio)
]).decode().strip())

print("=" * 60)
print(f"CALIBRATION COMPLETE (Exact 0.38s Pacing Standard)")
print("=" * 60)
print(f"Original Audio Duration: {dur:.2f}s")
print(f"Calibrated 0.38s Duration: {new_dur:.2f}s")
print(f"Dead Air Eliminated: {dur - new_dur:.2f}s of awkward pauses removed!")
print(f"Output File: {output_audio.resolve()}")
print("=" * 60)
