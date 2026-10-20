import React from "react";
import { AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame } from "remotion";
import { ShotCameraConfig, ThreeStage } from "../../../../../three/ThreeStage";

export const Clip04_Two_Days_VictoryComposition: React.FC = () => {
  const frame = useCurrentFrame();

  // =========================================================================
  // FAST-FORWARD MONTAGE: 2 DAYS OF PERFECT EXECUTION
  // Narration: "And for two days, you actually do it." (Duration: 110 frames / ~3.67s)
  // Replays the daily 3-habit cycle twice in fast-forward mode:
  // - Cycle 1 (Day 2): Frames 0 to 55 (Bedroom Wakeup -> Park Run -> Office Work)
  // - Cycle 2 (Day 3): Frames 55 to 110 (Bedroom Wakeup -> Park Run -> Office Work)
  // All cuts feature silky smooth cross-dissolves and light bridge washes.
  // =========================================================================

  // --- CYCLE 1: DAY 2 SHOT CONFIGS ---
  // Sub-shot 1: 5:00 AM Dawn Bedroom Wakeup (Shot 21)
  const c1Bedroom: ShotCameraConfig = {
    shotId: 21,
    startFrame: 0,
    endFrame: 20,
    startPos: [-2.45, 1.40, 0.20],
    endPos: [-2.10, 1.30, -0.10],
    target: [0.70, 0.90, -0.90],
    fov: 48,
    timeRange: [0.3, 1.8], // Full wakeup in fast-forward!
  };

  // Sub-shot 2: Morning Park Run (Shot 2)
  const c1Park: ShotCameraConfig = {
    shotId: 2,
    startFrame: 16,
    endFrame: 38,
    startPos: [0.0, 0.50, -7.3],
    endPos: [3.4, 0.50, 3.0],
    target: [0.0, 1.05, -3.9],
    endTarget: [6.8, 1.05, 3.0],
    fov: 46,
    timeRange: [2.25, 5.15], // Full sprint and 90-degree bank turn in fast-forward!
  };

  // Sub-shot 3: Executive Office Desk & Laptop (Shot 3)
  const c1Office: ShotCameraConfig = {
    shotId: 3,
    startFrame: 34,
    endFrame: 56,
    startPos: [-3.70, 1.48, 1.35],
    endPos: [-1.80, 1.32, 0.45],
    target: [-0.05, 1.05, -0.80],
    endTarget: [-0.02, 1.02, -0.78],
    fov: 42,
    timeRange: [0.0, 4.0], // Rapid keystroke typing vibrations!
  };

  // --- CYCLE 2: DAY 3 SHOT CONFIGS ---
  // Sub-shot 4: 5:00 AM Dawn Bedroom Wakeup (Shot 21)
  const c2Bedroom: ShotCameraConfig = {
    shotId: 21,
    startFrame: 53,
    endFrame: 74,
    startPos: [-2.45, 1.40, 0.20],
    endPos: [-2.10, 1.30, -0.10],
    target: [0.70, 0.90, -0.90],
    fov: 48,
    timeRange: [0.3, 1.8],
  };

  // Sub-shot 5: Morning Park Run (Shot 2)
  const c2Park: ShotCameraConfig = {
    shotId: 2,
    startFrame: 70,
    endFrame: 92,
    startPos: [0.0, 0.50, -7.3],
    endPos: [3.4, 0.50, 3.0],
    target: [0.0, 1.05, -3.9],
    endTarget: [6.8, 1.05, 3.0],
    fov: 46,
    timeRange: [2.25, 5.15],
  };

  // Sub-shot 6: Executive Office Desk & Laptop (Shot 3)
  const c2Office: ShotCameraConfig = {
    shotId: 3,
    startFrame: 88,
    endFrame: 110,
    startPos: [-3.70, 1.48, 1.35],
    endPos: [-1.80, 1.32, 0.45],
    target: [-0.05, 1.05, -0.80],
    endTarget: [-0.02, 1.02, -0.78],
    fov: 42,
    timeRange: [0.0, 4.0],
  };

  // =========================================================================
  // CINEMATIC SEAMLESS CROSS-FADES (NO HARD CUTS)
  // =========================================================================
  const globalFadeIn = interpolate(frame, [0, 10], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const globalFadeOut = interpolate(frame, [100, 110], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Cycle 1 Opacity Curves
  const c1BedOpacity = interpolate(frame, [16, 21], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const c1ParkIn = interpolate(frame, [16, 21], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const c1ParkOut = interpolate(frame, [34, 39], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const c1ParkOpacity = c1ParkIn * c1ParkOut;

  const c1OfficeIn = interpolate(frame, [34, 39], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const c1OfficeOut = interpolate(frame, [53, 57], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const c1OfficeOpacity = c1OfficeIn * c1OfficeOut;

  // Cycle 2 Opacity Curves
  const c2BedIn = interpolate(frame, [53, 57], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const c2BedOut = interpolate(frame, [70, 75], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const c2BedOpacity = c2BedIn * c2BedOut;

  const c2ParkIn = interpolate(frame, [70, 75], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const c2ParkOut = interpolate(frame, [88, 93], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const c2ParkOpacity = c2ParkIn * c2ParkOut;

  const c2OfficeOpacity = interpolate(frame, [88, 93], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Light bridge washes during rapid scene shifts
  const lightWash1 = interpolate(frame, [17, 20, 23], [0, 0.35, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const lightWash2 = interpolate(frame, [35, 38, 41], [0, 0.30, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const dayBridgeWash = interpolate(frame, [53, 56, 59], [0, 0.45, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const lightWash3 = interpolate(frame, [71, 74, 77], [0, 0.35, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const lightWash4 = interpolate(frame, [89, 92, 95], [0, 0.30, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const totalLightWash = Math.max(lightWash1, lightWash2, dayBridgeWash, lightWash3, lightWash4);

  // Day Progression Badge (Day 2 for frames 0-55, Day 3 for frames 55-110)
  const isDay3 = frame >= 55;
  const dayBadgeFlip = interpolate(frame, [52, 55, 58], [1, 0.2, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Fast forward indicator pulse
  const ffPulse = 0.75 + 0.25 * Math.sin(frame * 0.45);

  return (
    <AbsoluteFill style={{ backgroundColor: "#0A0E17", opacity: globalFadeIn * globalFadeOut }}>
      {/* Clip-Specific Voiceover Audio */}
      <Audio src={staticFile("audio/ep02/clips/clip_04.mp3")} volume={1.0} />
      <Audio src={staticFile("audio/bgm.mp3")} volume={0.08} />

      {/* ===================================================================
          CYCLE 1: DAY 2 EXECUTION (Frames 0 to 56)
          =================================================================== */}
      {/* Cycle 1 - Shot 1: Bedroom Wakeup */}
      {frame <= 22 && (
        <AbsoluteFill style={{ opacity: c1BedOpacity }}>
          <ThreeStage shots={[c1Bedroom]} />
        </AbsoluteFill>
      )}

      {/* Cycle 1 - Shot 2: Morning Park Run */}
      {frame >= 15 && frame <= 40 && (
        <AbsoluteFill style={{ opacity: c1ParkOpacity }}>
          <ThreeStage shots={[c1Park]} />
        </AbsoluteFill>
      )}

      {/* Cycle 1 - Shot 3: Executive Office Desk */}
      {frame >= 33 && frame <= 58 && (
        <AbsoluteFill style={{ opacity: c1OfficeOpacity }}>
          <ThreeStage shots={[c1Office]} />
        </AbsoluteFill>
      )}

      {/* ===================================================================
          CYCLE 2: DAY 3 REPEAT EXECUTION (Frames 52 to 110)
          =================================================================== */}
      {/* Cycle 2 - Shot 4: Bedroom Wakeup */}
      {frame >= 52 && frame <= 76 && (
        <AbsoluteFill style={{ opacity: c2BedOpacity }}>
          <ThreeStage shots={[c2Bedroom]} />
        </AbsoluteFill>
      )}

      {/* Cycle 2 - Shot 5: Morning Park Run */}
      {frame >= 69 && frame <= 94 && (
        <AbsoluteFill style={{ opacity: c2ParkOpacity }}>
          <ThreeStage shots={[c2Park]} />
        </AbsoluteFill>
      )}

      {/* Cycle 2 - Shot 6: Executive Office Desk */}
      {frame >= 87 && (
        <AbsoluteFill style={{ opacity: c2OfficeOpacity }}>
          <ThreeStage shots={[c2Office]} />
        </AbsoluteFill>
      )}

      {/* Seamless Fast-Forward Light Bridge Wash (Zero harsh cuts!) */}
      {totalLightWash > 0.01 && (
        <AbsoluteFill
          style={{
            backgroundColor: frame >= 52 && frame <= 60 ? "#FFF8E7" : "#FFEFC7",
            opacity: totalLightWash,
            mixBlendMode: "screen",
            pointerEvents: "none",
          }}
        />
      )}

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
          border: isDay3
            ? "1px solid rgba(255, 215, 0, 0.50)"
            : "1px solid rgba(0, 240, 255, 0.35)",
          backdropFilter: "blur(6px)",
          boxShadow: isDay3
            ? "0 4px 16px rgba(255, 215, 0, 0.25)"
            : "0 4px 16px rgba(0, 0, 0, 0.55)",
          opacity: dayBadgeFlip,
          pointerEvents: "none",
          zIndex: 15,
        }}
      >
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            backgroundColor: isDay3 ? "#FFD700" : "#00F0FF",
            boxShadow: isDay3 ? "0 0 10px #FFD700" : "0 0 8px #00F0FF",
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
          {isDay3 ? "DAY - 3" : "DAY - 2"}
        </span>
      </div>

      {/* Top-Right Fast Forward HUD Badge */}
      <div
        style={{
          position: "absolute",
          top: 32,
          right: 42,
          display: "flex",
          alignItems: "center",
          gap: 8,
          backgroundColor: "rgba(10, 14, 23, 0.75)",
          padding: "6px 14px",
          borderRadius: 6,
          border: "1px solid rgba(255, 255, 255, 0.15)",
          backdropFilter: "blur(6px)",
          pointerEvents: "none",
          zIndex: 15,
        }}
      >
        <span
          style={{
            fontFamily: "'Arial Black', Impact, sans-serif",
            fontSize: 13,
            fontWeight: 900,
            color: "#00F0FF",
            letterSpacing: "0.12em",
            opacity: ffPulse,
          }}
        >
          ▶▶ FAST FORWARD
        </span>
      </div>

      {/* Synchronized Caption (Gold highlight on key phrase) */}
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
            "And for <span style={{ color: "#FFD700" }}>two days</span>, you actually do it."
          </span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
