import asyncio
import subprocess
from pathlib import Path
import edge_tts

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"
RATE = "+6%"  # Tested natural conversational storytelling rate
PAUSE_AFTER_WORD = 0.35  # Natural storytelling breath cushion (in seconds)

shots_test = [
    (1, "Chapter One: The Pedestal Paradox."),
    (2, "Have you ever noticed a strange and painful pattern in modern relationships?"),
    (3, "The person who texts you back in three seconds flat."),
    (4, "The person who agrees with everything you say.")
]

scratch_dir = Path("scratch/natural_pacing_test")
scratch_dir.mkdir(parents=True, exist_ok=True)

async def test_natural_pipeline():
    print("=" * 80)
    print("  EXACT WORD-BOUNDARY NATURAL PACING TEST")
    print("=" * 80)

    for sid, text in shots_test:
        raw_mp3 = scratch_dir / f"shot_{sid:02d}_raw.mp3"
        final_mp3 = scratch_dir / f"shot_{sid:02d}_clean.mp3"
        
        comm = edge_tts.Communicate(text, VOICE, pitch=PITCH, rate=RATE, boundary="WordBoundary")
        words = []
        with open(raw_mp3, "wb") as f:
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    start_sec = (chunk["offset"] / 10000) / 1000.0
                    end_sec = ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                    words.append((chunk["text"], start_sec, end_sec))

        total_raw_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(raw_mp3)]).decode().strip())
        
        last_word_text, last_word_start, last_word_end = words[-1]
        
        # Exact target duration = end of last word + natural pause (e.g. 0.35s)
        # We ensure target_dur does not exceed raw_dur
        target_dur = min(total_raw_dur, round(last_word_end + PAUSE_AFTER_WORD, 3))
        
        # Cut audio cleanly at target_dur with a tiny 0.03s soft fade-out at the very end to prevent pop
        # Notice: we DO NOT touch the audio before last_word_end! 100% of the speech is untouched!
        fade_out_start = max(0, target_dur - 0.03)
        cmd_trim = [
            "ffmpeg", "-y", "-i", str(raw_mp3),
            "-t", str(target_dur),
            "-af", f"afade=t=out:st={fade_out_start:.3f}:d=0.03",
            "-c:a", "libmp3lame", "-b:a", "192k",
            str(final_mp3)
        ]
        subprocess.run(cmd_trim, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        final_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(final_mp3)]).decode().strip())
        
        saved_dead_air = total_raw_dur - final_dur
        print(f"Shot #{sid:02d}:")
        print(f"  Text:               \"{text}\"")
        print(f"  Last Word:          \"{last_word_text}\" ends at {last_word_end:.3f}s")
        print(f"  Raw TTS Dur:        {total_raw_dur:.3f}s (had {total_raw_dur - last_word_end:.3f}s trailing dead air)")
        print(f"  Clean Final Dur:    {final_dur:.3f}s (retained full speech + {final_dur - last_word_end:.3f}s clean breath)")
        print(f"  Trimmed Dead Air:   -{saved_dead_air:.3f}s\n")

if __name__ == "__main__":
    asyncio.run(test_natural_pipeline())
