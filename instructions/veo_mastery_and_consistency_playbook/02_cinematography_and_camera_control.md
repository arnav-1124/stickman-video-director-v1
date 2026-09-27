# Chapter 02: Cinematography & Camera Control

> "The camera is the audience's eye. Direct it with precision, or the AI will guess randomly."

Veo 3.1 features native understanding of Hollywood camera gear, lenses, and grip equipment. Using exact cinematographic terms controls the camera trajectory reliably and prevents jarring AI drift.

---

## 1. Focal Length & Lens Vocabulary

Specifying lens optics alters how space, depth, and character proportions are rendered:

| Lens Specifier | Visual Impact | Best Used For |
| :--- | :--- | :--- |
| **24mm Wide-Angle** | Expansive field of view, exaggerated perspective, high environmental scale. | Establishing shots, expansive playgrounds, towering creatures, dynamic physical comedy. |
| **35mm Standard Wide** | Crisp, cinematic documentary feel. Captures character from waist up with clear surrounding context. | Multi-character dialogue, investigative detective tracking, character interactions. |
| **50mm "Nifty Fifty"** | Natural human eye perspective, zero optical distortion, grounded realism. | Neutral medium shots, conversational character exchanges. |
| **85mm / 100mm Telephoto** | Shallow depth of field, background compression, subject isolation with rich creamy bokeh. | Emotional close-ups, sad/longing facial micro-expressions, dramatic realization beats. |

---

## 2. Professional Camera Trajectories

Stick to **one clear, purposeful camera move per shot**. Combining multiple complex movements (e.g., pan + zoom + roll) causes spatial warping in diffusion models.

### A. The Push-In / Dolly-In
* **Prompt Syntax:** `Slow, intimate push-in camera trajectory...` or `Cinematic dolly-in moving smoothly from medium shot to close-up...`
* **Emotional Effect:** Intensifies focus, conveys sudden realization, emotional gravity, or intimacy (e.g., Barnaby sighing outside his cave).

### B. The Pull-Back / Reveal
* **Prompt Syntax:** `Camera slowly dollies back and elevates upward, expanding the frame...`
* **Emotional Effect:** Reveals isolation (showing a lonely character small against a vast landscape) or triumphant context (revealing the restored playground full of kids).

### C. The Lateral Tracking / Parallax Follow
* **Prompt Syntax:** `Smooth lateral tracking shot moving parallel to the character's movement with strong foreground tree parallax...`
* **Emotional Effect:** High sense of journey, progression, and momentum (e.g., trio creeping through the forest ridge).

### D. The Orbit / 360 Arc
* **Prompt Syntax:** `Subtle 45-degree orbital arc shot sweeping clockwise around the frozen characters...`
* **Emotional Effect:** Emphasizes 3D volume and spatial relationships without requiring character locomotion.

### E. The Crane / Jib Lift
* **Prompt Syntax:** `Smooth crane elevation lifting upward from waist level to a high-angle celebratory vista...`
* **Emotional Effect:** Grand finales, triumphant conclusions, awe-inspiring scale.

---

## 3. The Secret Weapon: Depth-of-Field Stabilization

### The Problem: Background Morphing
In AI video generation, the background often shimmers, morphs, or spawns glitchy textures as the camera moves. This occurs because the neural network is forced to hallucinate millions of detailed background pixels (tree leaves, distant windows, brick patterns) simultaneously with foreground character physics.

### The Solution: Shallow Focus
Always specify:
```text
Shallow depth of field, sharp focus on [Subject], softly blurred background bokeh.
```
* **Why it works:** By commanding the model to blur background elements into smooth bokeh, the diffusion model dedicates 90%+ of its computational attention to the character's face, hands, and bodily physics.
* **Result:** Pristine character animation, zero background morphing, and an instantly high-end, cinematic studio aesthetic.
