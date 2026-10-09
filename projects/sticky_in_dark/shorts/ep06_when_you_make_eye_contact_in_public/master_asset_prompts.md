# Master Asset Reference Prompts: Episode 06
## Title: When You Make Eye Contact In Public
## Model: Nano Banana Pro (Gemini 3 Pro Image)
### Style: 2D Minimalist Comic Art / The Ink Explainer Aesthetic

> **INSTRUCTION:** Generate and save these 4 Master Asset images FIRST. You will attach them as `@Image1`, `@Image2`, etc., to lock 100% character and environmental consistency across all scene slides.

---

## 🎨 Master Character DNA Sheets (Clean Studio Isolation)
> **DIMENSIONS FOR CHARACTERS:** **`1:1` (Square)**
> *Keeps the character centered, bold, and perfectly framed as an image reference.*

### Master Asset 1: The Protagonist / The Calm Guy (`@Character_Protagonist`)
* **Aspect Ratio:** `1:1` (Square)
* **Prompt Box:**
```text
A clean full-body solo character illustration in 2D minimalist comic art style, centered on a plain solid off-white background (#FAF9F6). A single stickman figure standing alone. Smooth circular solid white head with bold, crisp solid black vector ink outlines (6px-8px stroke weight). Messy textured dark-brown fringe hair resting over his forehead. Wearing a comfortable dark forest-green cotton hoodie, simple black stick-line legs, and clean white doodle sneakers. Standing in a relaxed, grounded posture with hands loosely resting in front. Simple dark dot eyes with calm, relaxed horizontal eyebrows, serene unbothered expression. Flat 2D vector graphic novel illustration, high contrast, clean line art, zero 3D depth, zero gradients. Solo character only, perfectly isolated, zero text, no words, no letters, no labels, no color palette swatches, no turnaround views, no UI elements. 1:1 square aspect ratio, centered framing.
```

### Master Asset 2: The Approaching Stranger / Peer (`@Character_Stranger`)
* **Aspect Ratio:** `1:1` (Square)
* **Prompt Box:**
```text
A clean full-body solo character illustration in 2D minimalist comic art style, centered on a plain solid off-white background (#FAF9F6). A single stickman figure standing alone in walking posture. Smooth circular solid white head with bold, crisp solid black vector ink outline (6px-8px stroke weight). Short neat black parted hair. Wearing a casual dark navy crewneck sweater, simple black stick legs, and grey sneakers. Casual everyday neutral expression with simple dot eyes and flat mouth line. Flat 2D vector graphic novel illustration, high contrast, clean line art, zero 3D depth, zero gradients. Solo character only, perfectly isolated, zero text, no words, no letters, no labels, no color palette swatches, no turnaround views, no UI elements. 1:1 square aspect ratio, centered framing.
```

### Master Asset 3: The Black Smartphone Prop (`@Prop_Smartphone`)
* **Aspect Ratio:** `1:1` (Square)
* **Prompt Box:**
```text
A clean minimalist 2D prop illustration in the vector comic art style of Ink Explainer, centered on a plain solid off-white background (#FAF9F6). A cartoon stickman mitten hand holding a modern black rectangular smartphone. Bold crisp black vector outlines (6px-8px stroke weight). The phone has rounded corners and a sleek solid pitch-black screen. Flat 2D vector illustration, zero gradients, zero shadows, zero 3D depth. Perfectly isolated prop study, zero text, no labels, no reflections, 1:1 square aspect ratio, centered framing.
```

---

## 🏛️ Master Environment & Scene Anchors (9:16 Vertical / 1080x1920)
> **DIMENSIONS FOR ENVIRONMENTS & SCENES:** **`9:16` (Vertical, 1080x1920)**
> *Minimal 2D hand-drawn cartoon doodle background designed to match the stick figure line art 100%—zero 3D, zero photorealism.*

### Master Asset 3: Empty Campus Street / Courtyard (`@Environment_Campus_Street`)
* **Aspect Ratio:** `9:16` (Vertical / 1080x1920)
* **Prompt Box:**
```text
A minimal 2D hand-drawn webcomic cartoon background of an open university campus paved outdoor walkway ground, in the simple vector doodle art style of Ink Explainer. Drawn on a clean solid off-white paper canvas (#FAF9F6). Bold black ink pen outlines (5px-7px stroke weight). In the background, simple architectural outline of a classic university hall with an arched entrance and minimalist windows. On the sides, simple outline silhouettes of a couple of park trees. The ground is an open flat paved campus street with subtle faint stone tile lines extending into the distance. Flat solid color blocking: soft stone grey ground, subtle muted slate accents, off-white cream sky (#FAF9F6). Minimalist cartoon doodle illustration, flat 2D perspective, zero gradients, zero shadows, zero 3D depth, zero photorealism. Clean empty background plate, zero people, zero characters, zero text, zero UI, 9:16 vertical aspect ratio.
```

---

### Master Asset 4: Master 2-Shot Approach Scene Anchor (`@Scene_Campus_Approach_Anchor`)
> **CRITICAL MASTER SCENE ANCHOR (Like Slide 02 in Ep 05):**
> *Attach `@Image1`: `master_assets/Character_Protagonist.jpg` and `@Image2`: `master_assets/Character_Stranger.jpg` to generate this master two-shot anchor! Once generated, save as `master_assets/Scene_Campus_Approach_Anchor.jpg` and `slides/slide_01.jpg`.*

* **Aspect Ratio:** `9:16` (Vertical / 1080x1920)
* **Input / Ingredients to attach:** 
  - `@Image1`: `master_assets/Character_Protagonist.jpg`
  - `@Image2`: `master_assets/Character_Stranger.jpg`
* **Prompt Box:**
```text
A minimal 2D hand-drawn animation still in the exact simple vector pen-and-ink cartoon style of Ink Explainer, drawn on an off-white paper canvas (#FAF9F6). Bold black ink pen outlines (5px-8px stroke weight), flat solid color blocking, zero gradients, zero 3D rendering, zero photorealism. Clean graphic novel doodle illustration. Vertical 9:16 aspect ratio (1080x1920).

Using references @Image1 and @Image2:
Wide shot across an open university campus courtyard ground on off-white textured paper (#FAF9F6):
Two stickmen figures are walking in opposite directions directly toward each other across the open paved ground, separated by a 20-meter gap.
On the left: The protagonist from @Image1 wearing his dark forest-green cotton hoodie, messy brown fringe hair, black stick legs, and white doodle sneakers, walking forward.
On the right: The oncoming stranger from @Image2 wearing his dark navy-blue crewneck sweater, neat parted black hair, and grey sneakers, walking toward the left.
Across the open ground between their eyes, a bright red dashed laser line (#E63946) connects their gazes with small hand-drawn red tension sparks in the center.
In the background: Minimalist black ink outline of a classic university hall with arched doorway and two clean tree silhouettes. Flat solid color blocking, zero shadows, zero 3D depth, clean vector ink lines, off-white background.

STRICT NEGATIVE: Single full-screen frame only. NO outer box borders, NO split comic frames, NO speech bubbles, NO photorealism, NO 3D rendering, 9:16 vertical.
```

