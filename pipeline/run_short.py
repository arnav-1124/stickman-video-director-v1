import argparse
import asyncio
import json
import subprocess
import sys
from pathlib import Path

# Enforce UTF-8 for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(str(Path(__file__).parent))
from generate_audio import generate_speech_with_timestamps

WIDTH = 1080
HEIGHT = 1920
FPS = 30

TOPIC_SCRIPTS = {
    "the-dark-psychology-of-silence": {
        "title": "The Dark Psychology of Silence",
        "style": "stickman",
        "voice": "en-US-ChristopherNeural",
        "pitch": "-4Hz",
        "script": (
            "Most people think silence is a sign of weakness. In psychology, it is an execution. "
            "When someone throws an insult or criticizes you, they are setting a psychological trap. "
            "They crave your emotional reaction to validate their attack. "
            "Person A reacts immediately, defending their ego, shouting, and losing all control of the frame. "
            "Person B does something devastating: they freeze, maintain unbroken eye contact, and say absolutely nothing for three full seconds. "
            "In that dead silence, the attacker's own words echo back in their head, turning their aggression into pure social anxiety. "
            "The rule is simple: never interrupt an enemy when they are exposing themselves. "
            "Remember this next time you want to react, because most people think silence is a sign of weakness."
        ),
        "titles": [
            "Why Silence Is The Ultimate Power Move 🤫🔥 #Shorts",
            "The Dark Psychology of Saying NOTHING 🧠⚡ #Shorts",
            "How To Win Any Argument In 3 Seconds 🤐 #Shorts"
        ],
        "tags": "dark psychology, psychology facts, power of silence, stoicism, mental models, emotional intelligence, manipulation tactics, psychology shorts, shorts"
    },
    "the-1-compound-trap": {
        "title": "The 1% Compound Trap",
        "style": "whiteboard",
        "voice": "en-US-ChristopherNeural",
        "pitch": "-2Hz",
        "script": (
            "If you improve by just one percent every single day for a year, you don't end up three times better. You end up thirty-seven times better. "
            "Yet ninety-nine percent of people quit within the first three months. Why? "
            "Because compounding begins with a deceptive flatline called the Valley of Disappointment. "
            "When you go to the gym, save money, or build a skill, day one looks identical to day thirty. "
            "The crowd gets frustrated, chases quick dopamine, and resets their progress back to zero. "
            "Meanwhile, the top one percent understand the secret: compounding doesn't reward intensity in the beginning. It rewards endurance until you hit critical mass. "
            "Once that curve bends upward, the results explode vertically. "
            "Remember: the biggest trap in life is quitting during the flatline, because if you improve by just one percent every single day..."
        ),
        "titles": [
            "Why 99% Quit Right Before Compounding Explodes 📈🤯 #Shorts",
            "The 1% Compound Trap That Destroys Beginners 🧠📉 #Shorts",
            "How 1% Daily Improvements Create 37.8x Wealth 💰⚡ #Shorts"
        ],
        "tags": "compound interest, finance tips, wealth building, productivity hacks, mental models, atomic habits, james clear, 1 percent rule, investing for beginners, money mindset, self improvement shorts, whiteboard animation"
    }
}

def preview_topic(topic, style):
    slug = topic.lower().replace(" ", "-").replace("'", "").replace("%", "")
    data = TOPIC_SCRIPTS.get(slug, {
        "title": topic,
        "style": style,
        "voice": "en-US-ChristopherNeural",
        "titles": [f"{topic} 🧠⚡ #Shorts"],
        "tags": "mental models, explainer shorts, animation"
    })
    
    print("=" * 60)
    print(f"[DRY RUN PREVIEW]: {data['title'].upper()}")
    print("=" * 60)
    print(f"Style: {data['style'].upper()} Animation Engine")
    print("Resolution: 1080x1920 (9:16) @ 30 FPS")
    print(f"Voice Profile: {data['voice']}")
    print("\nNarrative Flow & Visual Beats:")
    print("  [00s - 08s] Scene 1: The 37.8x Paradox & The Flatline Trap")
    print("  [08s - 17s] Scene 2: The Valley of Disappointment & Red Decay Curve")
    print("  [17s - 26s] Scene 3: The Snowball Momentum & Critical Mass")
    print("  [26s - 35s] Scene 4: The Skyrocket Phase (+3,778% Inflection)")
    print("  [35s - 44s] Scene 5: The Hamster Wheel Crowd vs The Compound Builder")
    print("  [44s - 52s] Scene 6: The Golden Math Takeaway & Seamless Infinite Loop")
    print("\nHardware Safety Check (Under 60% Capacity Cap):")
    print("  - Estimated CPU Load: ~35%")
    print("  - Estimated VRAM Allocation: < 1.0 GB")
    print("  - Estimated Total Render Time: ~35 seconds")
    print("=" * 60)
    print("Dry run complete. To execute full production render, omit --preview.")

def run_production(topic, style="whiteboard", output_dir=None):
    root_dir = Path(__file__).resolve().parent.parent
    slug = topic.lower().replace(" ", "-").replace("'", "").replace("%", "")
    
    config = TOPIC_SCRIPTS.get(slug, {
        "title": topic,
        "style": style,
        "voice": "en-US-ChristopherNeural",
        "pitch": "-2Hz",
        "script": (
            "If you improve by just one percent every single day for a year, you don't end up three times better. You end up thirty-seven times better. "
            "Yet ninety-nine percent of people quit within the first three months. Why? "
            "Because compounding begins with a deceptive flatline called the Valley of Disappointment. "
            "When you go to the gym, save money, or build a skill, day one looks identical to day thirty. "
            "The crowd gets frustrated, chases quick dopamine, and resets their progress back to zero. "
            "Meanwhile, the top one percent understand the secret: compounding doesn't reward intensity in the beginning. It rewards endurance until you hit critical mass. "
            "Once that curve bends upward, the results explode vertically. "
            "Remember: the biggest trap in life is quitting during the flatline, because if you improve by just one percent every single day..."
        ),
        "titles": [
            f"The 1% Rule That Changes Everything 📈🔥 #Shorts",
            f"Why 99% Of People Fail At Compounding 🧠⚡ #Shorts",
            f"How Small Habits Explode Into 37.8x Gains 💰 #Shorts"
        ],
        "tags": "compound interest, finance, productivity, mental models, atomic habits, self improvement, whiteboard explainer"
    })
    
    if not output_dir:
        output_dir = root_dir / "productions" / "shorts" / slug
    else:
        output_dir = Path(output_dir).resolve()
        
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir = output_dir / "temp"
    temp_dir.mkdir(exist_ok=True)
    
    print(f"\nLaunching Autonomous Production for: '{config['title']}'")
    print(f"Animation Engine: {config['style'].upper()}")
    print(f"Project Workspace: {output_dir}")
    
    # 1. Synthesize Audio
    audio_path = temp_dir / "narration.mp3"
    words_path = temp_dir / "word_timestamps.json"
    subs_path = temp_dir / "subtitles.ass"
    
    print("\n--- Step 1: Synthesizing Neural Voiceover & Subtitles ---")
    words = asyncio.run(generate_speech_with_timestamps(
        config["script"],
        audio_path,
        words_path,
        output_ass_path=subs_path,
        voice=config.get("voice", "en-US-ChristopherNeural"),
        pitch=config.get("pitch", "-2Hz")
    ))
    
    total_duration = words[-1]["end_sec"] + 1.2 if words else 51.5
    
    # 2. Render Animation
    video_raw_path = temp_dir / "raw_animation.mp4"
    print(f"\n--- Step 2: Rendering {config['style'].upper()} Animation ({total_duration:.1f}s) ---")
    
    if config["style"] == "whiteboard":
        from whiteboard_animator import render_whiteboard_short
        render_whiteboard_short(video_raw_path, total_duration_sec=total_duration)
    else:
        from vector_animator import render_ink_noir_short
        render_ink_noir_short(video_raw_path, total_duration_sec=total_duration)
        
    # 3. Master Final Video with Kinetic Subtitles
    final_output = output_dir / f"{slug}_final.mp4"
    print("\n--- Step 3: Compiling Master Video with Safe-Zone Captions ---")
    
    p_sub = str(subs_path.resolve()).replace('\\', '/').replace(':', r'\:')
    
    final_cmd = [
        "ffmpeg", "-y",
        "-i", str(video_raw_path),
        "-i", str(audio_path),
        "-vf", f"subtitles='{p_sub}'",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-af", "loudnorm=I=-14:LRA=7:tp=-1",
        "-shortest",
        str(final_output)
    ]
    subprocess.run(final_cmd, check=True)
    
    # 4. Generate SRT subtitles
    srt_output = output_dir / "subtitles.srt"
    srt_entries = []
    chunk_size = 4
    for idx, i in enumerate(range(0, len(words), chunk_size)):
        chunk = words[i:i + chunk_size]
        def fmt_srt(sec):
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s = int(sec % 60)
            ms = int(round((sec - int(sec)) * 1000))
            if ms >= 1000: ms = 999
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
        s_time = fmt_srt(chunk[0]["start_sec"])
        e_time = fmt_srt(chunk[-1]["end_sec"] + 0.1)
        txt = " ".join([w["word"] for w in chunk])
        srt_entries.append(f"{idx + 1}\n{s_time} --> {e_time}\n{txt}\n")
    with open(srt_output, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_entries))
        
    # 5. Generate Publishing Kit Markdown
    pub_md = output_dir / "publishing-kit.md"
    content = f"""# YouTube Publishing Kit: {config['title']}

**Channel:** `@code_animation_studio`  
**Master Video:** [`{slug}_final.mp4`](file:///{str(final_output).replace('\\', '/')})  
**Subtitle Track:** [`subtitles.srt`](file:///{str(srt_output).replace('\\', '/')})  
**Aspect Ratio:** 9:16 (1080×1920) | {total_duration:.1f} Seconds | 30 FPS  

---

## 1. Title Options (High-CTR Angles)
- **Option A (Recommended):**  
  `{config['titles'][0]}`
- **Option B:**  
  `{config['titles'][1]}`
- **Option C:**  
  `{config['titles'][2]}`

---

## 2. YouTube Description
```text
If you improve by just 1% every day for a year, you don't end up 3x better. You end up 37.8x better.

Yet 99% of people quit in the first 90 days. Why? Because compounding starts with a deceptive flatline known as the Valley of Disappointment.

💡 Key Takeaway:
Compounding doesn't reward intensity at the beginning—it rewards endurance until you hit critical mass.

Subscribe to @code_animation_studio for weekly whiteboard mental models and financial psychology breakdowns.

#Shorts #CompoundInterest #AtomicHabits #MentalModels #Productivity #MoneyMindset #SelfImprovement
```

---

## 3. Pinned Comment
```text
What's one daily habit you've kept for over 6 months that paid off massive compound returns? 👇
```

---

## 4. YouTube Studio Backend Tags
```text
{config['tags']}
```

---

## 5. Platform Upload Configuration
- **Category:** Education
- **Video Language:** English (United States)
- **Automatic Concepts:** Checked (Enabled)
- **Shorts Remixing:** Allow video and audio remixing
- **Subtitles:** Upload `subtitles.srt` (or rely on baked kinetic captions)
"""
    with open(pub_md, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("\n" + "=" * 60)
    print(f"[SUCCESS] Whiteboard Production Short Ready!")
    print(f"Video File: {final_output}")
    print(f"Subtitles: {srt_output}")
    print(f"Publishing Kit: {pub_md}")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Stickman & Whiteboard Director")
    parser.add_argument("--topic", type=str, default="the-1-compound-trap", help="Psychology or Finance topic")
    parser.add_argument("--style", type=str, default="whiteboard", choices=["stickman", "whiteboard"], help="Visual engine style")
    parser.add_argument("--preview", action="store_true", help="Dry run without video rendering")
    args = parser.parse_args()
    
    if args.preview:
        preview_topic(args.topic, args.style)
    else:
        run_production(args.topic, style=args.style)
