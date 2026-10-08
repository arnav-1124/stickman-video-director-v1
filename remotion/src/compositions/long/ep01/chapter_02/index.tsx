import React, { useState } from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { KenBurnsSlide } from "../../../../components/KenBurnsSlide";
import { SubtitleOverlay } from "../../../../components/SubtitleOverlay";
import { BrandingWatermark } from "../../../../components/BrandingWatermark";
import { ShotHUD } from "../../../../components/ShotHUD";
import { SHOTS } from "./shots";
import { SUBTITLES } from "./subtitles";
import { Shot } from "../../../../types/shot";
import type { Chapter02Props } from "../../../../Root";

export const Chapter02Composition: React.FC<Chapter02Props> = ({
  zoomStart,
  zoomEnd,
  panCenterX,
  panCenterY,
  showOnScreenHUD = true,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentSec = frame / fps;

  // Persistent live shot overrides from localStorage
  const [shotOverrides, setShotOverrides] = useState<Record<number, Partial<Shot>>>(() => {
    try {
      if (typeof window !== "undefined") {
        const saved = window.localStorage?.getItem("ch02_shot_overrides");
        if (saved) return JSON.parse(saved);
      }
    } catch (e) {}
    return {};
  });

  const handleUpdateShot = (updated: Shot) => {
    setShotOverrides((prev) => {
      const next = { ...prev, [updated.id]: updated };
      try {
        window.localStorage?.setItem("ch02_shot_overrides", JSON.stringify(next));
      } catch (e) {}
      return next;
    });
  };

  const handleResetShot = (shotId: number) => {
    setShotOverrides((prev) => {
      const next = { ...prev };
      delete next[shotId];
      try {
        window.localStorage?.setItem("ch02_shot_overrides", JSON.stringify(next));
      } catch (e) {}
      return next;
    });
  };

  const handleExportAll = () => {
    const fullShots = SHOTS.map((s) => ({ ...s, ...(shotOverrides[s.id] || {}) }));
    let tsCode = `export interface Shot {
  id: number;
  image: string;
  start: number;
  end: number;
  zoomStart: number;
  zoomEnd: number;
  cx1: number;
  cy1: number;
  cx2: number;
  cy2: number;
  title: string;
}

export const SHOTS: Shot[] = [\n`;
    for (const s of fullShots) {
      tsCode += `  { id: ${s.id}, image: "${s.image}", start: ${s.start.toFixed(2)}, end: ${s.end.toFixed(2)}, zoomStart: ${s.zoomStart.toFixed(2)}, zoomEnd: ${s.zoomEnd.toFixed(2)}, cx1: ${s.cx1.toFixed(2)}, cy1: ${s.cy1.toFixed(2)}, cx2: ${s.cx2.toFixed(2)}, cy2: ${s.cy2.toFixed(2)}, title: "${s.title}" },\n`;
    }
    tsCode += `];\n`;
    navigator.clipboard?.writeText(tsCode);
    alert("Copied complete updated shots.ts to clipboard! You can paste it directly into shots.ts.");
  };

  // 1. Locate active shot from timeline
  let activeShot: Shot = SHOTS[0];
  for (let i = 0; i < SHOTS.length; i++) {
    if (currentSec >= SHOTS[i].start && currentSec < SHOTS[i].end) {
      activeShot = SHOTS[i];
      break;
    }
  }
  if (currentSec >= SHOTS[SHOTS.length - 1].end) {
    activeShot = SHOTS[SHOTS.length - 1];
  }

  // 2. Apply live in-memory override if user adjusted sliders
  const effectiveShot: Shot = { ...activeShot, ...(shotOverrides[activeShot.id] || {}) };

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000", overflow: "hidden" }}>
      {/* 1. Master Audio Track (Voiceover + Ducked BGM) */}
      <Audio src={staticFile("audio/audio.mp3")} />

      {/* 2. Visual Ken Burns Slide with Zero-Black-Border Math */}
      <KenBurnsSlide shot={effectiveShot} currentSec={currentSec} />

      {/* 3. Channel Branding Watermark */}
      <BrandingWatermark />

      {/* 4. Interactive Live Camera Studio Controller HUD */}
      {showOnScreenHUD && (
        <ShotHUD
          shot={effectiveShot}
          currentSec={currentSec}
          onUpdateShot={handleUpdateShot}
          onResetShot={handleResetShot}
          onExportAll={handleExportAll}
          hasOverrides={Boolean(shotOverrides[effectiveShot.id])}
        />
      )}

      {/* 5. Fast-Paced Kinetic Subtitles (2-4 words per beat) */}
      <SubtitleOverlay subtitles={SUBTITLES} currentSec={currentSec} />
    </AbsoluteFill>
  );
};
