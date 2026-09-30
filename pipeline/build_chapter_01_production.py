import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VOICE_EN = "en-US-ChristopherNeural"
PITCH_EN = "-2Hz"
RATE_EN = "+2%"

VOICE_HI = "hi-IN-MadhurNeural"
PITCH_HI = "+0Hz"
RATE_HI = "+20%"

PROJECT_DIR = Path("projects/long/ep01_why_people_fall_for_who_ignores_them")
CH01_DIR = PROJECT_DIR / "chapter_01_the_pedestal_paradox"
AUDIO_DIR_EN = CH01_DIR / "audio" / "en"
AUDIO_DIR_HI = CH01_DIR / "audio" / "hi"
STORYBOARD_FILE = CH01_DIR / "storyboard.json"

AUDIO_DIR_EN.mkdir(parents=True, exist_ok=True)
AUDIO_DIR_HI.mkdir(parents=True, exist_ok=True)

def get_audio_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_shot(text, out_mp3, voice, pitch, rate):
    communicate = edge_tts.Communicate(text, voice, pitch=pitch, rate=rate)
    await communicate.save(str(out_mp3))

async def main():
    with open(STORYBOARD_FILE, "r", encoding="utf-8") as f:
        sb_data = json.load(f)

    shots = sb_data["shots"]
    print(f"Loaded {len(shots)} shots for Chapter 1.")

    total_dur_en = 0.0

    for s in shots:
        shot_id = s["shot_id"]
        clause = s["spoken_clause"].strip()

        # Handle chapter title cleanly
        if clause.startswith("[CHAPTER"):
            speech_text = "Chapter One: The Pedestal Paradox."
        else:
            speech_text = clause

        out_mp3_en = AUDIO_DIR_EN / f"shot_{shot_id:03d}.mp3"
        print(f"Generating EN audio for Shot {shot_id:03d}: '{speech_text[:40]}...'")
        await synthesize_shot(speech_text, out_mp3_en, VOICE_EN, PITCH_EN, RATE_EN)

        dur = get_audio_duration(out_mp3_en)
        # Pad duration by 0.35s for clean acoustic breathing room
        padded_dur = round(dur + 0.35, 2)
        s["duration_sec"] = padded_dur
        s["audio_file_en"] = f"audio/en/shot_{shot_id:03d}.mp3"
        total_dur_en += padded_dur

    # Save updated storyboard with exact measured durations
    with open(STORYBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(sb_data, f, indent=2)

    print(f"\nAll 36 EN audio files generated!")
    print(f"Total Chapter 1 Measured Duration: {total_dur_en:.2f}s ({total_dur_en/60:.2f} mins)")

    # Build quick_batch_copypaste.txt for Google Flow AI (Nano Banana Pro)
    batch_file = CH01_DIR / "quick_batch_copypaste.txt"
    with open(batch_file, "w", encoding="utf-8") as bf:
        bf.write("==================================================================\n")
        bf.write("  EPISODE 01 - CHAPTER 01: THE PEDESTAL PARADOX\n")
        bf.write("  Model: Nano Banana Pro (Gemini 3 Pro Image) via Google Flow\n")
        bf.write("  Aspect Ratio: 16:9 Widescreen (1920x1080) for all 36 scene slides\n")
        bf.write("  Style: Minimal Hand-Drawn 2D Comic Doodle (Ink Explainer DNA)\n")
        bf.write(f"  Total Slides: {len(shots)} | Measured Duration: {total_dur_en:.1f}s\n")
        bf.write("==================================================================\n\n")

        for s in shots:
            shot_id = s["shot_id"]
            title = s["title"]
            dur = s["duration_sec"]
            clause = s["spoken_clause"]
            comp = s["visual_composition_16_9"].replace("\n", " ").strip()
            accent = s.get("color_accent", "").replace("\n", " ").strip()
            cam = s.get("camera_movement", "").replace("\n", " ").strip()

            # Determine appropriate master asset references
            refs = []
            if "SOVEREIGN" in comp or "CHAR_01" in comp or "backbencher" in comp.lower() or "sovereign" in comp.lower():
                refs.append("@char_01_sovereign.jpg")
            if "OVERGIVER" in comp or "CHAR_02" in comp or "eager" in comp.lower() or "pedestal" in comp.lower() or "text" in comp.lower():
                refs.append("@char_02_overgiver.jpg")
            if "OBSERVER" in comp or "CHAR_03" in comp or "girl" in comp.lower() or "female" in comp.lower():
                refs.append("@char_03_observer.jpg")
            if "bed" in comp.lower() or "02:14" in comp.lower() or "night" in comp.lower():
                refs.append("@env_01_bedroom.jpg")
            if "pedestal" in comp.lower() or "column" in comp.lower() or "pillar" in comp.lower():
                refs.append("@env_06_pedestal_pillar.jpg")
            if "scale" in comp.lower() or "brain" in comp.lower() or "graph" in comp.lower() or "value" in comp.lower():
                refs.append("@env_05_abstract_mind.jpg")

            ref_str = ", ".join(refs) if refs else "@char_01_sovereign.jpg (for style & line weight)"

            bf.write(f"--- SLIDE {shot_id:03d} ({dur}s) --- [Voiceover: \"{clause}\"]\n")
            prompt_text = (
                f"A minimal 2D hand-drawn webcomic illustration in the exact simple vector doodle art style of Ink Explainer, "
                f"drawn on an off-white paper canvas (#FAF9F6). Bold wobbly organic black ink pen outlines (6px-8px stroke weight), "
                f"flat solid color blocking, zero gradients, zero 3D rendering, zero photorealism, zero CAD perspective. "
                f"Widescreen 16:9 aspect ratio (1920x1080). Using references {ref_str}: {comp}. "
                f"{('Color Accent: ' + accent + '. ') if accent else ''}"
                f"Clean 2D graphic novel doodle art with generous negative space. "
                f"STRICT NEGATIVE: Single full-screen frame only. NO comic panel borders, NO multi-panel grids, NO speech bubbles, NO realistic human skin, 16:9 widescreen."
            )
            bf.write(prompt_text + "\n\n")

    print(f"Generated Flow AI batch prompts in: {batch_file}")

    # Generate FFmpeg concat list
    concat_file = CH01_DIR / "concat_en_ch01.txt"
    with open(concat_file, "w", encoding="utf-8") as cf:
        for s in shots:
            shot_id = s["shot_id"]
            dur = s["duration_sec"]
            # slide filename
            cf.write(f"file 'slides/slide_{shot_id:03d}.png'\n")
            cf.write(f"duration {dur}\n")
        # Final file repeat for FFmpeg concat demuxer
        cf.write(f"file 'slides/slide_{shots[-1]['shot_id']:03d}.png'\n")

    print(f"Generated FFmpeg concat list: {concat_file}")

if __name__ == "__main__":
    asyncio.run(main())
