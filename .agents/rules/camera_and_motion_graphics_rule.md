# 2D Affine Camera & Motion Graphics Production Standard

> **IMMUTABLE CAMERA DIRECTIVE FOR ALL SHORTS & LONG-FORM EPISODES**  
> Every video rendered via Remotion or FFmpeg must adhere to this camera standard.  
> It guarantees broadcast-grade motion graphics fluidity while preserving 100% on-screen visibility of all illustrations, titles, and props.

---

## 1. The 2D Affine Camera Matrix Rig

To lock any focal point $(X, Y)$ on an illustration dead-center on screen without distortion, apply the exact affine camera matrix transformation:

```typescript
/**
 * Professional 2D Motion Graphics Affine Camera Rig
 * 
 * Maps canvas target coordinate (camX, camY) to dead-center (540, 960) on 9:16 mobile canvas.
 * For 16:9 widescreen, map (camX, camY) to (960, 540).
 */
function getCameraMatrix(camX: number, camY: number, zoom: number) {
  return `translate(540px, 960px) scale(${zoom}) translate(${-camX}px, ${-camY}px)`;
}
```

- **CSS Styling Mandate:** Always set `transformOrigin: "0px 0px"` on the `<AbsoluteFill>` wrapper.

---

## 2. The Full-Frame Visibility Mandate (Anti-Cropping Law)

1. **Conservative Zoom Range (`1.00× – 1.08×`):**
   - **Never exceed `1.08×`** (hard maximum `1.10×` only on extreme single-subject reaction close-ups).
   - High zooms (`1.30× – 1.85×`) are strictly prohibited because they crop out up to 50% of the artwork and hide critical elements (e.g. title banners, split-screen comparisons, dual characters, props, and background context).
2. **Subtle Organic Pan Drifts ($\pm 20\text{px} – 50\text{px}$):**
   - Panning must be a delicate, organic drift that guides the viewer's eye across the scene without pushing the edges of the drawing off-canvas.
3. **Split-Screen & Multi-Element Protection:**
   - On split-screen slides (e.g. comparison beats), zoom must stay strictly between `1.00× – 1.03×` centered at `(540, 960)` so both sides of the contrast are 100% visible side-by-side.

---

## 3. Motion Curves & Stabilization

1. **Cubic-Bezier Broadcast Easing:**
   - Use high-end easing curves such as `Easing.bezier(0.16, 1.0, 0.3, 1.0)` or `Easing.inOut(Easing.cubic)`.
2. **Zero Screen Jitter / No Vibration:**
   - Formulaic shakes (`Math.sin(frame * freq) * amp`) and pixel noise vibrations are strictly banned. The camera must glide with documentary smoothness.
3. **Seamless 4-to-6 Frame Crossfade:**
   - Overlap adjacent slides by 4 to 6 frames using `interpolate(frame, [start, start + 4], [0, 1])` to guarantee buttery crossfades with zero black flashes or hard cuts.

---

## 4. Subtitle & Acoustic Synchronization

1. **Acoustic Waveform Snapping:**
   - Never use arbitrary duration division across entire scripts. Subtitle clauses must snap to the actual acoustic speech onsets and silence breaks detected in the voiceover waveform.
2. **Canary Yellow Active Word Pop:**
   - Active word: `{\c&H0000D7FF&\3c&H000A0D14&\t(0,60,\fscx112\fscy112)\t(60,120,\fscx100\fscy100)}`
   - Inactive words: `{\c&H00FFFFFF&\3c&H000A0D14&}`
   - Safe vertical margin: `MarginV=400` on 9:16 vertical canvas (to stay clear of YouTube Shorts bottom UI controls).
