"""
Generates the clip-wise Remotion composition components and updates Root.tsx and the manifests.
"""

import os
import json

MANIFEST_PATH = "scratch/clip_manifest.json"
CLIPS_BASE_DIR = "remotion/src/compositions/sticky_in_dark/long/ep02_the_consistency_paradox/clips"

with open(MANIFEST_PATH, "r") as f:
    data = json.load(f)

clips = data["clips"]
total_frames = data["totalFrames"]

os.makedirs(CLIPS_BASE_DIR, exist_ok=True)

# 1. Generate each clip folder and index.tsx
for clip in clips:
    c_id = clip["id"]
    folder_name = f"clip_{c_id:02d}"
    clip_dir = os.path.join(CLIPS_BASE_DIR, folder_name)
    os.makedirs(clip_dir, exist_ok=True)

    is_danger = clip["day"] == "DAY - 4"
    audio_path = f"audio/ep02/clips/clip_{c_id:02d}.mp3"
    scene_id = clip["sceneId"]
    frames = clip["durationFrames"]

    code = f"""import React from "react";
import {{ AbsoluteFill, Audio, staticFile }} from "remotion";
import {{ ThreeStage }} from "../../../../../../three/ThreeStage";

export const {clip['name']}Composition: React.FC = () => {{
  // Camera framing for Scene {scene_id} ({clip['title']})
  const cameraConfig = {{
    shotId: {scene_id},
    startFrame: 0,
    endFrame: {frames},
    startPos: [0, 1.5, 4.2] as [number, number, number],
    endPos: [0, 1.4, 3.6] as [number, number, number],
    target: [0, 1.0, 0] as [number, number, number],
    fov: 40,
  }};

  return (
    <AbsoluteFill style={{{{ backgroundColor: "#0A0E17" }}}}>
      {{/* Clip-Specific Voiceover Audio */}}
      <Audio src={{staticFile("{audio_path}")}} volume={{1.0}} />
      <Audio src={{staticFile("audio/bgm.mp3")}} volume={{0.08}} />

      {{/* 3D Voxel Scene */}}
      <ThreeStage shots={{[cameraConfig]}} />

      {{/* Subtle Film Vignette */}}
      <AbsoluteFill
        style={{{{
          boxShadow: "inset 0 0 140px rgba(0, 0, 0, 0.70)",
          pointerEvents: "none",
        }}}}
      />

      {{/* Top-Left Day Progression Badge */}}
      <div
        style={{{{
          position: "absolute",
          top: 32,
          left: 42,
          display: "flex",
          alignItems: "center",
          gap: 9,
          backgroundColor: "rgba(10, 14, 23, 0.82)",
          padding: "6px 16px",
          borderRadius: 6,
          border: { "true" if is_danger else "false" }
            ? "1px solid rgba(255, 42, 77, 0.4)"
            : "1px solid rgba(0, 240, 255, 0.25)",
          backdropFilter: "blur(6px)",
          boxShadow: "0 4px 16px rgba(0, 0, 0, 0.55)",
          pointerEvents: "none",
          zIndex: 15,
        }}}}
      >
        <div
          style={{{{
            width: 8,
            height: 8,
            borderRadius: "50%",
            backgroundColor: { "true" if is_danger else "false" } ? "#FF2A4D" : "#00F0FF",
            boxShadow: { "true" if is_danger else "false" }
              ? "0 0 8px #FF2A4D"
              : "0 0 8px #00F0FF",
          }}}}
        />
        <span
          style={{{{
            fontFamily: "'Arial Black', Impact, sans-serif",
            fontSize: 16,
            fontWeight: 900,
            color: "#FFFFFF",
            letterSpacing: "0.08em",
          }}}}
        >
          {clip['day']}
        </span>
      </div>

      {{/* Synchronized Caption */}}
      <div
        style={{{{
          position: "absolute",
          bottom: 38,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          padding: "0 80px",
          pointerEvents: "none",
          zIndex: 20,
        }}}}
      >
        <div
          style={{{{
            backgroundColor: "rgba(10, 14, 23, 0.88)",
            padding: "10px 24px",
            borderRadius: 6,
            border: "1px solid rgba(255, 255, 255, 0.12)",
            boxShadow: "0 8px 32px rgba(0, 0, 0, 0.65)",
            backdropFilter: "blur(6px)",
          }}}}
        >
          <span
            style={{{{
              fontFamily: "'Arial Black', Impact, sans-serif",
              fontSize: 22,
              fontWeight: 900,
              color: "#FFFFFF",
              textAlign: "center",
              lineHeight: 1.35,
              textTransform: "uppercase",
              letterSpacing: "0.03em",
            }}}}
          >
            {json.dumps(clip['text'])}
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
}};
"""
    with open(os.path.join(clip_dir, "index.tsx"), "w", encoding="utf-8") as f:
        f.write(code)

print("Generated all 25 clip index.tsx files!")

# 2. Generate clips/index.ts
clips_export_lines = []
for clip in clips:
    c_id = clip["id"]
    folder_name = f"clip_{c_id:02d}"
    name = clip["name"]
    clips_export_lines.append(f'export {{ {name}Composition }} from "./{folder_name}";')

clips_export_code = "\n".join(clips_export_lines) + f"\n\nexport const CLIPS_METADATA = {json.dumps(clips, indent=2)};\n"
with open(os.path.join(CLIPS_BASE_DIR, "index.ts"), "w", encoding="utf-8") as f:
    f.write(clips_export_code)

print("Generated clips/index.ts!")

# 3. Update subtitles.ts for master sequence
sub_entries = []
for clip in clips:
    sub_entries.append(f"""  {{
    start: {clip['startFrame']},
    end: {clip['endFrame']},
    text: {json.dumps(clip['text'])},
  }},""")

sub_file_content = f"""export interface SubtitleTiming {{
  start: number;
  end: number;
  text: string;
}}

/**
 * Clean 25-Beat Synchronized Subtitles (Strict 0.25s Pause)
 * Total Duration: {total_frames} frames @ 30fps ({data['totalDurationSec']:.2f}s)
 */
export const SUBTITLES_TIMINGS: SubtitleTiming[] = [
{chr(10).join(sub_entries)}
];
"""
with open("remotion/src/compositions/sticky_in_dark/long/ep02_the_consistency_paradox/subtitles.ts", "w", encoding="utf-8") as f:
    f.write(sub_file_content)

print("Updated subtitles.ts!")

# 4. Update cameraPaths.ts for master sequence
cam_entries = []
for clip in clips:
    c_id = clip["id"]
    start_f = clip["startFrame"]
    end_f = clip["endFrame"]
    title = clip["title"]
    
    # Custom camera settings per scene
    if c_id == 1:
        sp, ep, tg, fov = "[-1.3, 1.7, 1.1]", "[-0.7, 1.35, 0.65]", "[0.5, 0.75, -0.9]", 42
    elif c_id == 2:
        sp, ep, tg, fov = "[-3.0, 1.6, 3.8]", "[1.8, 1.6, 3.8]", "[0, 1.2, 0]", 40
    elif c_id == 3:
        sp, ep, tg, fov = "[2.8, 2.2, 2.5]", "[-1.8, 2.2, 2.5]", "[0, 1.1, -0.8]", 38
    elif c_id == 4:
        sp, ep, tg, fov = "[0, 1.4, 2.2]", "[0, 1.3, 1.6]", "[0, 1.1, -0.6]", 35
    elif c_id == 5:
        sp, ep, tg, fov = "[0, 1.2, 4.5]", "[0, 2.2, 3.5]", "[0, 2.0, 0]", 42
    elif c_id == 6:
        sp, ep, tg, fov = "[0, 0.4, 4.8]", "[0, 0.4, 4.5]", "[0, 0.3, 0]", 30
    elif c_id == 7:
        sp, ep, tg, fov = "[0, 4.8, 2.5]", "[0, 3.2, 1.8]", "[0.2, 0.4, -0.9]", 42
    elif c_id == 8:
        sp, ep, tg, fov = "[0, 1.3, 2.4]", "[0, 1.3, 1.5]", "[0, 1.2, 0]", 32
    elif c_id == 9:
        sp, ep, tg, fov = "[2.5, 1.3, 0.8]", "[1.8, 1.1, 0.2]", "[0.6, 0.85, -0.2]", 36
    elif c_id == 10:
        sp, ep, tg, fov = "[-1.2, 2.5, 3.2]", "[-0.4, 1.2, 2.4]", "[0, 0.7, 0]", 42
    elif c_id == 11:
        sp, ep, tg, fov = "[0, 1.4, 4.0]", "[0, 1.4, 2.6]", "[0, 1.3, 0]", 34
    elif c_id == 12:
        sp, ep, tg, fov = "[-2.2, 1.8, 3.2]", "[1.8, 1.6, 2.8]", "[-0.3, 1.0, 0]", 38
    elif c_id == 13:
        sp, ep, tg, fov = "[0, 1.8, 4.2]", "[0, 1.8, 2.2]", "[0, 1.6, 0]", 32
    elif c_id == 14:
        sp, ep, tg, fov = "[2.0, 1.6, 3.8]", "[-1.5, 1.2, 3.0]", "[0, 1.1, 0]", 40
    elif c_id == 15:
        sp, ep, tg, fov = "[0, 1.6, 5.8]", "[0, 1.5, 5.2]", "[0, 1.1, -0.6]", 46
    elif c_id == 16:
        sp, ep, tg, fov = "[0, 2.2, 6.0]", "[0, 1.4, 3.2]", "[0, 1.3, 0]", 36
    elif c_id == 17:
        sp, ep, tg, fov = "[1.8, 1.2, 2.4]", "[0.8, 1.2, 2.2]", "[0, 0.9, 0]", 30
    elif c_id == 18:
        sp, ep, tg, fov = "[0.7, 1.7, 1.8]", "[0.3, 1.4, 1.1]", "[0, 1.1, -0.6]", 34
    elif c_id == 19:
        sp, ep, tg, fov = "[0, 5.5, 0.2]", "[0, 3.8, 0.1]", "[0, 0, 0]", 45
    elif c_id == 20:
        sp, ep, tg, fov = "[-3.2, 1.6, 3.2]", "[3.2, 1.6, 3.2]", "[0, 1.1, 0]", 38
    elif c_id == 21:
        sp, ep, tg, fov = "[-3.8, 2.8, 5.2]", "[2.4, 2.2, 4.5]", "[0, 1.1, 0]", 45
    elif c_id == 22:
        sp, ep, tg, fov = "[0, 0.6, 2.2]", "[0, 1.4, 3.5]", "[0, 0.7, 0]", 36
    elif c_id == 23:
        sp, ep, tg, fov = "[2.2, 1.1, 2.8]", "[1.0, 1.1, 2.6]", "[0, 0.7, 0]", 32
    elif c_id == 24:
        sp, ep, tg, fov = "[-1.8, 1.4, 2.8]", "[1.8, 1.4, 2.8]", "[0, 1.1, 0]", 35
    else:
        sp, ep, tg, fov = "[0, 1.4, 2.8]", "[0, 2.8, 7.5]", "[0, 1.6, 0]", 42

    cam_entries.append(f"""  // Shot {c_id}: {title}
  {{
    shotId: {c_id},
    startFrame: {start_f},
    endFrame: {end_f},
    startPos: {sp},
    endPos: {ep},
    target: {tg},
    fov: {fov},
  }},""")

camera_file_content = f"""import {{ ShotCameraConfig }} from "../../../../three/ThreeStage";

/**
 * 25-Shot Cinematic Camera Configurations
 * Synchronized with the {total_frames} frames ({data['totalDurationSec']:.2f}s) master deep motivational voiceover.
 * Strict pause of 0.25s between shots.
 */
export const SHOT_CAMERA_PATHS: ShotCameraConfig[] = [
{chr(10).join(cam_entries)}
];
"""
with open("remotion/src/compositions/sticky_in_dark/long/ep02_the_consistency_paradox/cameraPaths.ts", "w", encoding="utf-8") as f:
    f.write(camera_file_content)

print("Updated cameraPaths.ts!")
