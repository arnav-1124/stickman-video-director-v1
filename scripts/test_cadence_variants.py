import asyncio
import subprocess
from pathlib import Path
import edge_tts

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"

shots_test = [
    (1, "Chapter One: The Pedestal Paradox."),
    (2, "Have you ever noticed a strange and painful pattern in modern relationships?"),
    (3, "The person who texts you back in three seconds flat."),
    (4, "The person who agrees with everything you say."),
    (5, "The person who rearranges their entire schedule just to see you for twenty minutes."),
    (6, "On paper, they are doing everything right.")
]

scratch_dir = Path("scratch/cadence_test")
scratch_dir.mkdir(parents=True, exist_ok=True)

async def generate_variants():
    for rate_label, rate in [("12pct", "+12%"), ("15pct", "+15%")]:
        print(f"\n--- Testing Rate: {rate} ---")
        concat_lines = []
        for sid, text in shots_test:
            raw_mp3 = scratch_dir / f"shot_{sid:02d}_{rate_label}_raw.mp3"
            trim_mp3 = scratch_dir / f"shot_{sid:02d}_{rate_label}.mp3"
            
            comm = edge_tts.Communicate(text, VOICE, pitch=PITCH, rate=rate)
            await comm.save(str(raw_mp3))
            
            # Trim trailing silence leaving 0.18s natural acoustic cushion
            cmd_trim = [
                "ffmpeg", "-y", "-i", str(raw_mp3),
                "-af", "areverse,silenceremove=start_periods=1:start_duration=0.1:start_threshold=-35dB,areverse,apad=pad_dur=0.18",
                str(trim_mp3)
            ]
            subprocess.run(cmd_trim, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
            dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(trim_mp3)]).decode().strip())
            print(f"  Shot {sid:02d} ({dur:.2f}s): {text[:40]}...")
            concat_lines.append(f"file '{trim_mp3.name}'")
        
        # Concat the 6 shots into a master sample
        concat_txt = scratch_dir / f"concat_{rate_label}.txt"
        with open(concat_txt, "w") as f:
            for l in concat_lines:
                f.write(l + "\n")
        
        master_sample = scratch_dir / f"sample_{rate_label}_master.mp3"
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy",
            str(master_sample)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        total_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(master_sample)]).decode().strip())
        print(f"  -> Total 6-shot sample ({rate}): {total_dur:.2f}s (vs original 23.16s)")

if __name__ == "__main__":
    asyncio.run(generate_variants())
