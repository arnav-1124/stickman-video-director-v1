import subprocess
from pathlib import Path

test_concat = Path("scratch/test_pts_concat.txt")
durations = [2.769, 4.100, 3.124]

root = Path(__file__).resolve().parent.parent
slides_dir = root / "projects" / "long" / "ep01_why_people_fall_for_who_ignores_them" / "chapter_01_the_pedestal_paradox" / "slides"

with open(test_concat, "w") as f:
    for i, d in enumerate(durations, 1):
        f.write(f"file '{slides_dir.as_posix()}/slide_{i:02d}.jpg'\n")
        f.write(f"duration {d:.4f}\n")
    f.write(f"file '{slides_dir.as_posix()}/slide_03.jpg'\n")

out_test = Path("scratch/test_pts.mp4")
vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#FAF9F6,setsar=1,fps=30"
cmd = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", str(test_concat),
    "-vf", vf,
    "-c:v", "libx264", "-preset", "ultrafast",
    str(out_test)
]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print(res.stderr)
    exit(1)

# Probe frame packet timestamps
cmd_probe = [
    "ffprobe", "-v", "error",
    "-show_entries", "frame=pkt_pts_time,pict_type",
    "-select_streams", "v",
    "-of", "csv=p=0",
    str(out_test)
]
res = subprocess.check_output(cmd_probe).decode().splitlines()
print(f"Total frames generated: {len(res)}")
print(f"First frame PTS: {res[0]}")
print(f"Frame at ~2.769s: {res[int(2.769*30)]}")
print(f"Total video duration: {float(res[-1].split(',')[0]):.3f}s (Expected: {sum(durations):.3f}s)")
