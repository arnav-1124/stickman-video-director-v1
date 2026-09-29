# Google Flow & Nano Banana Pro: Multi-Reference Master Guide

> **DOCUMENT STATUS:** PERMANENT STUDIO RECORD  
> **PURPOSE:** Retains all verified facts, limits, and workflows for generating consistent 2D comic assets in Google Flow using Nano Banana Pro (Gemini 3 Pro Image).  

---

## 1. Core Engine Limits & Capabilities

* **Engine:** Nano Banana Pro (Gemini 3 Pro Image) within Google Flow / VideoFX.
* **Maximum Reference Limit:** Supports **up to 14 reference images** per prompt for multi-image blending.
* **The Practical Sweet Spot (3 to 6 Images):**
  * Feeding more than 6 references causes **context dilution / feature bleeding** (the model mixes unintended background colors or body shapes together).
  * **Single-character scene:** Use **3 to 4 references** (`@Character_DNA` + `@Environment` + `@Style_Anchor`).
  * **Two-character interaction:** Use **4 to 6 references** (`@Character_A` + `@Character_B` + `@Environment` + `@Style_Anchor`).

---

## 2. The 5 Valid Reference Types

| Reference Type | Source Asset | What It Locks |
| :--- | :--- | :--- |
| **1. Character DNA** | Character on neutral, isolated white/grey background. | Head shape, hairstyle, clothing colorway, accessories (hoodie, glasses, backpack). |
| **2. Style Anchor** | Master 2D comic art sample frame. | Line weight (6px vector ink contour), flat color shading, no 3D photorealism. |
| **3. Environment Anchor** | Wide shot of the location (e.g. lecture hall, hallway). | Wall color, desk wood grain, chalkboard green, lighting perspective. |
| **4. Previous Shot Continuity (I2I)** | The immediately preceding shot (`shot_02` $\to$ `shot_03`). | Prevents room layout or camera angle from shifting between sequential cuts. |
| **5. Composition / Layout** | Rough doodle or framing layout. | Directs character placement (left, center, right, close-up vs wide). |

---

## 3. The 100% Consistency Protocol (Hybrid Studio Rule)

* **Generative Reality:** Pure AI generation across 25 independent text prompts will naturally drift (typically 92%–96% likeness).
* **The Studio Solution:**
  1. **Phase 1: Pre-Production Asset Anchors:** Generate and permanently lock:
     - 3 Master Character DNA Sheets.
     - 3 Master Environment Anchors.
  2. **Phase 2: Scene Generation in Flow:**
     - Always attach the Master Environment + Master Character DNA into Flow.
     - Use Flow's **conversational memory** to modify poses and expressions within the same scene session without redrawing the background.
  3. **Phase 3: Fast Micro-Cuts (0.7s–1.0s):**
     - For tight object shots (inserting key, closing laptop, text cards), use direct 2D graphic overlays on the clean canvas.
