import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Shot } from "../types/shot";
import { calculateSafeKenBurns } from "../utils/camera";

interface KenBurnsSlideProps {
  shot: Shot;
  currentSec: number;
}

export const KenBurnsSlide: React.FC<KenBurnsSlideProps> = ({ shot, currentSec }) => {
  const { zoom, transformOrigin, transform } = calculateSafeKenBurns(shot, currentSec);

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
      }}
    >
      <Img
        src={staticFile(shot.image)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transformOrigin,
          transform
        }}
      />
      {/* Studio Vignette Overlay */}
      <AbsoluteFill
        style={{
          boxShadow: "inset 0 0 100px rgba(0, 0, 0, 0.65)",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
