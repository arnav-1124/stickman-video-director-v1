import asyncio
import subprocess
from pathlib import Path
import edge_tts

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"

test_cases = [
    ("shot_02", "Have you ever noticed a strange and painful pattern in modern relationships?"),
    ("shot_07", "They are kind, attentive, and consistently present."),
    ("shot_10", "Their enthusiasm feels exhausting."),
    ("shot_31", "Think about what happens when you place another human being on a pedestal. The moment you put someone above you, you are forced to look up at them. And more importantly, they are forced to look down at you.")
]

test_dir = Path("scratch/pacing_tests")
test_dir.mkdir(parents=True, exist_ok=True)

rates = ["+2%", "+8%", "+12%", "+15%", "+18%"]

async def run_tests():
    print(f"{'Shot':<8} | {'Rate':<6} | {'Duration (s)':<12} | {'WPM':<8} | File")
    print("-" * 65)
    for name, text in test_cases:
        words = len(text.split())
        for r in rates:
            safe_r = r.replace("+", "plus").replace("%", "pct")
            out_file = test_dir / f"{name}_{safe_r}.mp3"
            comm = edge_tts.Communicate(text, VOICE, pitch=PITCH, rate=r)
            await comm.save(str(out_file))
            
            cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_file)]
            dur = float(subprocess.check_output(cmd).decode().strip())
            wpm = (words / dur) * 60
            print(f"{name:<8} | {r:<6} | {dur:<12.2f} | {wpm:<8.1f} | {out_file.name}")
        print("-" * 65)

if __name__ == "__main__":
    asyncio.run(run_tests())
