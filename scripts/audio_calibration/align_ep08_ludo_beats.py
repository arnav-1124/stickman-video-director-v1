import re
import json
import subprocess
from pathlib import Path

PROJECT_DIR = Path("projects/sticky_in_dark/shorts/ep08_the_toothbrush_protocol")
AUDIO_FILE = PROJECT_DIR / "audio" / "master_voiceover.wav"
SCRIPT_FILE = PROJECT_DIR / "script.txt"
TIMINGS_FILE = PROJECT_DIR / "audio" / "calibrated_beats_timing.json"

def get_silence_intervals(audio_path):
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", "silencedetect=noise=-28dB:d=0.10",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, check=True)
    lines = res.stderr.splitlines()

    silences = []
    current_start = None
    for line in lines:
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([0-9.]+)", line)
            if m:
                current_start = float(m.group(1))
        elif "silence_end:" in line and current_start is not None:
            m = re.search(r"silence_end:\s*([0-9.]+)", line)
            if m:
                s_end = float(m.group(1))
                dur = s_end - current_start
                silences.append((current_start, s_end, dur))
                current_start = None
    return silences

def align():
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]

    silences = get_silence_intervals(AUDIO_FILE)
    print(f"Detected {len(silences)} pause gaps in calibrated 49.86s audio.")

    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(AUDIO_FILE)]
    total_dur = float(subprocess.check_output(cmd).decode().strip())
    print(f"Total audio duration: {total_dur:.3f}s")

    # Proportionally distribute sentence durations based on syllable/word counts mapped to speech intervals
    word_counts = [len(s.split()) for s in sentences]
    total_words = sum(word_counts)

    # Let's map 20 beats across the 49.86s timeline:
    beats = []
    curr_time = 0.0

    for i, (sent, wc) in enumerate(zip(sentences, word_counts), 1):
        # Estimated proportional slice
        est_dur = (wc / total_words) * total_dur
        start_sec = round(curr_time, 2)
        end_sec = round(min(total_dur, curr_time + est_dur), 2)
        if i == len(sentences):
            end_sec = total_dur

        beats.append({
            "beat_id": i,
            "line": sent,
            "word_count": wc,
            "start_sec": start_sec,
            "end_sec": end_sec,
            "duration": round(end_sec - start_sec, 2)
        })
        curr_time = end_sec

    # Snap end_sec of each beat to the nearest silence gap
    for b in beats[:-1]:
        target = b["end_sec"]
        best_gap = None
        best_diff = 999
        for s_start, s_end, s_dur in silences:
            center = (s_start + s_end) / 2.0
            diff = abs(center - target)
            if diff < best_diff and diff < 1.2:
                best_diff = diff
                best_gap = center
        if best_gap:
            b["end_sec"] = round(best_gap, 2)
            b["duration"] = round(b["end_sec"] - b["start_sec"], 2)

    # Fix continuity
    for i in range(1, len(beats)):
        beats[i]["start_sec"] = beats[i-1]["end_sec"]
        beats[i]["duration"] = round(beats[i]["end_sec"] - beats[i]["start_sec"], 2)
    beats[-1]["end_sec"] = total_dur
    beats[-1]["duration"] = round(total_dur - beats[-1]["start_sec"], 2)

    with open(TIMINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(beats, f, indent=2)

    for b in beats:
        print(f"Beat {b['beat_id']:02d}: [{b['start_sec']:5.2f}s - {b['end_sec']:5.2f}s | {b['duration']:4.2f}s] \"{b['line'][:40]}...\"")

if __name__ == "__main__":
    align()
