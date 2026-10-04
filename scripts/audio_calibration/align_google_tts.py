import json
import re
import subprocess
from pathlib import Path

PROJECT_DIR = Path("projects/shorts/ep05_how_to_handle_disrespect")
AUDIO_FILE = PROJECT_DIR / "audio" / "voiceover_googleTTS.wav"
SCRIPT_FILE = PROJECT_DIR / "script.txt"
STORYBOARD_FILE = PROJECT_DIR / "storyboard.json"

def get_silence_intervals(audio_path):
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", "silencedetect=noise=-30dB:d=0.25",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, check=True)
    lines = res.stderr.splitlines()
    
    silences = []
    for line in lines:
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([0-9.]+)", line)
            if m:
                s_start = float(m.group(1))
        elif "silence_end:" in line:
            m = re.search(r"silence_end:\s*([0-9.]+)", line)
            if m:
                s_end = float(m.group(1))
                silences.append((s_start, s_end))
    return silences

def main():
    print(f"Analyzing {AUDIO_FILE}...")
    
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]
        
    silences = get_silence_intervals(AUDIO_FILE)
    print(f"Found {len(silences)} pause gaps in audio.")
    
    # ffprobe total duration
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(AUDIO_FILE)]
    total_dur = float(subprocess.check_output(cmd).decode().strip())
    print(f"Total audio duration: {total_dur:.3f}s")
    
    # We have 19 sentences. Let's find the sentence boundaries:
    # Sentence 1 ends around silence 1 (~5.7s)
    # Sentence 2 ends around silence 2 (~7.1s)
    # ...
    # Sentence 19 ends at total_dur (53.36s)
    
    # Let's verify and construct 19 sentence split points:
    # Key pause split points:
    split_points = [
        5.73,   # 1. "What do you actually do when someone makes a slick joke at your expense in front of everyone at a friend’s house?"
        7.17,   # 2. "Most guys freeze."
        9.83,   # 3. "You either laugh along nervously to keep the peace,"
        12.17,  # 4. "or you get angry and ruin the whole vibe."
        15.51,  # 5. "Look, both reactions hand all your power to them."
        18.17,  # 6. "Fake-laughing says you accept disrespect."
        20.42,  # 7. "Getting angry shows they rattled you."
        23.45,  # 8. "Here’s what an experienced senior will tell you."
        26.11,  # 9. "Don’t get mad, and don’t raise your voice."
        29.68,  # 10. "Just look at them calmly, and ask with quiet curiosity:"
        32.20,  # 11. "Wait, I didn’t get it. What’s the joke?"
        34.03,  # 12. "Notice what happens next."
        36.19,  # 13. "The whole room goes quiet."
        39.21,  # 14. "Sarcasm only survives on quick laughter."
        42.05,  # 15. "The moment you force someone to explain their insult,"
        44.30,  # 16. "they have to admit they were just being petty."
        47.27,  # 17. "They'll mumble, backpedal, and fold on the spot."
        50.00,  # 18. "You don’t need to fight to command respect."
        53.36   # 19. "Just hold up the mirror, and let them dismantle themselves."
    ]
    
    # Sentence durations:
    sent_durations = []
    prev = 0.0
    for sp in split_points:
        sent_durations.append(round(sp - prev, 3))
        prev = sp
        
    print("\nSentence Durations:")
    for i, (text, dur) in enumerate(zip(sentences, sent_durations), 1):
        print(f"  Beat {i:02d}: {dur:5.2f}s | {text[:45]}...")
        
    # Map to 23 visual cuts:
    # Beat 1 (5.73s): Cut 1 (3.20s), Cut 2 (2.53s)
    # Beat 2 (1.44s): Cut 3 (1.44s)
    # Beat 3 (2.66s): Cut 4 (2.66s)
    # Beat 4 (2.34s): Cut 5 (2.34s)
    # Beat 5 (3.34s): Cut 6 (3.34s)
    # Beat 6 (2.66s): Cut 7 (2.66s)
    # Beat 7 (2.25s): Cut 8 (2.25s)
    # Beat 8 (3.03s): Cut 9 (3.03s)
    # Beat 9 (2.66s): Cut 10 (2.66s)
    # Beat 10 (3.57s): Cut 11 (1.40s), Cut 12 (2.17s)
    # Beat 11 (2.52s): Cut 13 (1.20s), Cut 14 (1.32s)
    # Beat 12 (1.83s): Cut 15 (1.83s)
    # Beat 13 (2.16s): Cut 16 (2.16s)
    # Beat 14 (3.02s): Cut 17 (3.02s)
    # Beat 15 (2.84s): Cut 18 (2.84s)
    # Beat 16 (2.25s): Cut 19 (2.25s)
    # Beat 17 (2.97s): Cut 20 (2.97s)
    # Beat 18 (2.73s): Cut 21 (2.73s)
    # Beat 19 (3.36s): Cut 22 (1.50s), Cut 23 (1.86s)
    
    cut_durations = [
        3.20, 2.53,  # Beat 1
        1.44,        # Beat 2
        2.66,        # Beat 3
        2.34,        # Beat 4
        3.34,        # Beat 5
        2.66,        # Beat 6
        2.25,        # Beat 7
        3.03,        # Beat 8
        2.66,        # Beat 9
        1.40, 2.17,  # Beat 10
        1.20, 1.32,  # Beat 11
        1.83,        # Beat 12
        2.16,        # Beat 13
        3.02,        # Beat 14
        2.84,        # Beat 15
        2.25,        # Beat 16
        2.97,        # Beat 17
        2.73,        # Beat 18
        1.50, 1.86   # Beat 19
    ]
    
    total_cuts_dur = sum(cut_durations)
    print(f"\nTotal 23 Cuts Duration: {total_cuts_dur:.2f}s (Audio total: {total_dur:.2f}s)")
    
    # Update storyboard.json
    with open(STORYBOARD_FILE, "r", encoding="utf-8") as f:
        sb = json.load(f)
        
    sb["target_duration_sec"] = total_dur
    for i, cut in enumerate(sb["cuts"]):
        cut["duration"] = cut_durations[i]
        
    with open(STORYBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(sb, f, indent=2)
        
    # Update concat_en_23.txt
    concat_lines = []
    for i, dur in enumerate(cut_durations, 1):
        concat_lines.append(f"file 'slides/slide_{i:02d}.png'")
        concat_lines.append(f"duration {dur:.3f}")
    concat_lines.append(f"file 'slides/slide_{len(cut_durations):02d}.png'")
    
    with open(PROJECT_DIR / "concat_en_23.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(concat_lines) + "\n")
        
    # Update build_manifest.json
    with open(PROJECT_DIR / "build_manifest.json", "r", encoding="utf-8") as f:
        bm = json.load(f)
        
    bm["voiceover_track"] = "audio/voiceover_googleTTS.wav"
    bm["total_duration"] = total_dur
    for i, clip in enumerate(bm["clips"]):
        clip["duration"] = cut_durations[i]
        
    with open(PROJECT_DIR / "build_manifest.json", "w", encoding="utf-8") as f:
        json.dump(bm, f, indent=2)
        
    print(f"\n[OK] Successfully synchronized all 23 slides to Google TTS (Ludo)! Total duration: {total_dur:.2f}s")

if __name__ == "__main__":
    main()
