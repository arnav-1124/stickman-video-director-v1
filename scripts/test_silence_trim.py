import subprocess
from pathlib import Path

test_files = [
    "scratch/pacing_tests/shot_02_plus15pct.mp3",
    "scratch/pacing_tests/shot_07_plus15pct.mp3",
    "scratch/pacing_tests/shot_10_plus15pct.mp3",
    "scratch/pacing_tests/shot_31_plus15pct.mp3"
]

out_dir = Path("scratch/pacing_trimmed")
out_dir.mkdir(parents=True, exist_ok=True)

for f in test_files:
    p = Path(f)
    out_trimmed = out_dir / p.name
    
    # FFmpeg filter:
    # 1. areverse -> remove leading silence (which was trailing silence) -> areverse
    # This trims excessive silence at the end while preserving a crisp 120ms fade/cushion.
    # Alternatively silenceremove from end:
    cmd = [
        "ffmpeg", "-y", "-i", str(p),
        "-af", "areverse,silenceremove=start_periods=1:start_duration=0.1:start_threshold=-35dB,areverse,apad=pad_dur=0.15",
        str(out_trimmed)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    dur_orig = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(p)]).decode().strip())
    dur_trim = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_trimmed)]).decode().strip())
    print(f"{p.name:<25} | Orig: {dur_orig:.2f}s -> Trimmed+Cushion: {dur_trim:.2f}s (Saved {dur_orig - dur_trim:.2f}s)")
