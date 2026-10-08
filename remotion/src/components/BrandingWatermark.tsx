import React from "react";
import { Img, staticFile } from "remotion";

interface BrandingWatermarkProps {
  logoPath?: string;
  top?: number;
  right?: number;
  height?: number;
  opacity?: number;
}

export const BrandingWatermark: React.FC<BrandingWatermarkProps> = ({
  logoPath = "branding/logo.png",
  top = 36,
  right = 48,
  height = 56,
  opacity = 0.85,
}) => {
  return (
    <div
      style={{
        position: "absolute",
        top,
        right,
        opacity,
        filter: "drop-shadow(0 2px 8px rgba(0,0,0,0.8))",
        pointerEvents: "none",
        zIndex: 5,
      }}
    >
      <Img src={staticFile(logoPath)} style={{ height }} />
    </div>
  );
};
