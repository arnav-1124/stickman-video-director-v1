"""
Build Clip-Wise Pipeline for Episode 02: The Consistency Paradox
- Strict pause of 0.25s between all clips
- Generates clip-wise audio in remotion/public/audio/ep02/clips/clip_XX.mp3
- Generates master audio in remotion/public/audio/ep02_voiceover.mp3
- Creates clip-wise Remotion composition folders in:
  remotion/src/compositions/sticky_in_dark/long/ep02_the_consistency_paradox/clips/clip_XX/index.tsx
- Registers all clips in Remotion Root.tsx
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
STRICT_PAUSE_SEC = 0.25

CLIPS = [
    {
        "id": 1,
        "name": "Clip01_2AM_Promise",
        "title": "2 AM Promise in Bedroom",
        "sceneId": 1,
        "day": "DAY - 1",
        "text": "At two in the morning, you promise yourself that tomorrow everything changes.",
    },
    {
        "id": 2,
        "name": "Clip02_Dawn_Run",
        "title": "Dawn 5-Mile Run",
        "sceneId": 2,
        "day": "DAY - 1",
        "text": "You will wake up at dawn. You will run five miles.",
    },
    {
        "id": 3,
        "name": "Clip03_Executive_Office",
        "title": "8 Unbroken Hours in Office",
        "sceneId": 3,
        "day": "DAY - 1",
        "text": "You will work for eight unbroken hours, eat clean, and finally master your life.",
    },
    {
        "id": 4,
        "name": "Clip04_Two_Days_Victory",
        "title": "Two Days of Perfect Execution",
        "sceneId": 4,
        "day": "DAY - 2",
        "text": "And for two days, you actually do it.",
    },
    {
        "id": 5,
        "name": "Clip05_Invincible_Peak",
        "title": "Feeling Invincible on the Peak",
        "sceneId": 5,
        "day": "DAY - 2",
        "text": "You feel invincible. You feel like you finally unlocked the secret everyone else is missing.",
    },
    {
        "id": 6,
        "name": "Clip06_Day_Four_Arrival",
        "title": "THEN DAY FOUR ARRIVES",
        "sceneId": 6,
        "day": "DAY - 4",
        "text": "THEN DAY FOUR ARRIVES.",
    },
    {
        "id": 7,
        "name": "Clip07_Cold_Room_Slump",
        "title": "Cold Room, Warm Bed",
        "sceneId": 7,
        "day": "DAY - 4",
        "text": "You wake up tired. The room is cold. Your bed is warm.",
    },
    {
        "id": 8,
        "name": "Clip08_Vanished_Fire",
        "title": "Vanished Tuesday Fire",
        "sceneId": 8,
        "day": "DAY - 4",
        "text": "And suddenly, that fiery motivation from Tuesday has vanished into thin air.",
    },
    {
        "id": 9,
        "name": "Clip09_Negotiate_Alarm",
        "title": "30-Second Negotiation",
        "sceneId": 9,
        "day": "DAY - 4",
        "text": "You negotiate with yourself for thirty seconds, turn off the alarm, and fall back asleep.",
    },
    {
        "id": 10,
        "name": "Clip10_Noon_Guilt",
        "title": "The Weight of Guilt",
        "sceneId": 10,
        "day": "DAY - 4",
        "text": "By noon, the familiar weight of guilt sets in. You tell yourself you lack discipline. You tell yourself you are just lazy.",
    },
    {
        "id": 11,
        "name": "Clip11_Senior_Truth",
        "title": "Senior Mentor Wisdom",
        "sceneId": 11,
        "day": "DAY - 5",
        "text": "Here is the truth an experienced senior will tell you.",
    },
    {
        "id": 12,
        "name": "Clip12_Willpower_Broken",
        "title": "The Wrong Job for Willpower",
        "sceneId": 12,
        "day": "DAY - 5",
        "text": "You did not fail because you lack willpower. You failed because you asked willpower to do a job it was never built for.",
    },
    {
        "id": 13,
        "name": "Clip13_Survival_Brain",
        "title": "Survival Organ Not Inspiration Machine",
        "sceneId": 13,
        "day": "DAY - 5",
        "text": "Your brain is not an inspiration machine. Your brain is a survival organ designed to conserve energy.",
    },
    {
        "id": 14,
        "name": "Clip14_Biology_Alarm",
        "title": "Biology Sounds the Alarm",
        "sceneId": 14,
        "day": "DAY - 5",
        "text": "The moment you attempt a massive, radical overhaul overnight, your biology sounds the alarm. It treats that sudden spike in effort like a threat.",
    },
    {
        "id": 15,
        "name": "Clip15_Gym_vs_Study",
        "title": "IronForge Gym vs Tea Routine",
        "sceneId": 15,
        "day": "DAY - 5",
        "text": "People who stay consistent year after year are not suffering through superhuman acts of discipline every morning.",
    },
    {
        "id": 16,
        "name": "Clip16_Eliminate_Choice",
        "title": "Elimination of Choice",
        "sceneId": 16,
        "day": "DAY - 14",
        "text": "Consistency is not an act of willpower, it is the elimination of choice.",
    },
    {
        "id": 17,
        "name": "Clip17_No_Negotiation_7AM",
        "title": "No Negotiation at 7 AM",
        "sceneId": 17,
        "day": "DAY - 14",
        "text": "They do not negotiate with their feelings at seven in the morning.",
    },
    {
        "id": 18,
        "name": "Clip18_No_Mood_Waiting",
        "title": "Opening Laptop Without Mood",
        "sceneId": 18,
        "day": "DAY - 14",
        "text": "They do not wait for the mood to strike them before opening the laptop.",
    },
    {
        "id": 19,
        "name": "Clip19_Engineer_Environment",
        "title": "Engineer the Environment",
        "sceneId": 19,
        "day": "DAY - 14",
        "text": "Instead, they engineer the environment so that starting requires less effort than feeling guilty.",
    },
    {
        "id": 20,
        "name": "Clip20_Friction_Trilogy",
        "title": "Phone Away, Shoes Ready, Blank Doc",
        "sceneId": 20,
        "day": "DAY - 21",
        "text": "Phone in another room. Shoes directly by doorway. Blank document open before bed.",
    },
    {
        "id": 21,
        "name": "Clip21_Riverbed_vs_Boulder",
        "title": "Carve Riverbed Not Push Boulder",
        "sceneId": 21,
        "day": "DAY - 21",
        "text": "They carve a riverbed where water flows naturally, instead of pushing a giant boulder up a muddy hill every day.",
    },
    {
        "id": 22,
        "name": "Clip22_Stop_Legendary_Days",
        "title": "Stop Aiming for Exhausting Days",
        "sceneId": 22,
        "day": "DAY - 21",
        "text": "Stop aiming for legendary days that leave you exhausted and broken by Friday.",
    },
    {
        "id": 23,
        "name": "Clip23_Lower_The_Barrier",
        "title": "Make Resistance Ridiculous",
        "sceneId": 23,
        "day": "DAY - 21",
        "text": "Lower the barrier until resistance becomes ridiculous.",
    },
    {
        "id": 24,
        "name": "Clip24_Two_Minute_Rule",
        "title": "Two Minutes in Chair, One Paragraph",
        "sceneId": 24,
        "day": "DAY - 30",
        "text": "Sit in the chair for two minutes. Write one clean paragraph. Put on the sneakers and step outside.",
    },
    {
        "id": 25,
        "name": "Clip25_Cast_Small_Vote",
        "title": "Cast Small Vote & Let Momentum Lift",
        "sceneId": 25,
        "day": "DAY - 30",
        "text": "Cast one small vote for the person you want to become, and let momentum do the heavy lifting.",
    },
]

AUDIO_CLIPS_DIR = "remotion/public/audio/ep02/clips"
MASTER_AUDIO = "remotion/public/audio/ep02_voiceover.mp3"
CLIPS_SRC_DIR = "remotion/src/compositions/sticky_in_dark/long/ep02_the_consistency_paradox/clips"

def get_duration(p: str) -> float:
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        p
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

async def run():
    os.makedirs(AUDIO_CLIPS_DIR, exist_ok=True)
    os.makedirs(CLIPS_SRC_DIR, exist_ok=True)
    os.makedirs("scratch/temp_clips", exist_ok=True)

    manifest = []
    accum_frame = 0

    print(f"Generating {len(CLIPS)} clip-wise audio files with strict {STRICT_PAUSE_SEC}s pause...")

    for clip in CLIPS:
        c_id = clip["id"]
        raw_p = f"scratch/temp_clips/raw_{c_id:02d}.mp3"
        out_p = f"{AUDIO_CLIPS_DIR}/clip_{c_id:02d}.mp3"

        # 1. Edge-TTS synthesis
        comm = edge_tts.Communicate(clip["text"], VOICE, rate=RATE, pitch=PITCH)
        await comm.save(raw_p)

        raw_dur = get_duration(raw_p)

        # 2. Add STRICT 0.25s pause at the end using apad
        cmd = [
            "ffmpeg", "-y", "-i", raw_p,
            "-af", f"apad=pad_dur={STRICT_PAUSE_SEC}",
            "-c:a", "libmp3lame", "-b:a", "192k",
            out_p
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        total_dur = get_duration(out_p)
        dur_frames = int(round(total_dur * FPS))

        start_frame = accum_frame
        end_frame = accum_frame + dur_frames
        accum_frame = end_frame

        clip_data = {
            "id": c_id,
            "name": clip["name"],
            "title": clip["title"],
            "sceneId": clip["sceneId"],
            "day": clip["day"],
            "text": clip["text"],
            "rawDurationSec": round(raw_dur, 3),
            "pauseSec": STRICT_PAUSE_SEC,
            "totalDurationSec": round(total_dur, 3),
            "durationFrames": dur_frames,
            "startFrame": start_frame,
            "endFrame": end_frame,
            "audioRelPath": f"audio/ep02/clips/clip_{c_id:02d}.mp3",
        }
        manifest.append(clip_data)
        print(f"[{c_id:02d}/25] {clip['name']}: Speech={raw_dur:.2f}s + Pause={STRICT_PAUSE_SEC}s = {total_dur:.2f}s ({dur_frames} frames)")

    # 3. Concatenate all clip audios into master audio
    concat_list = "scratch/temp_clips/concat_clips.txt"
    with open(concat_list, "w") as f:
        for m in manifest:
            abs_p = os.path.abspath(f"{AUDIO_CLIPS_DIR}/clip_{m['id']:02d}.mp3").replace("\\", "/")
            f.write(f"file '{abs_p}'\n")

    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        MASTER_AUDIO
    ]
    subprocess.run(concat_cmd, check=True)
    master_dur = get_duration(MASTER_AUDIO)
    master_frames = int(round(master_dur * FPS))
    print(f"\nConcatenated Master Audio: {MASTER_AUDIO}")
    print(f"Total Duration: {master_dur:.2f}s = {master_frames} frames @ {FPS}fps")

    # 4. Save manifest JSON
    with open("scratch/clip_manifest.json", "w") as f:
        json.dump({
            "strictPauseSec": STRICT_PAUSE_SEC,
            "totalDurationSec": master_dur,
            "totalFrames": master_frames,
            "fps": FPS,
            "clips": manifest
        }, f, indent=2)

    return manifest, master_frames

if __name__ == "__main__":
    asyncio.run(run())
