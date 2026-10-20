import React from "react";
import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame } from "remotion";
import { ThreeStage } from "../../../../../three/ThreeStage";

export const Clip02_Dawn_RunComposition: React.FC = () => {
  const frame = useCurrentFrame();

  // Phase 1: 5:00 AM Dawn Bedroom (Wakeup sequence from window wall angle)
  // Camera comes from the window wall, looking across the bed with morning sunlight streaming in,
  // showing Alex awakening naturally, the nightstand with 5:00 AM clock, and face-down phone.
  const bedroomCamera = {
    shotId: 201,
    startFrame: 0,
    endFrame: 85,
    startPos: [-2.45, 1.40, 0.20] as [number, number, number],
    endPos: [-2.20, 1.35, -0.05] as [number, number, number],
    target: [0.70, 0.90, -0.90] as [number, number, number],
    fov: 48,
  };

  // Phase 2: Morning Park Run (Dynamic low-angle follow camera behind Alex, tracking around the park turn)
  const parkChaseShot = {
    shotId: 2,
    startFrame: 65,
    endFrame: 154,
    startPos: [0.0, 0.50, -7.3] as [number, number, number],
    endPos: [3.4, 0.50, 3.0] as [number, number, number],
    target: [0.0, 1.05, -3.9] as [number, number, number],
    endTarget: [6.8, 1.05, 3.0] as [number, number, number],
    fov: 46,
  };

  const parkShots = [parkChaseShot];

  // Clip 1 to Clip 2 Story Transition: Smooth dawn awakening fade-in from midnight darkness
  const dawnArrivalFade = interpolate(frame, [0, 14], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Seamless cinematic cross-transition (No cut!) when voice says "You will run..."
  const bedroomOpacity = interpolate(frame, [68, 80], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const parkOpacity = interpolate(frame, [68, 80], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const parkFadeOut = interpolate(frame, [140, 154], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Morning sunflare bloom wash bridging the window sunlight into the outdoor park
  const sunflareWash = interpolate(frame, [68, 74, 80], [0, 0.42, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0E17" }}>
      {/* Clip-Specific Voiceover Audio */}
      <Audio src={staticFile("audio/ep02/clips/clip_02.mp3")} volume={1.0} />
      <Audio src={staticFile("audio/bgm.mp3")} volume={0.08} />

      {/* Layer 1: 5:00 AM Dawn Bedroom (Frames 0 - 80) */}
      {frame <= 82 && (
        <AbsoluteFill style={{ opacity: bedroomOpacity * dawnArrivalFade }}>
          <ThreeStage shots={[bedroomCamera]} />
        </AbsoluteFill>
      )}

      {/* Layer 2: Morning Park Run (Frames 68 - 154) */}
      {frame >= 66 && (
        <AbsoluteFill style={{ opacity: parkOpacity * parkFadeOut }}>
          <ThreeStage shots={parkShots} />
        </AbsoluteFill>
      )}

      {/* Layer 3: Morning Sunbeam Flare Wash (Zero-cut continuous light bridge) */}
      {sunflareWash > 0.01 && (
        <AbsoluteFill
          style={{
            backgroundColor: "#FFF0C2",
            opacity: sunflareWash,
            mixBlendMode: "screen",
            pointerEvents: "none",
          }}
        />
      )}

      {/* Subtle Film Vignette */}
      <AbsoluteFill
        style={{
          boxShadow: "inset 0 0 140px rgba(0, 0, 0, 0.65)",
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
          border: "1px solid rgba(0, 240, 255, 0.25)",
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
            backgroundColor: "#00F0FF",
            boxShadow: "0 0 8px #00F0FF",
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

