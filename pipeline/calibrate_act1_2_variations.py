import os
import re
import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
ep_dir = root_dir / "projects/long/ep03_how_humans_first_fell_in_love"
acts_dir = ep_dir / "acts"
test_output_dir = ep_dir / "audio/act1_2_tests"
test_output_dir.mkdir(parents=True, exist_ok=True)
temp_dir = root_dir / "temp/act1_2_calibrate"
temp_dir.mkdir(parents=True, exist_ok=True)

# 1. Combine Act 1 and Act 2 raw audio
act1_raw = acts_dir / "act01_the_animal_standard/audio/voiceover_raw.wav"
act2_raw = acts_dir / "act02_the_savanna_baby_crisis/audio/voiceover_raw.wav"

combined_raw = temp_dir / "act1_2_raw_combined.wav"
concat_manifest = temp_dir / "concat_raw.txt"

with open(concat_manifest, "w", encoding="utf-8") as f:
    f.write(f"file '{act1_raw.resolve().as_posix()}'\n")
    f.write(f"file '{act2_raw.resolve().as_posix()}'\n")

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", str(concat_manifest),
    "-c", "copy",
    str(combined_raw)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 2. Detect all silence intervals
print("[1/4] Detecting silences across combined Act 1 & 2...")
cmd_silence = [
    "ffmpeg", "-i", str(combined_raw),
    "-af", "silencedetect=noise=-30dB:d=0.18",
    "-f", "null", "-"
]
res = subprocess.run(cmd_silence, stderr=subprocess.PIPE, text=True)

events = []
for line in res.stderr.split('\n'):
    if 'silence_start:' in line:
        m = re.search(r'silence_start:\s*([0-9.]+)', line)
        if m: events.append(('silence_start', float(m.group(1))))
    elif 'silence_end:' in line:
        m = re.search(r'silence_end:\s*([0-9.]+)', line)
        if m: events.append(('silence_end', float(m.group(1))))

probe_dur = [
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", str(combined_raw)
]
total_dur = float(subprocess.check_output(probe_dur).decode().strip())

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
    if s_start > last_end + 0.12:
        speech_intervals.append((last_end, s_start))
    last_end = s_end

if last_end < total_dur - 0.12:
    speech_intervals.append((last_end, total_dur))

print(f"Extracted {len(speech_intervals)} speech chunks across Act 1 & 2.")

# 3. Extract and accelerate each speech chunk slightly (atempo=1.065 ~ 6.5% speed increase)
speed_factor = 1.065
print(f"[2/4] Accelerating speech chunks by {speed_factor}x (natural energetic cadence)...")

chunks_accelerated = []
for idx, (st, en) in enumerate(speech_intervals, 1):
    chunk_dur = en - st
    chunk_p = temp_dir / f"chunk_acc_{idx:03d}.wav"
    fade_cmd = [
        "ffmpeg", "-y", "-ss", f"{st:.3f}", "-i", str(combined_raw),
        "-t", f"{chunk_dur:.3f}",
        "-af", f"atempo={speed_factor},afade=t=in:st=0:d=0.012,afade=t=out:st={(chunk_dur/speed_factor)-0.012:.3f}:d=0.012",
        "-ar", "44100", "-ac", "2",
        str(chunk_p)
    ]
    subprocess.run(fade_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    chunks_accelerated.append(chunk_p)

# DSP filter for master broadcast polish
dsp_filter = (
    "equalizer=f=115:width_type=o:w=1.2:g=4.2,"
    "equalizer=f=250:width_type=o:w=1.0:g=2.0,"
    "equalizer=f=3500:width_type=o:w=1.2:g=2.5,"
    "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
    "loudnorm=I=-11.9:TP=-1.0:LRA=6.0"
)

# Function to build calibrated version
def build_version(pause_sec: float, label: str):
    print(f"\n[3/4] Building {label} (max pause = {pause_sec:.3f}s)...")
    silence_p = temp_dir / f"silence_{int(pause_sec*1000)}ms.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", f"{pause_sec:.3f}", str(silence_p)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    concat_list = temp_dir / f"concat_{label}.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for idx, cf in enumerate(chunks_accelerated):
            f.write(f"file '{cf.resolve().as_posix()}'\n")
            if idx < len(chunks_accelerated) - 1:
                f.write(f"file '{silence_p.resolve().as_posix()}'\n")
                
    raw_calibrated = temp_dir / f"raw_{label}.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(raw_calibrated)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Master with DSP chain
    final_wav = test_output_dir / f"act1_2_combined_{label}.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_calibrated),
        "-af", dsp_filter,
        "-ar", "44100", "-ac", "2",
        str(final_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Also export MP3 for direct preview
    final_mp3 = test_output_dir / f"act1_2_combined_{label}.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-i", str(final_wav),
        "-b:a", "192k",
        str(final_mp3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    out_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(final_wav)
    ]).decode().strip())
    
    m, s = int(out_dur // 60), int(out_dur % 60)
    print(f"  -> Generated {label}: {final_wav.name} ({out_dur:.2f}s / {m}m {s:02d}s)")
    return final_wav, final_mp3, out_dur

# Build Version 1: 0.320s pacing
v1_wav, v1_mp3, v1_dur = build_version(0.320, "pacing_032s_faster")

# Build Version 2: 0.300s pacing
v2_wav, v2_mp3, v2_dur = build_version(0.300, "pacing_030s_faster")

print("\n=========================================================")
print("  ACT 1 & 2 PACING VARIATIONS GENERATED SUCCESSFULLY!")
print("=========================================================")
print(f"Original Raw Act 1+2 Duration: {total_dur:.2f}s")
print(f"Version A (0.32s Pause + 1.065x Speed): {v1_dur:.2f}s -> {v1_wav}")
print(f"Version B (0.30s Pause + 1.065x Speed): {v2_dur:.2f}s -> {v2_wav}")
print("=========================================================")
