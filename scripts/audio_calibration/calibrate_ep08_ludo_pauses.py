import re
import wave
import subprocess
from pathlib import Path

PROJECT_DIR = Path("projects/sticky_in_dark/shorts/ep08_the_toothbrush_protocol")
AUDIO_DIR = PROJECT_DIR / "audio"
RAW_WAV = AUDIO_DIR / "voiceover_ludo_raw.wav"
TEMP_CALIBRATED_WAV = AUDIO_DIR / "voiceover_ludo_trimmed.wav"
MASTER_WAV = AUDIO_DIR / "master_voiceover.wav"
MASTER_MP3 = AUDIO_DIR / "voiceover.mp3"

MAX_PAUSE_SEC = 0.18  # Maximum allowable pause in seconds (180ms)

def get_silence_intervals(audio_path, threshold_db="-28dB", min_dur=0.18):
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", f"silencedetect=noise={threshold_db}:d={min_dur}",
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

def calibrate_pauses():
    print(f"Loading {RAW_WAV} for pause calibration...")
    with wave.open(str(RAW_WAV), 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        raw_bytes = wf.readframes(n_frames)

    bytes_per_sample = n_channels * sampwidth
    silences = get_silence_intervals(RAW_WAV, threshold_db="-28dB", min_dur=MAX_PAUSE_SEC)
    print(f"Detected {len(silences)} pauses exceeding {MAX_PAUSE_SEC:.2f}s in raw audio.")

    silences.sort(key=lambda x: x[0])

    out_bytes = bytearray()
    last_idx = 0
    total_trimmed_sec = 0.0

    for s_start, s_end, dur in silences:
        start_byte = int(s_start * framerate) * bytes_per_sample
        end_byte = int(s_end * framerate) * bytes_per_sample
        
        # Audio up to start of silence
        out_bytes.extend(raw_bytes[last_idx:start_byte])

        # Keep only MAX_PAUSE_SEC of silence
        keep_bytes = int(MAX_PAUSE_SEC * framerate) * bytes_per_sample
        out_bytes.extend(raw_bytes[start_byte : start_byte + keep_bytes])

        trimmed_dur = dur - MAX_PAUSE_SEC
        total_trimmed_sec += trimmed_dur

        last_idx = end_byte

    # Add remaining audio
    out_bytes.extend(raw_bytes[last_idx:])

    with wave.open(str(TEMP_CALIBRATED_WAV), 'wb') as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(framerate)
        wf.writeframes(out_bytes)

    raw_dur = len(raw_bytes) / (framerate * bytes_per_sample)
    cal_dur = len(out_bytes) / (framerate * bytes_per_sample)
    print(f"[OK] Raw duration: {raw_dur:.2f}s -> Calibrated duration: {cal_dur:.2f}s (Trimmed {total_trimmed_sec:.2f}s of dead silence!)")

    # Step 2: Apply Deep Masculine Broadcast Standard DSP (-11.9 LUFS)
    print("\nApplying Deep Masculine Broadcast Standard DSP (-11.9 LUFS)...")
    dsp_filter = (
        "highpass=f=75,"
        "equalizer=f=115:t=q:w=1.2:g=3.5,"
        "equalizer=f=250:t=q:w=1.5:g=1.8,"
        "equalizer=f=3500:t=q:w=1.0:g=2.2,"
        "acompressor=threshold=-18dB:ratio=2.5:attack=15:release=120,"
        "loudnorm=I=-11.9:TP=-1.5:LRA=7.0"
    )

    subprocess.run([
        "ffmpeg", "-y", "-i", str(TEMP_CALIBRATED_WAV),
        "-af", dsp_filter,
        "-ar", "48000", "-ac", "2",
        str(MASTER_WAV)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    subprocess.run([
        "ffmpeg", "-y", "-i", str(MASTER_WAV),
        "-b:a", "192k",
        str(MASTER_MP3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Copy to Remotion public audio as well
    remotion_audio = Path("remotion/public/audio/ep08_voiceover.wav")
    remotion_audio.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(MASTER_WAV),
        "-ar", "48000", "-ac", "2",
        str(remotion_audio)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(MASTER_WAV)]
    final_dur = float(subprocess.check_output(cmd).decode().strip())
    print(f"\n[SUCCESS] Master Google TTS Ludo voiceover created: {MASTER_WAV} ({final_dur:.2f}s at -11.9 LUFS)")
    return final_dur

if __name__ == "__main__":
    calibrate_pauses()
