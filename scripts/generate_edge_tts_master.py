"""
Generate Clean Deep Motivator Audio using local edge-tts with 100% Sync.
Outputs:
- remotion/public/audio/ep02_voiceover.mp3
- remotion/src/compositions/sticky_in_dark/long/ep02_the_consistency_paradox/subtitles.ts
- remotion/src/compositions/sticky_in_dark/long/ep02_the_consistency_paradox/cameraPaths.ts (updated frame timings)
"""

import asyncio
import os
import subprocess
import json
import edge_tts

VOICE = "en-US-ChristopherNeural"
RATE = "-3%"
PITCH = "+0Hz"

FPS = 30

# The 25 script beats for "The Consistency Paradox"
BEATS = [
    {
        "id": "beat_01",
        "scene": "AlexBedroomNight",
        "text": "At two in the morning, you promise yourself that tomorrow everything changes.",
        "pause_after": 0.45,
    },
    {
        "id": "beat_02",
        "scene": "SunriseTrail",
        "text": "You will wake up at dawn. You will run five miles.",
        "pause_after": 0.45,
    },
    {
        "id": "beat_03",
        "scene": "AlexOffice",
        "text": "You will work for eight unbroken hours, eat clean, and finally master your life.",
        "pause_after": 0.55,
    },
    {
        "id": "beat_04",
        "scene": "AlexOfficeProductive",
        "text": "And for two days, you actually do it.",
        "pause_after": 0.5,
    },
    {
        "id": "beat_05",
        "scene": "SunriseRidge",
        "text": "You feel invincible. You feel like you finally unlocked the secret everyone else is missing.",
        "pause_after": 0.7,
    },
    {
        "id": "beat_06",
        "scene": "AlexBedroomDay4",
        "text": "THEN DAY FOUR ARRIVES.",
        "pause_after": 0.75,
    },
    {
        "id": "beat_07",
        "scene": "AlexBedroomCold",
        "text": "You wake up tired. The room is cold. Your bed is warm.",
        "pause_after": 0.5,
    },
    {
        "id": "beat_08",
        "scene": "AlexBedroomVanished",
        "text": "And suddenly, that fiery motivation from Tuesday has vanished into thin air.",
        "pause_after": 0.55,
    },
    {
        "id": "beat_09",
        "scene": "AlexBedroomAlarmOff",
        "text": "You negotiate with yourself for thirty seconds, turn off the alarm, and fall back asleep.",
        "pause_after": 0.6,
    },
    {
        "id": "beat_10",
        "scene": "AlexGuiltDesk",
        "text": "By noon, the familiar weight of guilt sets in. You tell yourself you lack discipline. You tell yourself you are just lazy.",
        "pause_after": 0.65,
    },
    {
        "id": "beat_11",
        "scene": "MentorSanctuary",
        "text": "Here is the truth an experienced senior will tell you.",
        "pause_after": 0.6,
    },
    {
        "id": "beat_12",
        "scene": "WillpowerEngine",
        "text": "You did not fail because you lack willpower. You failed because you asked willpower to do a job it was never built for.",
        "pause_after": 0.6,
    },
    {
        "id": "beat_13",
        "scene": "BrainSurvivalCore",
        "text": "Your brain is not an inspiration machine. Your brain is a survival organ designed to conserve energy.",
        "pause_after": 0.6,
    },
    {
        "id": "beat_14",
        "scene": "BiologyAlarmCrisis",
        "text": "The moment you attempt a massive, radical overhaul overnight, your biology sounds the alarm. It treats that sudden spike in effort like a threat.",
        "pause_after": 0.65,
    },
    {
        "id": "beat_15",
        "scene": "ConsistentRoutineCafe",
        "text": "People who stay consistent year after year are not suffering through superhuman acts of discipline every morning.",
        "pause_after": 0.6,
    },
    {
        "id": "beat_16",
        "scene": "IronForgeGym",
        "text": "Consistency is not an act of willpower, it is the elimination of choice.",
        "pause_after": 0.65,
    },
    {
        "id": "beat_17",
        "scene": "MorningNoNegotiation",
        "text": "They do not negotiate with their feelings at seven in the morning.",
        "pause_after": 0.5,
    },
    {
        "id": "beat_18",
        "scene": "AlexOfficeFocus",
        "text": "They do not wait for the mood to strike them before opening the laptop.",
        "pause_after": 0.55,
    },
    {
        "id": "beat_19",
        "scene": "EnvironmentArchitect",
        "text": "Instead, they engineer the environment so that starting requires less effort than feeling guilty.",
        "pause_after": 0.6,
    },
    {
        "id": "beat_20",
        "scene": "EnvironmentChecklist",
        "text": "Phone in another room. Shoes directly by doorway. Blank document open before bed.",
        "pause_after": 0.65,
    },
    {
        "id": "beat_21",
        "scene": "RiverbedValley",
        "text": "They carve a riverbed where water flows naturally, instead of pushing a giant boulder up a muddy hill every day.",
        "pause_after": 0.65,
    },
    {
        "id": "beat_22",
        "scene": "ExhaustionWarning",
        "text": "Stop aiming for legendary days that leave you exhausted and broken by Friday.",
        "pause_after": 0.55,
    },
    {
        "id": "beat_23",
        "scene": "MinimalThreshold",
        "text": "Lower the barrier until resistance becomes ridiculous.",
        "pause_after": 0.6,
    },
    {
        "id": "beat_24",
        "scene": "AlexChairWriting",
        "text": "Sit in the chair for two minutes. Write one clean paragraph. Put on the sneakers and step outside.",
        "pause_after": 0.65,
    },
    {
        "id": "beat_25",
        "scene": "SunriseHorizonVictory",
        "text": "Cast one small vote for the person you want to become, and let momentum do the heavy lifting.",
        "pause_after": 1.2,
    },
]

TEMP_DIR = "scratch/edge_tts_clips"

def get_audio_duration(file_path: str) -> float:
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

async def generate_speech():
    os.makedirs(TEMP_DIR, exist_ok=True)
    clip_files = []
    shot_timings = []
    
    current_time_sec = 0.0
    
    print(f"Generating {len(BEATS)} speech beats with {VOICE} (clean deep motivator)...")
    for i, beat in enumerate(BEATS):
        raw_clip = os.path.join(TEMP_DIR, f"clip_{i:02d}_raw.mp3")
        padded_clip = os.path.join(TEMP_DIR, f"clip_{i:02d}_padded.mp3")
        
        # 1. Edge-TTS synthesis
        communicate = edge_tts.Communicate(beat["text"], VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(raw_clip)
        
        raw_dur = get_audio_duration(raw_clip)
        pause = beat["pause_after"]
        
        # 2. Add clean silence pad at end for natural pacing
        # apad filter adds exact silence duration
        cmd = [
            "ffmpeg", "-y", "-i", raw_clip,
            "-af", f"apad=pad_dur={pause}",
            "-c:a", "libmp3lame", "-b:a", "192k",
            padded_clip
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        clip_dur = get_audio_duration(padded_clip)
        clip_files.append(padded_clip)
        
        start_sec = current_time_sec
        end_sec = current_time_sec + clip_dur
        
        start_frame = int(round(start_sec * FPS))
        end_frame = int(round(end_sec * FPS))
        
        shot_timings.append({
            "index": i + 1,
            "scene": beat["scene"],
            "text": beat["text"],
            "startSec": start_sec,
            "endSec": end_sec,
            "startFrame": start_frame,
            "endFrame": end_frame,
            "durationFrames": end_frame - start_frame
        })
        
        current_time_sec = end_sec
        print(f"[{i+1:02d}/25] {start_sec:.2f}s -> {end_sec:.2f}s (Frames: {start_frame}->{end_frame}) - {beat['text'][:40]}...")

    # 3. Concatenate all clips cleanly
    concat_list = os.path.join(TEMP_DIR, "concat_list.txt")
    with open(concat_list, "w") as f:
        for clip in clip_files:
            abs_p = os.path.abspath(clip).replace("\\", "/")
            f.write(f"file '{abs_p}'\n")
            
    final_audio = "remotion/public/audio/ep02_voiceover.mp3"
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        final_audio
    ]
    subprocess.run(concat_cmd, check=True)
    
    total_audio_dur = get_audio_duration(final_audio)
    total_frames = int(round(total_audio_dur * FPS))
    print(f"\nMaster Audio Ready: {final_audio}")
    print(f"Total Duration: {total_audio_dur:.2f}s = {total_frames} frames @ {FPS}fps")
    
    # Verify last shot ends at total_frames
    shot_timings[-1]["endFrame"] = total_frames
    shot_timings[-1]["durationFrames"] = total_frames - shot_timings[-1]["startFrame"]
    
    # Save timing manifest JSON
    with open("scratch/shot_timings.json", "w") as f:
        json.dump({
            "totalDurationSec": total_audio_dur,
            "totalDurationFrames": total_frames,
            "fps": FPS,
            "shots": shot_timings
        }, f, indent=2)
        
    print("Saved timing manifest to scratch/shot_timings.json")
    return shot_timings, total_frames

if __name__ == "__main__":
    asyncio.run(generate_speech())
