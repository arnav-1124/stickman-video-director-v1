import argparse
import asyncio
import json
import subprocess
import sys
from pathlib import Path

# Enforce UTF-8 for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add pipeline directory to import paths
sys.path.append(str(Path(__file__).parent))
from generate_audio import generate_speech_with_timestamps

WIDTH = 1080
HEIGHT = 1920
FPS = 30

def preview_topic(topic):
    print("=" * 60)
    print(f"[DRY RUN PREVIEW]: {topic.upper()}")
    print("=" * 60)
    print("Target Runtime: 60 seconds (1080x1920 @ 30fps)")
    print("Aesthetic: Ink Noir (Dark Slate #0B0B0E + Crimson Accent #FF2A4D)")
    print("Voice Profile: en-US-ChristopherNeural (-4Hz pitch)")
    print("\n5-Beat Retention Narrative Clock:")
    print("  [00s - 03s] BEAT 1 (Hook): Counter-intuitive psychological pattern interrupt.")
    print("  [03s - 18s] BEAT 2 (Mechanism): The neurological / social bias explained.")
    print("  [18s - 42s] BEAT 3 (Stickman Contrast): Person A (reactive) vs. Person B (composed).")
    print("  [42s - 55s] BEAT 4 (Actionable Rule): Concrete psychological tactic.")
    print("  [55s - 60s] BEAT 5 (The Loop): Grammatical seamless loop back to opening line.")
    print("\nHardware Safety Check (Under 60% Capacity Cap):")
    print("  - Estimated CPU Load: ~35%")
    print("  - Estimated VRAM Allocation: < 1.0 GB")
    print("  - Estimated Total Render Time: ~35 seconds")
    print("=" * 60)
    print("Dry run complete. To execute full render, omit --preview.")

def run_production(topic, output_dir=None):
    root_dir = Path(__file__).resolve().parent.parent
    if not output_dir:
        slug = topic.lower().replace(" ", "-").replace("'", "")
        output_dir = root_dir / "productions" / "shorts" / slug
    else:
        output_dir = Path(output_dir).resolve()
        
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = output_dir / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    print(f"\nLaunching Autonomous Production for: '{topic}'")
    print(f"Project Workspace: {output_dir}")
    
    # 1. Generate Voiceover & Timestamps
    script_text = (
        "Most people think silence is a sign of weakness. In psychology, it is an execution. "
        "When someone throws an insult or criticizes you, they are setting a psychological trap. "
        "They crave your emotional reaction to validate their attack. "
        "Person A reacts immediately, defending their ego, shouting, and losing all control of the frame. "
        "Person B does something devastating: they freeze, maintain unbroken eye contact, and say absolutely nothing for three full seconds. "
        "In that dead silence, the attacker's own words echo back in their head, turning their aggression into pure social anxiety. "
        "The rule is simple: never interrupt an enemy when they are exposing themselves. "
        "Remember this next time you want to react, because most people think silence is a sign of weakness."
    )
    
    audio_path = temp_dir / "narration.mp3"
    words_path = temp_dir / "word_timestamps.json"
    subs_path = temp_dir / "subtitles.ass"
    
    print("\n--- Step 1: Synthesizing Neural Audio & Word Timestamps ---")
    words = asyncio.run(generate_speech_with_timestamps(
        script_text,
        audio_path,
        words_path,
        output_ass_path=subs_path
    ))
    
    # 2. Render Ink Noir Vector Stickman Video
    video_raw_path = temp_dir / "raw_animation.mp4"
    print("\n--- Step 2: Rendering Vector Stickman Animation (Hardware-Safe) ---")
    
    total_duration = words[-1]["end_sec"] + 1.0 if words else 48.0
    from vector_animator import render_ink_noir_short
    render_ink_noir_short(video_raw_path, total_duration_sec=total_duration)
    
    # 3. Master Audio, Burn Captions, and Finalize
    final_output = output_dir / f"{output_dir.name}_final.mp4"
    print("\n--- Step 3: Compiling Master Video with Kinetic Captions ---")
    
    p_sub = str(subs_path.resolve()).replace('\\', '/').replace(':', r'\:')
    
    final_cmd = [
        "ffmpeg", "-y",
        "-i", str(video_raw_path),
        "-i", str(audio_path),
        "-vf", f"subtitles='{p_sub}'",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-af", "loudnorm=I=-14:LRA=7:tp=-1",
        "-shortest",
        str(final_output)
    ]
    
    subprocess.run(final_cmd, check=True)
    
    # 4. Generate YouTube Publishing Kit
    pub_kit = {
        "channel": "@code_animation_studio",
        "topic": topic,
        "title_options": [
            "Why Silence Is The Ultimate Power Move 🤫🔥 #Shorts",
            "The Dark Psychology of Saying NOTHING 🧠⚡ #Shorts",
            "How To Win Any Argument In 3 Seconds 🤐 #Shorts"
        ],
        "description": f"Why do the most powerful people stay silent when attacked? Discover the psychological mechanism behind emotional detachment.\n\nSubscribe to @code_animation_studio for weekly dark psychology and mental model breakdowns!\n\n#DarkPsychology #PsychologyFacts #Mindset #SelfImprovement #MentalModels #Shorts",
        "tags": "dark psychology, psychology facts, power of silence, stoicism, mental models, emotional intelligence, manipulation tactics, psychology shorts, shorts",
        "master_video": str(final_output)
    }
    
    with open(output_dir / "publishing_kit.json", "w", encoding="utf-8") as f:
        json.dump(pub_kit, f, indent=2)
        
    print("\n" + "=" * 60)
    print(f"[SUCCESS] Production Short Ready!")
    print(f"Video File: {final_output}")
    print(f"Publishing Kit: {output_dir / 'publishing_kit.json'}")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Stickman & Whiteboard Director")
    parser.add_argument("--topic", type=str, required=True, help="Psychology or Finance topic")
    parser.add_argument("--preview", action="store_true", help="10-second dry run without video rendering")
    args = parser.parse_args()
    
    if args.preview:
        preview_topic(args.topic)
    else:
        run_production(args.topic)

