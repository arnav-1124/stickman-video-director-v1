import React from "react";
import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame } from "remotion";
import { ThreeStage } from "../../../../../three/ThreeStage";

export const Clip01_2AM_PromiseComposition: React.FC = () => {
  const frame = useCurrentFrame();

  // Angular Top Camera framing for Scene 1 (5 AM Promise in Bedroom)
  const cameraConfig = {
    shotId: 1,
    startFrame: 0,
    endFrame: 164,
    startPos: [2.7, 2.3, 2.3] as [number, number, number],
    endPos: [2.3, 2.0, 1.9] as [number, number, number],
    target: [-0.1, 0.95, -1.15] as [number, number, number],
    fov: 42,
  };

  // Cinematic seamless cross-transitions by default (No abrupt cuts!)
  const fadeIn = interpolate(frame, [0, 16], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [148, 164], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const transitionOpacity = fadeIn * fadeOut;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0E17" }}>
      {/* Clip-Specific Voiceover Audio */}
      <Audio src={staticFile("audio/ep02/clips/clip_01.mp3")} volume={1.0} />
      <Audio src={staticFile("audio/bgm.mp3")} volume={0.08} />

      {/* 3D Voxel Scene with Smooth Transition */}
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
    </AbsoluteFill>
  );
};
