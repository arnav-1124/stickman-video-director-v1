import React from "react";
import { AbsoluteFill, Audio, staticFile } from "remotion";
import { ThreeStage } from "../../../../../three/ThreeStage";

export const Clip17_No_Negotiation_7AMComposition: React.FC = () => {
  // Camera framing for Scene 17 (No Negotiation at 7 AM)
  const cameraConfig = {
    shotId: 17,
    startFrame: 0,
    endFrame: 134,
    startPos: [-2.60, 1.65, 1.80] as [number, number, number],
    endPos: [-2.10, 1.50, 1.20] as [number, number, number],
    target: [0.10, 0.95, -0.60] as [number, number, number],
    fov: 44,
  };

  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0E17" }}>
      {/* Clip-Specific Voiceover Audio */}
      <Audio src={staticFile("audio/ep02/clips/clip_17.mp3")} volume={1.0} />
      <Audio src={staticFile("audio/bgm.mp3")} volume={0.08} />

      {/* 3D Voxel Scene */}
      <ThreeStage shots={[cameraConfig]} />

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
          DAY - 14
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
            "They do not negotiate with their feelings at seven in the morning."
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
