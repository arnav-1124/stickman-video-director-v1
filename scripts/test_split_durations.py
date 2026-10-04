import asyncio
import edge_tts
import subprocess
from pathlib import Path

VOICE = "en-US-ChristopherNeural"
PITCH = "-2Hz"
RATE = "+5%"

test_clauses = [
    ("Line 6", "One student is desperate for an A-plus."),
    ("Line 7", "He stays up until three in the morning formatting slides, worrying about fonts, and sweating every detail."),
    ("Line 18", "They smile too broadly."),
    ("Line 19", "They follow you down the aisle."),
    ("Line 20", "They offer you discounts before you even inspect the price tag."),
    ("Line 21", "Even if the product they are selling is decent, what is your immediate reflex?"),
    ("Line 22", "You want to back away."),
    ("Line 23", "You feel suspicious."),
    ("Line 25", "Desperate enthusiasm always feels like an invisible trap."),
    ("Line 26", "It signals that the seller needs something from you more than you need something from them."),
    ("Line 27", "When a person ignores you, or simply doesn't rush to cater to your every mood, they trigger the exact opposite reaction."),
    ("Line 28", "They signal emotional self-sufficiency."),
    ("Line 30", "They have their own orbit."),
    ("Line 31", "They are not auditioning for your approval."),
    ("Line 32", "And because they refuse to sell themselves, you immediately assume the product must be of immense value.")
]

async def measure():
    print("Exact Sentence Durations with edge_tts:")
    print("=" * 60)
    for label, text in test_clauses:
        comm = edge_tts.Communicate(text, VOICE, pitch=PITCH, rate=RATE)
        temp_file = Path("test_temp.mp3")
        await comm.save(str(temp_file))
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(temp_file)]
        dur = float(subprocess.run(cmd, stdout=subprocess.PIPE, text=True).stdout.strip())
        print(f"{label:8} | {dur:4.2f}s | \"{text}\"")
        if temp_file.exists():
            temp_file.unlink()

asyncio.run(measure())
