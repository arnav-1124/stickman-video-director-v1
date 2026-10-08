import React from "react";
import { Subtitle } from "../types/subtitle";

interface SubtitleOverlayProps {
  subtitles: Subtitle[];
  currentSec: number;
  fontSize?: number;
  bottomOffset?: number;
}

export const SubtitleOverlay: React.FC<SubtitleOverlayProps> = ({
  subtitles,
  currentSec,
  fontSize = 48,
  bottomOffset = 84,
}) => {
  const activeSub = subtitles.find(
    (sub) => currentSec >= sub.start && currentSec < sub.end
  );

  if (!activeSub) return null;

  return (
    <div
      style={{
        position: "absolute",
        bottom: bottomOffset,
        left: 0,
        right: 0,
        textAlign: "center",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        pointerEvents: "none",
        zIndex: 10,
      }}
    >
      <div
        style={{
          backgroundColor: "rgba(5, 7, 12, 0.82)",
          padding: "10px 24px",
          borderRadius: 10,
          border: "1px solid rgba(255, 255, 255, 0.15)",
          boxShadow: "0 8px 30px rgba(0, 0, 0, 0.8)",
          backdropFilter: "blur(6px)",
          maxWidth: "85%",
        }}
      >
        <span
          style={{
            fontFamily: "'Arial Black', 'Impact', sans-serif",
            fontSize,
            color: "#ffffff",
            letterSpacing: "0.04em",
            textTransform: "uppercase",
            textShadow:
              "0 2px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000, 0 4px 12px rgba(0,0,0,0.9)",
          }}
        >
          {activeSub.text}
        </span>
      </div>
    </div>
  );
};
