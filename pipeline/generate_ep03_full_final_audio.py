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
acts_dir = ep_dir / "acts"
master_audio_dir = ep_dir / "audio"
temp_dir = root_dir / "temp/ep03_full_production"
temp_dir.mkdir(parents=True, exist_ok=True)
master_audio_dir.mkdir(parents=True, exist_ok=True)

# 5 Acts Data
acts_list = [
    "act01_the_animal_standard",
    "act02_the_savanna_baby_crisis",
    "act03_the_first_spark",
    "act04_the_brain_on_love",
    "act05_the_eternal_echo"
]

dsp_filter = (
    "equalizer=f=115:width_type=o:w=1.2:g=4.2,"
    "equalizer=f=250:width_type=o:w=1.0:g=2.0,"
    "equalizer=f=3500:width_type=o:w=1.2:g=2.5,"
    "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
    "loudnorm=I=-11.9:TP=-1.0:LRA=6.0"
)

def calibrate_and_clamp_pauses(input_wav: Path, output_wav: Path, target_pause: float = 0.280):
    cmd_silence = [
        "ffmpeg", "-i", str(input_wav),
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
        "-of", "default=noprint_wrappers=1:nokey=1", str(input_wav)
    ]).decode().strip())

    audio_segments = []
    curr_pos = 0.0

    for s_st, s_en, s_dur in silence_spans:
        if s_dur > target_pause:
            keep_end = s_st + (target_pause / 2.0)
            audio_segments.append((curr_pos, keep_end))
            curr_pos = s_en - (target_pause / 2.0)

    audio_segments.append((curr_pos, dur_raw))

    chunk_files = []
    for idx, (st, en) in enumerate(audio_segments):
        c_dur = en - st
        if c_dur <= 0.05: continue
        c_p = temp_dir / f"{input_wav.stem}_c_{idx:03d}.wav"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{st:.3f}", "-i", str(input_wav),
            "-t", f"{c_dur:.3f}", "-c", "copy", str(c_p)
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        chunk_files.append(c_p)

    concat_file = temp_dir / f"{input_wav.stem}_concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for cf in chunk_files:
            f.write(f"file '{cf.resolve().as_posix()}'\n")

    clamped_raw = temp_dir / f"{input_wav.stem}_clamped.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file), "-c", "copy", str(clamped_raw)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Master with studio DSP
    subprocess.run([
        "ffmpeg", "-y", "-i", str(clamped_raw),
        "-af", dsp_filter, "-ar", "44100", "-ac", "2",
        str(output_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


print("=================================================================")
print("  EPISODE 03: FULL & FINAL BENCHMARK AUDIO PIPELINE (ALL 5 ACTS)")
print("=================================================================\n")

final_act_wavs = []

for idx, act_id in enumerate(acts_list, 1):
    act_folder = acts_dir / act_id
    script_p = act_folder / "script.txt"
    with open(script_p, "r", encoding="utf-8") as f:
        text = f.read().strip()

    print(f"[{idx}/5] Processing {act_id}...")
    prompt = f"""## Style: High-energy, crisp, authoritative documentary narration at exactly 164 words per minute. Punchy cadence, rapid natural vocal momentum, and tight sentence transitions. Take only tiny 250-millisecond breaths at full stops. Do not take dramatic sighs or long reflective pauses. Voice of an experienced, witty psychologist with deep masculine resonance.

## Transcript:
{text}
"""
    raw_wav = temp_dir / f"{act_id}_raw.wav"
    mastered_act_wav = act_folder / "audio/voiceover.wav"
    mastered_act_mp3 = act_folder / "audio/voiceover.mp3"

    # 1. TTS Generation
    generate_tts(prompt, str(raw_wav), voice_name="Ludo")

    # 2. Benchmark Pause Clamping & DSP Mastering
    calibrate_and_clamp_pauses(raw_wav, mastered_act_wav)
    
    # Also export MP3
    subprocess.run([
        "ffmpeg", "-y", "-i", str(mastered_act_wav),
        "-b:a", "192k", str(mastered_act_mp3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(mastered_act_wav)
    ]).decode().strip())
    print(f"  -> {act_id} mastered: {dur:.2f}s ({mastered_act_wav.name})")
    final_act_wavs.append(mastered_act_wav)

# Assemble Master Full Video Audio Track
print("\n--- Assembling Full-Fledged Master Film Audio Track ---")
master_concat = master_audio_dir / "master_concat_list.txt"
with open(master_concat, "w", encoding="utf-8") as f:
    for aw in final_act_wavs:
        f.write(f"file '{aw.resolve().as_posix()}'\n")

final_master_wav = master_audio_dir / "master_voiceover.wav"
final_master_mp3 = master_audio_dir / "master_voiceover.mp3"

subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", str(master_concat), "-c", "copy",
    str(final_master_wav)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

subprocess.run([
    "ffmpeg", "-y", "-i", str(final_master_wav),
    "-b:a", "192k", str(final_master_mp3)
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

total_dur = float(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", str(final_master_wav)
]).decode().strip())

m, s = int(total_dur // 60), int(total_dur % 60)

print("\n" + "=" * 65)
print("  EPISODE 03: FULL & FINAL AUDIO MASTER COMPLETE!")
print("=" * 65)
print(f"Total Master Film Duration: {total_dur:.2f}s ({m}m {s:02d}s)")
print(f"Master WAV:                 {final_master_wav}")
print(f"Master MP3:                 {final_master_mp3}")
print("=================================================================")
