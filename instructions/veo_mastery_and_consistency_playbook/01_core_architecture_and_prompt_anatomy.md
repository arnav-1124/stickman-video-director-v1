# Chapter 01: Core Architecture & Prompt Anatomy

> "Treat your prompt as a directorial script, not a search query."

Veo 3.1 is trained on extensive professional cinematic and television footage. Consequently, it understands and responds best to **filmmaking terminology** (lens types, camera moves, lighting ratios, sound engineering) rather than vague adjectives like "hyperrealistic" or "epic 8k".

---

## 1. The 7-Layer Directorial Formula

Every high-performing prompt for Veo 3.1 should be assembled using this systematic 7-layer hierarchy:

```text
[1. CAMERA & LENS] + [2. SUBJECT SPECIFICATION] + [3. CHOREOGRAPHED ACTION] + 
[4. ENVIRONMENT & DEPTH] + [5. LIGHTING & COLOR] + [6. TEXTURE & RENDERING STYLE] + 
[7. NATIVE AUDIO CUES]
```

### Breakdown of the 7 Layers:
1. **Camera & Lens:** The optical perspective (e.g., `Cinematic low-angle medium shot on a 35mm prime lens`).
2. **Subject Specification:** Concrete character or object description with locked physical anchors (e.g., `5-year-old boy Tommy with messy blonde hair and bright blue dinosaur t-shirt`).
3. **Choreographed Action:** Explicit, physical micro-actions broken down second-by-second (never vague adjectives).
4. **Environment & Depth:** Foreground, midground, background elements, weather, spatial scale.
5. **Lighting & Color:** Key light source, rim lighting, color temperature (e.g., `Warm golden hour sunbeams filtering through pine trees, soft natural rim light`).
6. **Texture & Rendering Style:** Concrete aesthetic genre (e.g., `3D Pixar style animated render, soft matte fabric textures, tactile fur physics`).
7. **Native Audio Cues:** Specific dialogue lines with timestamps, Foley sound effects, and ambient room tone.

---

## 2. The Front-Loading Principle (Token Weighting)

In transformer-diffusion models like Veo 3.1:
* **The first 25–40 tokens carry the highest positional attention.**
* If you place the camera move and main subject at the *end* of a 150-word prompt, the model may drift, hallucinate unwanted elements, or default to a static wide shot.
* **Always front-load:** Start immediately with the camera framing, lens, and primary subject action before detailing the background grass or cloud shapes.

### ❌ Ineffective (Back-Loaded):
> *"In a beautiful green forest where there are pine trees and nice flowers and sun shining down with cute grass, a small robot hovers forward on a 35mm lens."*

### ✅ Effective (Front-Loaded):
> *"Eye-level tracking shot on a 35mm lens: the small spherical white robot Bip hovers forward across vibrant green turf, his cyan visor pulsing. Surrounding background: dense sun-dappled pine forest with wildflowers."*

---

## 3. Simple Verbs vs. Stacked Verbs

Diffusion models generate video frame-by-frame across latent space. When a prompt contains **stacked contradictory verbs** (e.g., *"he runs, then falls, then gets up, laughs, and kicks a ball"*), the model attempts to interpolate all actions simultaneously, leading to distorted limbs, sudden cuts, or morphing.

### Rule of Action:
* **One Primary Macro-Action per 4–8 seconds.**
* Support that macro-action with **sequential micro-actions** (see Chapter 05: Narrow Intervals).
* Use concrete physical verbs:
  * Instead of: *"walking sadly"*
  * Use: *"shuffling forward with hunched shoulders, dragging boots across turf"*

---

## 4. Avoiding Mutually Exclusive Contradictions

A major cause of muddy, artifact-heavy generations is accidental prompt contradiction:
* **Lighting Conflict:** Asking for `"moody dark cinematic film noir shadows"` AND `"bright, cheerful, vibrant saturated colors"`.
* **Motion Conflict:** Asking for a `"rapid high-speed whip pan"` AND `"slow intimate character close-up"`.
* **Style Conflict:** Asking for `"photorealistic documentary"` AND `"stylized 3D Pixar character cartoon"`.

Select **one cohesive visual tone** per shot and enforce it across all layers.
