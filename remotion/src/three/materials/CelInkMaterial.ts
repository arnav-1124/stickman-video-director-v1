import * as THREE from "three";

export interface CelPalette {
  ink: number;
  paper: number;
  accentCyan: number;
  accentRed: number;
  warmDawn: number;
}

export const PALETTE: CelPalette = {
  ink: 0x0a0d14,
  paper: 0xfaf9f6,
  accentCyan: 0x00f0ff,
  accentRed: 0xff2a4d,
  warmDawn: 0xffa726,
};

/**
 * Creates a clean NPR (Non-Photorealistic) Ink & Paper material using Three.js Toon shading.
 */
export function createInkMaterial(color: number = PALETTE.ink): THREE.MeshToonMaterial {
  const format = THREE.RGBAFormat;
  const colors = new Uint8Array([
    10, 13, 20, 255,   // Shadow step
    80, 85, 95, 255,   // Midtone
    250, 249, 246, 255 // Highlight
  ]);
  const gradientMap = new THREE.DataTexture(colors, 3, 1, format);
  gradientMap.minFilter = THREE.NearestFilter;
  gradientMap.magFilter = THREE.NearestFilter;
  gradientMap.needsUpdate = true;

  return new THREE.MeshToonMaterial({
    color,
    gradientMap,
  });
}

/**
 * Creates an inverted-hull outline mesh for clean graphic hand-inked borders.
 */
export function createOutlineMesh(
  geometry: THREE.BufferGeometry,
  thickness: number = 0.04,
  outlineColor: number = PALETTE.ink
): THREE.Mesh {
  const outlineMaterial = new THREE.MeshBasicMaterial({
    color: outlineColor,
    side: THREE.BackSide,
  });

  const outlineMesh = new THREE.Mesh(geometry, outlineMaterial);
  outlineMesh.scale.multiplyScalar(1.0 + thickness);
  return outlineMesh;
}
