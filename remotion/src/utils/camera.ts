import { interpolate } from "remotion";
import { Shot, CameraTransform } from "../types/shot";

/**
 * Calculates a mathematically safe Ken Burns camera transform.
 *
 * Black Border Prevention Rule:
 * For an element filling 100% of the canvas with scale S >= 1.0,
 * the maximum allowed focal shift from center (0.50) without revealing
 * the canvas background is:
 *   maxDelta = (S - 1) / (2 * S)
 *
 * Clamping (cx, cy) to [0.5 - maxDelta, 0.5 + maxDelta] guarantees
 * 100% full-frame coverage at all times with zero black voids.
 */
export function calculateSafeKenBurns(
  shot: Shot,
  currentSec: number
): CameraTransform {
  const shotDur = Math.max(0.05, shot.end - shot.start);
  const prog = Math.min(1, Math.max(0, (currentSec - shot.start) / shotDur));

  // Smooth cosine ease-in-out curve
  const ease = 0.5 * (1 - Math.cos(prog * Math.PI));

  // Raw interpolated parameters
  const rawZoom = interpolate(ease, [0, 1], [shot.zoomStart, shot.zoomEnd]);
  const rawCx = interpolate(ease, [0, 1], [shot.cx1, shot.cx2]);
  const rawCy = interpolate(ease, [0, 1], [shot.cy1, shot.cy2]);

  // Ensure zoom is at least 1.0 (covers 100% of viewport)
  const zoom = Math.max(1.0, rawZoom);

  // Safe bounding box clamping
  const maxDeltaX = Math.max(0, (zoom - 1) / (2 * zoom));
  const maxDeltaY = Math.max(0, (zoom - 1) / (2 * zoom));

  const safeCx = Math.min(0.5 + maxDeltaX, Math.max(0.5 - maxDeltaX, rawCx));
  const safeCy = Math.min(0.5 + maxDeltaY, Math.max(0.5 - maxDeltaY, rawCy));

  return {
    zoom,
    safeCx,
    safeCy,
    transformOrigin: `${safeCx * 100}% ${safeCy * 100}%`,
    transform: `scale(${zoom})`,
    progress: prog,
  };
}
