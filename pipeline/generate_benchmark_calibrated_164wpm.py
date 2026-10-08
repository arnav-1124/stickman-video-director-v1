import os
import re
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir / "pipeline"))

from generate_gemini_tts import generate_tts

load_dotenv(root_dir / ".env")

ep_dir = root_dir / "projects/long/ep03_how_humans_first_fell_in_love"
test_output_dir = ep_dir / "audio/act1_2_tests"
test_output_dir.mkdir(parents=True, exist_ok=True)
temp_dir = root_dir / "temp/benchmark_164wpm"
temp_dir.mkdir(parents=True, exist_ok=True)

# 1. Cleaned Act 1 & 2 Script (Removed dramatic ellipses and mid-clause dash breaks that cause TTS to stall)
clean_transcript = """In ninety-seven percent of all mammal species on Earth, romance does not exist.
A male grizzly bear or a lion mates for thirty seconds, turns around, and disappears into the forest forever.
No awkward text messages. No second dates. No staying awake until three in the morning wondering what they're thinking.
In the wild, nature values speed, efficiency, and moving on.
So why on Earth did human beings evolve this sweaty-palmed, obsessive, heart-pounding insanity called falling in love?
If nature only cared about survival, love is an absolute disaster.
It makes you clumsy. It makes you reckless. It makes grown adults write terrible poetry and stare blankly at their phones.
To understand why your brain does this, you have to travel back four million years ago, to the sun-scorched African savanna.
Back then, our ape-like ancestors made a monumental decision: they stood up on two feet.
Walking upright was brilliant for spotting predators and traveling long distances.
There was only one catastrophic catch: it narrowed the female pelvis.
At the exact same time, hominid brains were rapidly ballooning in size.
And that created an evolutionary nightmare known as the Obstetric Dilemma.
If a human baby stayed inside the womb until its brain was fully developed, it would physically kill the mother during birth.
So nature was forced into a desperate compromise:
Human babies must be born prematurely. Completely, utterly helpless.
A baby horse can stand and run thirty minutes after birth.
A human newborn cannot even support the weight of its own neck for four months.
Now put that helpless baby into an ancient savanna crawling with saber-toothed cats, hyenas, and lethal droughts.
A mother carrying a crying, defenseless infant could not hunt, run, or dig for roots alone. Without constant help, she would starve.
And the male hunters? In the animal world, a male has zero incentive to share his food. You eat your kill, and you survive.
Evolution hit a biological dead end:
Either human beings would go completely extinct, or nature had to invent an emotional superglue so powerful it could force a selfish hunter to stay for years.
That superglue was romantic love."""

print("=================================================================")
print("  GENERATING 164 WPM BENCHMARK-CALIBRATED AUDIO (ACT 1 & 2)")
print("=================================================================\n")

# Targeted 164 WPM Prompt based on forensic benchmark analysis
prompt_164wpm = f"""## Style: High-energy, crisp, authoritative documentary narration at exactly 164 words per minute. Punchy cadence, rapid natural vocal momentum, and tight sentence transitions. Take only tiny 250-millisecond breaths at full stops. Do not take dramatic sighs or long reflective pauses. Voice of an experienced, witty psychologist with deep masculine resonance.

## Transcript:
{clean_transcript}
"""

raw_tts_wav = temp_dir / "raw_tts_164wpm.wav"

print("[1/3] Synthesizing Voiceover with Gemini Flash TTS (Ludo @ 164 WPM)...")
generate_tts(prompt_164wpm, str(raw_tts_wav), voice_name="Ludo")

# 2. Benchmark Pause Clamping (Ensuring no pause exceeds 0.29s, matching benchmark 0.288s median)
print("\n[2/3] Clamping Pauses to Benchmark Gold Standard (Max 0.285s)...")

# Detect silence periods in raw TTS
cmd_silence = [
    "ffmpeg", "-i", str(raw_tts_wav),
    "-af", "silencedetect=noise=-30dB:d=0.20",
    "-f", "null", "-"
]
res = subprocess.run(cmd_silence, stderr=subprocess.PIPE, text=True)

silence_spans = []
starts = []
for line in res.stderr.split('\n'):
    m_s = re.search(r'silence_start:\s*([0-9.]+)', line)
    m_e = re.search(r'silence_end:\s*([0-9.]+)\s*\|\s*silence_duration:\s*([0-9.]+)', line)
    if m_s:
        starts.append(float(m_s.group(1)))
    if m_e:
        st = starts.pop(0) if starts else 0
        en = float(m_e.group(1))
        dur = float(m_e.group(2))
        silence_spans.append((st, en, dur))

dur_raw = float(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", str(raw_tts_wav)
]).decode().strip())

# We clamp any silence > 0.285s down to 0.280s
# To do this cleanly without slicing words:
# If silence > 0.285s, we trim (dur - 0.280s) from the silence center
target_pause = 0.280
audio_segments_to_keep = []
curr_pos = 0.0

for s_st, s_en, s_dur in silence_spans:
    if s_dur > target_pause:
        # Keep speech up to silence start + half target pause
        keep_end = s_st + (target_pause / 2.0)
        audio_segments_to_keep.append((curr_pos, keep_end))
        # Skip excess dead air
        curr_pos = s_en - (target_pause / 2.0)
    else:
        # Keep as is
        pass

audio_segments_to_keep.append((curr_pos, dur_raw))

# Export segments and concat
seg_files = []
for idx, (st, en) in enumerate(audio_segments_to_keep):
    seg_dur = en - st
    if seg_dur <= 0.05: continue
    seg_p = temp_dir / f"clean_seg_{idx:03d}.wav"
    subprocess.run([
        "ffmpeg", "-y", "-ss", f"{st:.3f}", "-i", str(raw_tts_wav),
        "-t", f"{seg_dur:.3f}",
        "-c", "copy",
        str(seg_p)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    seg_files.append(seg_p)

concat_list = temp_dir / "concat_clamped.txt"
with open(concat_list, "w", encoding="utf-8") as f:
    for sf in seg_files:
        f.write(f"file '{sf.resolve().as_posix()}'\n")

clamped_wav = temp_dir / "clamped_164wpm.wav"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", str(concat_list),
    "-c", "copy",
    str(clamped_wav)
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# 3. Master with studio DSP chain
print("\n[3/3] Applying Studio DSP Mastering Chain...")
dsp_filter = (
    "equalizer=f=115:width_type=o:w=1.2:g=4.2,"
    "equalizer=f=250:width_type=o:w=1.0:g=2.0,"
    "equalizer=f=3500:width_type=o:w=1.2:g=2.5,"
    "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
    "loudnorm=I=-11.9:TP=-1.0:LRA=6.0"
)

output_wav = test_output_dir / "act1_2_164wpm_benchmark_calibrated.wav"
output_mp3 = test_output_dir / "act1_2_164wpm_benchmark_calibrated.mp3"

subprocess.run([
    "ffmpeg", "-y", "-i", str(clamped_wav),
    "-af", dsp_filter,
    "-ar", "44100", "-ac", "2",
    str(output_wav)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-i", str(output_wav),
    "-b:a", "192k",
    str(output_mp3)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

final_dur = float(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", str(output_wav)
]).decode().strip())

words_count = len(clean_transcript.split())
effective_wpm = round((words_count / (final_dur / 60)), 1)
m, s = int(final_dur // 60), int(final_dur % 60)

print("\n" + "=" * 65)
print("  BENCHMARK-CALIBRATED 164 WPM AUDIO COMPLETE!")
print("=" * 65)
print(f"Total Words Spoken:         {words_count} words")
print(f"Final Audio Runtime:        {final_dur:.2f}s ({m}m {s:02d}s)")
print(f"Effective Speaking Cadence: {effective_wpm} WPM (Target: ~164 WPM)")
print(f"Max Pause Duration:         Capped strictly at ~0.28s")
print(f"WAV File:                   {output_wav}")
print(f"MP3 File:                   {output_mp3}")
print("=" * 65)
