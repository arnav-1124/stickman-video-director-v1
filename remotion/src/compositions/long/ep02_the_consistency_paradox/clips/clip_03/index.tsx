import React from "react";
import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame } from "remotion";
import { ThreeStage } from "../../../../../three/ThreeStage";

export const Clip03_Executive_OfficeComposition: React.FC = () => {
  const frame = useCurrentFrame();

  // Cinematic Doorway Entrance Camera:
  // Glides smoothly through the side wall door opening from the hallway into the office,
  // framing Alex working on his laptop, the picture & golden trophy, notepad, and coffee cup.
  const cameraConfig = {
    shotId: 3,
    startFrame: 0,
    endFrame: 182,
    startPos: [-3.70, 1.48, 1.35] as [number, number, number],
    endPos: [-1.80, 1.32, 0.45] as [number, number, number],
    target: [-0.05, 1.05, -0.80] as [number, number, number],
    endTarget: [-0.02, 1.02, -0.78] as [number, number, number],
    fov: 42,
  };

  // Cinematic Seamless Cross-Fade Transitions by default (No harsh jump cuts!)
  const fadeIn = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [164, 182], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const transitionOpacity = fadeIn * fadeOut;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0E17" }}>
      {/* Clip-Specific Voiceover Audio */}
      <Audio src={staticFile("audio/ep02/clips/clip_03.mp3")} volume={1.0} />
      <Audio src={staticFile("audio/bgm.mp3")} volume={0.08} />

      {/* 3D Voxel Scene with Smooth Fade Transition */}
      <AbsoluteFill style={{ opacity: transitionOpacity }}>
        <ThreeStage shots={[cameraConfig]} />
      </AbsoluteFill>

      {/* Subtle Film Vignette */}
      <AbsoluteFill
        style={{
          boxShadow: "inset 0 0 140px rgba(0, 0, 0, 0.70)",
          pointerEvents: "none",
        }}
      />

      {/* Top-Left Day Progression Badge */}
      <div
        style={{
          position: "absolute",
          top: 32,
          left: 42,
          display: "flex",
          alignItems: "center",
          gap: 9,
          backgroundColor: "rgba(10, 14, 23, 0.82)",
          padding: "6px 16px",
          borderRadius: 6,
          border: false
            ? "1px solid rgba(255, 42, 77, 0.4)"
            : "1px solid rgba(0, 240, 255, 0.25)",
          backdropFilter: "blur(6px)",
          boxShadow: "0 4px 16px rgba(0, 0, 0, 0.55)",
          pointerEvents: "none",
          zIndex: 15,
        }}
      >
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            backgroundColor: false ? "#FF2A4D" : "#00F0FF",
            boxShadow: false
              ? "0 0 8px #FF2A4D"
              : "0 0 8px #00F0FF",
          }}
        />
        <span
          style={{
            fontFamily: "'Arial Black', Impact, sans-serif",
            fontSize: 16,
            fontWeight: 900,
            color: "#FFFFFF",
            letterSpacing: "0.08em",
          }}
        >
          DAY - 1
        </span>
      </div>

      {/* Synchronized Caption */}
      <div
        style={{
          position: "absolute",
          bottom: 38,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          padding: "0 80px",
          pointerEvents: "none",
          zIndex: 20,
        }}
      >
        <div
          style={{
            backgroundColor: "rgba(10, 14, 23, 0.88)",
            padding: "10px 24px",
            borderRadius: 6,
            border: "1px solid rgba(255, 255, 255, 0.12)",
            boxShadow: "0 8px 32px rgba(0, 0, 0, 0.65)",
            backdropFilter: "blur(6px)",
          }}
        >
          <span
            style={{
              fontFamily: "'Arial Black', Impact, sans-serif",
              fontSize: 22,
              fontWeight: 900,
              color: "#FFFFFF",
              textAlign: "center",
              lineHeight: 1.35,
              textTransform: "uppercase",
              letterSpacing: "0.03em",
            }}
          >
            "You will work for eight unbroken hours, eat clean, and finally master your life."
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
