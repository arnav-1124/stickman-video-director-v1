import asyncio
import subprocess
from pathlib import Path
import edge_tts

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"
RATE = "+5%"

test_sentences = [
    (1, "Chapter One: The Pedestal Paradox."),
    (2, "Have you ever noticed a strange and painful pattern in modern relationships?"),
    (3, "The person who texts you back in three seconds flat."),
    (4, "The person who agrees with everything you say."),
    (5, "The person who rearranges their entire schedule just to see you for twenty minutes.")
]

scratch = Path("scratch/exact_timings")
scratch.mkdir(parents=True, exist_ok=True)

async def analyze():
    print(f"{'Shot':<6} | {'Total Dur':<10} | {'Last Word End':<14} | {'Trailing Gap':<14} | Sentence")
    print("-" * 75)
    for sid, text in test_sentences:
        comm = edge_tts.Communicate(text, VOICE, pitch=PITCH, rate=RATE, boundary="WordBoundary")
        raw_file = scratch / f"raw_{sid}.mp3"
        words = []
        with open(raw_file, "wb") as f:
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    start_sec = (chunk["offset"] / 10000) / 1000.0
                    end_sec = ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                    words.append((chunk["text"], start_sec, end_sec))

        dur_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(raw_file)]
        total_dur = float(subprocess.check_output(dur_cmd).decode().strip())
        last_word_text, _, last_word_end = words[-1]
        trailing_gap = total_dur - last_word_end
        print(f"#{sid:<5} | {total_dur:<10.3f} | {last_word_end:<14.3f} | {trailing_gap:<14.3f} | \"{last_word_text}\" -> {text[:30]}...")

if __name__ == "__main__":
    asyncio.run(analyze())
