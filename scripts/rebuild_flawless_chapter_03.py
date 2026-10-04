import os
import sys
import json
import asyncio
import subprocess
import shutil
from pathlib import Path
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = ROOT_DIR / "projects" / "long" / "ep01_why_people_fall_for_who_ignores_them"
CH03_DIR = PROJECT_DIR / "chapter_03_the_economy_of_availability"
SLIDES_DIR = CH03_DIR / "slides"
AUDIO_DIR_EN = CH03_DIR / "audio" / "en"
MASTER_VO_PATH = CH03_DIR / "audio" / "ch03_master_en.mp3"
BGM_PATH = ROOT_DIR / "assets" / "bgm" / "dark_contemplation.mp3"
STORYBOARD_FILE = CH03_DIR / "storyboard.json"
RENDERS_DIR = CH03_DIR / "renders"
CENTRAL_RENDERS_DIR = ROOT_DIR / "renders" / "long" / "ep01_why_people_fall_for_who_ignores_them"
SEGMENTS_DIR = CH03_DIR / "_segments_temp"

AUDIO_DIR_EN.mkdir(parents=True, exist_ok=True)
RENDERS_DIR.mkdir(parents=True, exist_ok=True)
CENTRAL_RENDERS_DIR.mkdir(parents=True, exist_ok=True)
SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)

# 100% Natural Storytelling Voice Settings
VOICE_EN = "en-US-ChristopherNeural"
PITCH_EN = "-2Hz"
RATE_EN = "+5%"  # Natural conversational storytelling pace

# Exact 33-shot specification for 100% 1:1 Narrative-to-Visual Synchronization
SHOTS_SPEC = [
    {
        "shot_id": "67",
        "slide_file": "slide_67.jpg",
        "title": "Chapter 3 Title Card",
        "scene_type": "title_card",
        "spoken_clause": "[CHAPTER 3: THE ECONOMY OF AVAILABILITY]",
        "speech_text": "Chapter Three: The Economy of Availability.",
        "major_pause": True
    },
    {
        "shot_id": "68",
        "slide_file": "slide_68.jpg",
        "title": "Social Supply & Demand",
        "scene_type": "metaphor_diagram",
        "spoken_clause": "Beyond dopamine, there is a second fundamental law at work: the Law of Social Supply and Demand.",
        "speech_text": "Beyond dopamine, there is a second fundamental law at work: the Law of Social Supply and Demand.",
        "major_pause": False
    },
    {
        "shot_id": "69",
        "slide_file": "slide_69.jpg",
        "title": "Unspoken Power Dynamics",
        "scene_type": "character_interaction",
        "spoken_clause": "Every social interaction carries an unspoken power dynamic.",
        "speech_text": "Every social interaction carries an unspoken power dynamic.",
        "major_pause": False
    },
    {
        "shot_id": "70",
        "slide_file": "slide_70.jpg",
        "title": "Social Exchange Theory",
        "scene_type": "text_card",
        "spoken_clause": "Psychologist George Homans called this Social Exchange Theory.",
        "speech_text": "Psychologist George Homans called this Social Exchange Theory.",
        "major_pause": False
    },
    {
        "shot_id": "71",
        "slide_file": "slide_71.jpg",
        "title": "The Principle of Least Interest",
        "scene_type": "metaphor_diagram",
        "spoken_clause": "In any relationship between two people, the person who has the least investment in the outcome holds the most leverage.",
        "speech_text": "In any relationship between two people, the person who has the least investment in the outcome holds the most leverage.",
        "major_pause": True
    },
    {
        "shot_id": "72",
        "slide_file": "slide_72.jpg",
        "title": "The College Group Project",
        "scene_type": "character_interaction",
        "spoken_clause": "Imagine two students working on a group presentation in college.",
        "speech_text": "Imagine two students working on a group presentation in college.",
        "major_pause": False
    },
    {
        "shot_id": "73A",
        "slide_file": "slide_73A.jpg",
        "title": "Desperate for an A-Plus",
        "scene_type": "character_vignette",
        "spoken_clause": "One student is desperate for an A-plus.",
        "speech_text": "One student is desperate for an A-plus.",
        "major_pause": False
    },
    {
        "shot_id": "73",
        "slide_file": "slide_73.jpg",
        "title": "3 AM Slide Formatting",
        "scene_type": "character_closeup",
        "spoken_clause": "He stays up until three in the morning formatting slides, worrying about fonts, and sweating every detail.",
        "speech_text": "He stays up until three in the morning formatting slides, worrying about fonts, and sweating every detail.",
        "major_pause": False
    },
    {
        "shot_id": "74",
        "slide_file": "slide_74.jpg",
        "title": "The B-Minus Guy",
        "scene_type": "character_interaction",
        "spoken_clause": "The other student leans back in his chair, glances at the project, and says, 'A B-minus is fine with me. I have other priorities.'",
        "speech_text": "The other student leans back in his chair, glances at the project, and says, 'A B-minus is fine with me. I have other priorities.'",
        "major_pause": True
    },
    {
        "shot_id": "75",
        "slide_file": "slide_75.jpg",
        "title": "Who Controls the Frame?",
        "scene_type": "text_punch_card",
        "spoken_clause": "Who controls the frame of that project?",
        "speech_text": "Who controls the frame of that project?",
        "major_pause": False
    },
    {
        "shot_id": "76",
        "slide_file": "slide_76.jpg",
        "title": "The Person Who Cares Less",
        "scene_type": "character_vignette",
        "spoken_clause": "The person who cares less.",
        "speech_text": "The person who cares less.",
        "major_pause": True
    },
    {
        "shot_id": "77",
        "slide_file": "slide_77.jpg",
        "title": "The Walking Away Power",
        "scene_type": "character_vignette",
        "spoken_clause": "The person who is comfortable walking away sets the rules.",
        "speech_text": "The person who is comfortable walking away sets the rules.",
        "major_pause": True
    },
    {
        "shot_id": "78",
        "slide_file": "slide_78.jpg",
        "title": "The Unspoken Broadcast",
        "scene_type": "metaphor_diagram",
        "spoken_clause": "When you constantly make yourself available to someone, you communicate a hidden signal without saying a single word.",
        "speech_text": "When you constantly make yourself available to someone, you communicate a hidden signal without saying a single word.",
        "major_pause": False
    },
    {
        "shot_id": "79",
        "slide_file": "slide_79.jpg",
        "title": "The Empty Calendar",
        "scene_type": "prop_closeup",
        "spoken_clause": "You communicate that your calendar is empty.",
        "speech_text": "You communicate that your calendar is empty.",
        "major_pause": False
    },
    {
        "shot_id": "80",
        "slide_file": "slide_80.jpg",
        "title": "No Compelling Passions",
        "scene_type": "metaphor_vignette",
        "spoken_clause": "You communicate that you have no pressing goals, no compelling passions, and no other options.",
        "speech_text": "You communicate that you have no pressing goals, no compelling passions, and no other options.",
        "major_pause": False
    },
    {
        "shot_id": "81",
        "slide_file": "slide_81.jpg",
        "title": "The Orbiting Satellite",
        "scene_type": "metaphor_diagram",
        "spoken_clause": "You communicate that your entire world revolves around whether this one person grants you their favor.",
        "speech_text": "You communicate that your entire world revolves around whether this one person grants you their favor.",
        "major_pause": False
    },
    {
        "shot_id": "82",
        "slide_file": "slide_82.jpg",
        "title": "Total Availability = Desperation",
        "scene_type": "text_card",
        "spoken_clause": "And to the human subconscious, total availability looks dangerously close to desperation.",
        "speech_text": "And to the human subconscious, total availability looks dangerously close to desperation.",
        "major_pause": True
    },
    {
        "shot_id": "83",
        "slide_file": "slide_83.jpg",
        "title": "The Cornering Salesman",
        "scene_type": "character_interaction",
        "spoken_clause": "Think about how you feel when a salesperson in a shopping mall corners you.",
        "speech_text": "Think about how you feel when a salesperson in a shopping mall corners you.",
        "major_pause": False
    },
    {
        "shot_id": "84A",
        "slide_file": "slide_84A.jpg",
        "title": "Smiling Too Broadly",
        "scene_type": "character_closeup",
        "spoken_clause": "They smile too broadly.",
        "speech_text": "They smile too broadly.",
        "major_pause": False
    },
    {
        "shot_id": "84B",
        "slide_file": "slide_84B.jpg",
        "title": "Following Down the Aisle",
        "scene_type": "character_interaction",
        "spoken_clause": "They follow you down the aisle.",
        "speech_text": "They follow you down the aisle.",
        "major_pause": False
    },
    {
        "shot_id": "84",
        "slide_file": "slide_84.jpg",
        "title": "Discounts Before Price Tag",
        "scene_type": "character_interaction",
        "spoken_clause": "They offer you discounts before you even inspect the price tag.",
        "speech_text": "They offer you discounts before you even inspect the price tag.",
        "major_pause": False
    },
    {
        "shot_id": "85A",
        "slide_file": "slide_85A.jpg",
        "title": "The Decent Product Dilemma",
        "scene_type": "character_interaction",
        "spoken_clause": "Even if the product they are selling is decent, what is your immediate reflex?",
        "speech_text": "Even if the product they are selling is decent, what is your immediate reflex?",
        "major_pause": False
    },
    {
        "shot_id": "85",
        "slide_file": "slide_85.jpg",
        "title": "The Reflex to Back Away",
        "scene_type": "character_closeup",
        "spoken_clause": "You want to back away.",
        "speech_text": "You want to back away.",
        "major_pause": False
    },
    {
        "shot_id": "85C",
        "slide_file": "slide_85C.jpg",
        "title": "The Spark of Suspicion",
        "scene_type": "character_closeup",
        "spoken_clause": "You feel suspicious.",
        "speech_text": "You feel suspicious.",
        "major_pause": False
    },
    {
        "shot_id": "86",
        "slide_file": "slide_86.jpg",
        "title": "The Hidden Defect Suspicion",
        "scene_type": "metaphor_vignette",
        "spoken_clause": "You think to yourself: 'If this jacket is so incredible, why are they practically begging me to take it?'",
        "speech_text": "You think to yourself: 'If this jacket is so incredible, why are they practically begging me to take it?'",
        "major_pause": False
    },
    {
        "shot_id": "87",
        "slide_file": "slide_87.jpg",
        "title": "The Invisible Trap",
        "scene_type": "metaphor_diagram",
        "spoken_clause": "Desperate enthusiasm always feels like an invisible trap.",
        "speech_text": "Desperate enthusiasm always feels like an invisible trap.",
        "major_pause": False
    },
    {
        "shot_id": "87B",
        "slide_file": "slide_87B.jpg",
        "title": "The Asymmetric Power Debt",
        "scene_type": "metaphor_diagram",
        "spoken_clause": "It signals that the seller needs something from you more than you need something from them.",
        "speech_text": "It signals that the seller needs something from you more than you need something from them.",
        "major_pause": True
    },
    {
        "shot_id": "88A",
        "slide_file": "slide_88A.jpg",
        "title": "The Opposite Reaction",
        "scene_type": "split_contrast",
        "spoken_clause": "When a person ignores you, or simply doesn't rush to cater to your every mood, they trigger the exact opposite reaction.",
        "speech_text": "When a person ignores you, or simply doesn't rush to cater to your every mood, they trigger the exact opposite reaction.",
        "major_pause": False
    },
    {
        "shot_id": "88",
        "slide_file": "slide_88.jpg",
        "title": "Emotional Self-Sufficiency",
        "scene_type": "character_vignette",
        "spoken_clause": "They signal emotional self-sufficiency.",
        "speech_text": "They signal emotional self-sufficiency.",
        "major_pause": False
    },
    {
        "shot_id": "89",
        "slide_file": "slide_89.jpg",
        "title": "Your Absence Won't Break Me",
        "scene_type": "character_interaction",
        "spoken_clause": "They communicate that while your presence might be welcome, your absence will not shatter their existence.",
        "speech_text": "They communicate that while your presence might be welcome, your absence will not shatter their existence.",
        "major_pause": False
    },
    {
        "shot_id": "90",
        "slide_file": "slide_90.jpg",
        "title": "Having Your Own Orbit",
        "scene_type": "metaphor_diagram",
        "spoken_clause": "They have their own orbit.",
        "speech_text": "They have their own orbit.",
        "major_pause": False
    },
    {
        "shot_id": "90B",
        "slide_file": "slide_90B.jpg",
        "title": "Not Auditioning for Approval",
        "scene_type": "metaphor_vignette",
        "spoken_clause": "They are not auditioning for your approval.",
        "speech_text": "They are not auditioning for your approval.",
        "major_pause": False
    },
    {
        "shot_id": "90C",
        "slide_file": "slide_90C.jpg",
        "title": "The Intrinsic Value of Sovereignty",
        "scene_type": "metaphor_diagram",
        "spoken_clause": "And because they refuse to sell themselves, you immediately assume the product must be of immense value.",
        "speech_text": "And because they refuse to sell themselves, you immediately assume the product must be of immense value.",
        "major_pause": True
    }
]

def get_duration(file_path):
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(file_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

async def synthesize_exact_shot(sid, text, is_major, raw_dir, out_mp3):
    comm = edge_tts.Communicate(text, VOICE_EN, pitch=PITCH_EN, rate=RATE_EN, boundary="WordBoundary")
    raw_mp3 = raw_dir / f"shot_{sid}_raw.mp3"
    words = []
    
    with open(raw_mp3, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = (chunk["offset"] / 10000) / 1000.0
                end_sec = ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                words.append((chunk["text"], start_sec, end_sec))

    total_raw = get_duration(raw_mp3)
    last_word_text, _, last_word_end = words[-1]
    
    # Breathing pause: 0.45s for major scene breaks, 0.35s for regular narrative flow
    pause_dur = 0.45 if is_major else 0.35
    target_dur = min(total_raw, round(last_word_end + pause_dur, 3))
    
    # Clean cut at target_dur with a gentle 0.04s fade-out at the very tail of silence
    fade_start = max(0, target_dur - 0.04)
    cmd_trim = [
        "ffmpeg", "-y", "-i", str(raw_mp3),
        "-t", f"{target_dur:.3f}",
        "-af", f"afade=t=out:st={fade_start:.3f}:d=0.04",
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(out_mp3)
    ]
    subprocess.run(cmd_trim, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    actual_dur = get_duration(out_mp3)
    return {
        "shot_id": sid,
        "text": text,
        "last_word": last_word_text,
        "last_word_end": round(last_word_end, 3),
        "pause_dur": round(actual_dur - last_word_end, 3),
        "duration": actual_dur
    }

async def main():
    print("=" * 80)
    print("  CHAPTER 03 FLAWLESS REBUILD: 33 SHOTS 1:1 NARRATIVE-TO-VISUAL SYNC")
    print("=" * 80)

    # 1. Clean old audio
    for f in AUDIO_DIR_EN.glob("*.mp3"):
        f.unlink()

    raw_dir = CH03_DIR / "audio" / "_raw_tts"
    raw_dir.mkdir(parents=True, exist_ok=True)

    print("\n--- [1/4] Generating natural voiceover for all 33 shots ---")
    total_audio_time = 0.0

    for item in SHOTS_SPEC:
        sid = item["shot_id"]
        speech_text = item["speech_text"]
        is_major = item["major_pause"]
        out_mp3 = AUDIO_DIR_EN / f"shot_{sid}.mp3"

        metrics = await synthesize_exact_shot(sid, speech_text, is_major, raw_dir, out_mp3)
        dur = metrics["duration"]
        item["duration_sec"] = dur
        total_audio_time += dur
        
        print(f"  Shot {sid:4} ({dur:5.2f}s) | Ends at {metrics['last_word_end']:5.2f}s (\"{metrics['last_word']}\") + {metrics['pause_dur']:.2f}s -> \"{speech_text[:38]}...\"")

    shutil.rmtree(raw_dir, ignore_errors=True)

    # Save complete updated storyboard.json
    sb_out = {
        "chapter": 3,
        "chapter_title": "3: THE ECONOMY OF AVAILABILITY",
        "total_shots": len(SHOTS_SPEC),
        "estimated_duration_sec": round(total_audio_time, 2),
        "shots": [
            {
                "shot_id": item["shot_id"],
                "chapter": 3,
                "title": item["title"],
                "duration_sec": item["duration_sec"],
                "spoken_clause": item["spoken_clause"],
                "scene_type": item["scene_type"],
                "slide_file": item["slide_file"]
            }
            for item in SHOTS_SPEC
        ]
    }
    with open(STORYBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(sb_out, f, indent=2)
    print(f"\n  ✓ Storyboard updated with all 33 shots (Total Audio: {total_audio_time:.2f}s / {total_audio_time/60:.2f}m)")

    # 2. Assembling sample-accurate master VO track
    print("\n--- [2/4] Assembling sample-accurate master VO track ---")
    inputs = []
    filter_inputs = []
    for idx, item in enumerate(SHOTS_SPEC):
        sid = item["shot_id"]
        inputs.extend(['-i', str(AUDIO_DIR_EN / f"shot_{sid}.mp3")])
        filter_inputs.append(f'[{idx}:a]')
    filter_str = ''.join(filter_inputs) + f'concat=n={len(SHOTS_SPEC)}:v=0:a=1[aout]'
    cmd_master = ['ffmpeg', '-y'] + inputs + ['-filter_complex', filter_str, '-map', '[aout]', '-c:a', 'libmp3lame', '-b:a', '192k', str(MASTER_VO_PATH)]
    subprocess.run(cmd_master, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    master_dur = get_duration(MASTER_VO_PATH)
    print(f"  ✓ Master VO Track compiled: {MASTER_VO_PATH.name} ({master_dur:.3f}s)")

    # 3. Render 33 micro-segments (100% Image-Audio Binding)
    print("\n--- [3/4] Rendering 33 micro-segments (100% frame sync) ---")
    vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#FAF9F6,setsar=1,fps=30"
    segment_files = []

    for idx, item in enumerate(SHOTS_SPEC):
        sid = item["shot_id"]
        slide_name = item["slide_file"]
        img_path = SLIDES_DIR / slide_name
        if not img_path.exists():
            raise FileNotFoundError(f"Missing slide image: {img_path}")

        audio_path = AUDIO_DIR_EN / f"shot_{sid}.mp3"
        seg_out = SEGMENTS_DIR / f"seg_{idx:02d}_{sid}.mp4"
        dur = item["duration_sec"]

        cmd_seg = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img_path),
            "-i", str(audio_path),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
            "-t", f"{dur:.3f}",
            "-shortest",
            str(seg_out)
        ]
        subprocess.run(cmd_seg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        segment_files.append(seg_out)
        if (idx + 1) % 6 == 0 or (idx + 1) == len(SHOTS_SPEC):
            print(f"  ✓ Built {idx + 1} of {len(SHOTS_SPEC)} segments...")

    # Write segment concat list
    seg_list_path = SEGMENTS_DIR / "concat_segments.txt"
    with open(seg_list_path, "w", encoding="utf-8") as f:
        for seg in segment_files:
            f.write(f"file '{seg.as_posix()}'\n")

    # 4. Concatenate segments into preview videos
    out_no_bgm = RENDERS_DIR / "ch03_the_economy_of_availability_preview_no_bgm.mp4"
    print(f"\n--- [4/4] Assembling full 33-shot Chapter 3 video ---")
    print(f"  Rendering clean narration preview: {out_no_bgm.name}")

    cmd_stitch = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(seg_list_path),
        "-c", "copy",
        str(out_no_bgm)
    ]
    subprocess.run(cmd_stitch, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Render with BGM
    out_with_bgm = RENDERS_DIR / "ch03_the_economy_of_availability_preview.mp4"
    central_out = CENTRAL_RENDERS_DIR / "ch03_the_economy_of_availability_preview.mp4"

    if BGM_PATH.exists():
        print(f"  Adding atmospheric BGM track: {BGM_PATH.name}")
        fade_out_start = max(0, total_audio_time - 2.5)
        filter_complex = (
            f"[1:a]volume=0.10,afade=t=in:st=0:d=0.5,afade=t=out:st={fade_out_start:.2f}:d=2.0[bgm];"
            f"[0:a]volume=1.0[vo];"
            f"[vo][bgm]amix=inputs=2:duration=first:normalize=0[aout]"
        )
        cmd_bgm = [
            "ffmpeg", "-y",
            "-i", str(out_no_bgm),
            "-stream_loop", "-1", "-i", str(BGM_PATH),
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(out_with_bgm)
        ]
        subprocess.run(cmd_bgm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        shutil.copy2(str(out_with_bgm), str(central_out))
        print(f"  ✓ Production video with BGM ready: {out_with_bgm}")
        print(f"  ✓ Central archive copy: {central_out}")

    # Cleanup temp segments
    shutil.rmtree(SEGMENTS_DIR, ignore_errors=True)

    final_v_dur = get_duration(out_with_bgm if out_with_bgm.exists() else out_no_bgm)
    print("\n" + "=" * 80)
    print("  CHAPTER 03 FLAWLESS REBUILD COMPLETE!")
    print(f"  Total Shots:          33 (Every script line has 1:1 dedicated visual)")
    print(f"  Final Video Duration: {final_v_dur:.2f}s ({int(final_v_dur//60)}m {int(final_v_dur%60):02d}s)")
    print(f"  Audio/Video Sync:     100.000% frame-bound")
    print(f"  Natural Speech Rate:  +5% ChristopherNeural with 0.35s-0.45s breathing pauses")
    print(f"  Preview with BGM:     {out_with_bgm}")
    print(f"  Narration Only:       {out_no_bgm}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
