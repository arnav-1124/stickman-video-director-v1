import React from "react";
import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame } from "remotion";
import { ShotCameraConfig, ThreeStage } from "../../../../../three/ThreeStage";

export const Clip05_Invincible_PeakComposition: React.FC = () => {
  const frame = useCurrentFrame();

  // =========================================================================
  // SCENE 5: FEELING INVINCIBLE ON THE MOUNTAIN PEAK
  // Narration: "You feel invincible. You feel like you finally unlocked the secret everyone else is missing."
  // Duration: 208 frames (~6.95s @ 30fps)
  //
  // Visual Choreography:
  // ONE SINGLE FULLY CONTINUOUS, UNBROKEN CINEMATIC CAMERA SHOT (Frames 0 to 208):
  // - Starts tightly zoomed-in on the summit plateau: Alex standing heroically
  //   beside the waving victory flag against the golden morning sunrise.
  // - Smoothly and continuously dollies backward, rises up into an epic crane vista,
  //   revealing the grand 12-step mountain staircase with 8 climbers struggling below:
  //   * 3 on the ground at the mountain base (one gazing up overwhelmed, one dejected, one hesitant)
  //   * 2 on the first stairs (one stumbling onto step 1, one exhausted on knees on step 2)
  //   * 3 along the mid and upper stairs (one climbing step 5, one resting on step 7, one near top on step 10)
  //   while Alex stands invincible at the peak beside the flag overlooking the world.
  // =========================================================================

  const continuousSummitZoomOut: ShotCameraConfig = {
    shotId: 5,
    startFrame: 0,
    endFrame: 208,
    // Starts close and clean on the summit plateau framing Alex and the full victory banner
    startPos: [-0.05, 5.48, 0.50] as [number, number, number],
    // Smoothly pulls back and elevates into the majestic wide mountain vista
    endPos: [5.0, 11.2, 18.0] as [number, number, number],
    // Target pans smoothly from the summit hero & banner to the grand staircase center
    target: [-0.05, 5.38, -2.00] as [number, number, number],
    endTarget: [0.0, 2.4, 3.2] as [number, number, number],
    fov: 42,
  };

  // Cinematic Seamless Transitions (Zero harsh cuts by default)
  const fadeIn = interpolate(frame, [0, 16], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(frame, [192, 208], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const transitionOpacity = fadeIn * fadeOut;

  // Key phrase timing for subtitle animation
  const phraseTwoActive = frame >= 68;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0E17" }}>
      {/* Clip-Specific Voiceover Audio */}
      <Audio src={staticFile("audio/ep02/clips/clip_05.mp3")} volume={1.0} />
      <Audio src={staticFile("audio/bgm.mp3")} volume={0.08} />

      {/* 3D Voxel Scene with 100% Continuous Unbroken Cinematic Camera Motion */}
      <AbsoluteFill style={{ opacity: transitionOpacity }}>
        <ThreeStage shots={[continuousSummitZoomOut]} />
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
          border: "1px solid rgba(255, 215, 0, 0.35)",
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
            backgroundColor: "#FFD700",
            boxShadow: "0 0 10px #FFD700",
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
          DAY - 2
        </span>
      </div>

      {/* Synchronized Caption (Gold highlight on key phrase matching production law) */}
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
            maxWidth: 1400,
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
            {!phraseTwoActive ? (
              <>
                "You feel <span style={{ color: "#FFD700" }}>invincible</span>."
              </>
            ) : (
              <>
                "You feel like you finally{" "}
                <span style={{ color: "#FFD700" }}>unlocked the secret</span> everyone else is missing."
              </>
            )}
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
