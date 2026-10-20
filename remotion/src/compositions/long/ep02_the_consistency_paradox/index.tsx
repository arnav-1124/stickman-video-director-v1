import React from "react";
import {
  AbsoluteFill,
  Audio,
  interpolate,
  staticFile,
  useCurrentFrame,
} from "remotion";
import { ThreeStage } from "../../../three/ThreeStage";
import { SHOT_CAMERA_PATHS } from "./cameraPaths";
import { SUBTITLES_TIMINGS } from "./subtitles";

export const ConsistencyParadoxComposition: React.FC = () => {
  const frame = useCurrentFrame();

  // Find active shot
  const currentShot =
    SHOT_CAMERA_PATHS.find((s) => frame >= s.startFrame && frame < s.endFrame) ||
    SHOT_CAMERA_PATHS[0];

  // Find active subtitle for current frame
  const activeSub = SUBTITLES_TIMINGS.find(
    (sub) => frame >= sub.start && frame < sub.end
  );

  // Dynamic Day Tracker in sync with narrative script
  let currentDay = "DAY - 1";
  let isDangerDay = false;
  if (frame >= 500 && frame < 818) {
    currentDay = "DAY - 2";
  } else if (frame >= 818 && frame < 1766) {
    currentDay = "DAY - 4";
    isDangerDay = true;
  } else if (frame >= 1766 && frame < 2898) {
    currentDay = "DAY - 5";
  } else if (frame >= 2898 && frame < 3538) {
    currentDay = "DAY - 14";
  } else if (frame >= 3538 && frame < 4311) {
    currentDay = "DAY - 21";
  } else if (frame >= 4311) {
    currentDay = "DAY - 30";
  }

  // Smooth cinematic scene transition overlay (Prevents harsh cuts & trims)
  const framesIntoShot = frame - currentShot.startFrame;
  const transitionOpacity =
    framesIntoShot < 6
      ? interpolate(framesIntoShot, [0, 6], [0.42, 0], {
          extrapolateRight: "clamp",
        })
      : 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0E17" }}>
      {/* Primary Audio Track: Deep, Resonant Male Motivational Voiceover */}
      <Audio src={staticFile("audio/ep02_voiceover.mp3")} volume={1.0} />

      {/* Secondary Audio Track: Cinematic Background Music Bed */}
      <Audio src={staticFile("audio/bgm.mp3")} loop volume={0.10} />

      {/* Layer 1: Three.js Minecraft Voxel 3D World (25 Dedicated Storyboard Shots) */}
      <ThreeStage shots={SHOT_CAMERA_PATHS} />

      {/* Layer 2: Subtle Cinematic Film Vignette */}
      <AbsoluteFill
        style={{
          boxShadow: "inset 0 0 140px rgba(0, 0, 0, 0.70)",
          pointerEvents: "none",
        }}
      />

      {/* Layer 3: Smooth Cinematic Transition Overlay (Eliminates Jarring Hard Cuts) */}
      <AbsoluteFill
        style={{
          backgroundColor: "#0A0E17",
          opacity: transitionOpacity,
          pointerEvents: "none",
          zIndex: 8,
        }}
      />

      {/* Layer 4: Top-Left Day Progression HUD (In Sync with Script) */}
      <div
        style={{
          position: "absolute",
          top: 32,
          left: 42,
          display: "flex",
          alignItems: "center",
          gap: 9,
          backgroundColor: "rgba(10, 14, 23, 0.80)",
          padding: "6px 16px",
          borderRadius: 6,
          border: isDangerDay
            ? "1px solid rgba(255, 42, 77, 0.4)"
            : "1px solid rgba(0, 240, 255, 0.25)",
          backdropFilter: "blur(6px)",
          boxShadow: "0 4px 16px rgba(0, 0, 0, 0.55)",
          pointerEvents: "none",
          zIndex: 15,
        }}
      >
        <span
          style={{
            width: 7,
            height: 7,
            borderRadius: "50%",
            backgroundColor: isDangerDay ? "#FF2A4D" : "#00F0FF",
            boxShadow: isDangerDay ? "0 0 6px #FF2A4D" : "0 0 6px #00F0FF",
            display: "inline-block",
          }}
        />
        <span
          style={{
            fontFamily: "'Arial Black', sans-serif",
            fontSize: 14,
            color: isDangerDay ? "#FF6B81" : "#FFFFFF",
            letterSpacing: "0.08em",
            textTransform: "uppercase",
          }}
        >
          {currentDay}
        </span>
      </div>

      {/* Layer 5: Top-Right Channel Watermark Badge (Sticky in Dark) */}
      <div
        style={{
          position: "absolute",
          top: 32,
          right: 42,
          opacity: 0.88,
          fontFamily: "'Arial Black', sans-serif",
          fontSize: 14,
          color: "#E2E8F0",
          letterSpacing: "0.08em",
          display: "flex",
          alignItems: "center",
          gap: 8,
          pointerEvents: "none",
          backgroundColor: "rgba(10, 14, 23, 0.55)",
          padding: "5px 12px",
          borderRadius: 6,
          border: "1px solid rgba(255, 255, 255, 0.08)",
          zIndex: 15,
        }}
      >
        <span
          style={{
            width: 7,
            height: 7,
            borderRadius: "50%",
            backgroundColor: "#00F0FF",
            display: "inline-block",
            boxShadow: "0 0 6px #00F0FF",
          }}
        />
        STICKY IN DARK
      </div>

      {/* Layer 6: Compact, Sleek Kinetic Subtitles (Lower-Third, 22px) */}
      {activeSub && (
        <div
          style={{
            position: "absolute",
            bottom: 42,
            left: 0,
            right: 0,
            textAlign: "center",
            display: "flex",
            justifyContent: "center",
            pointerEvents: "none",
            zIndex: 20,
          }}
        >
          <div
            style={{
              backgroundColor: "rgba(10, 14, 23, 0.85)",
              padding: "6px 20px",
              borderRadius: 6,
              border: "1px solid rgba(255, 255, 255, 0.12)",
              boxShadow: "0 6px 20px rgba(0, 0, 0, 0.65)",
              backdropFilter: "blur(6px)",
              maxWidth: "70%",
            }}
          >
            <span
              style={{
                fontFamily: "'Arial Black', 'Impact', sans-serif",
                fontSize: 22, // Compact & unobtrusive as requested
                color: "#FFFFFF",
                letterSpacing: "0.03em",
                textTransform: "uppercase",
                textShadow: "0 2px 4px rgba(0, 0, 0, 0.8)",
                lineHeight: 1.35,
              }}
            >
              {activeSub.text}
            </span>
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
