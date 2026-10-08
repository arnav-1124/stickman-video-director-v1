# Ink Explainer Production Constitution (Permanent Master Standard)

> **IMMUTABLE LAW FOR ALL EPISODES**  
> Every video produced in this studio must be an exact, uncompromising replica of the visual, narrative, and acoustic quality of the **Ink Explainer** YouTube channel.  
> This document is permanent and must be strictly adhered to across all scripts, storyboards, prompt generations, and video assembly.

---

## 1. The 2.0–3.0s Hard Cut Cadence Law (Anti-PPT Rule)
1. **The Pacing Mandate:** No single slide or visual illustration may remain static on screen for longer than **3.0 seconds**. The target average duration per visual cut across the entire video is **2.0s to 2.5s**.
2. **Motion Through Cutting:** The video is built from illustrated frames, but it must **never feel like a static PowerPoint presentation**. 
   - Rapid sequential framing: Wide establishing shot (2.0s) -> Medium action shot (2.0s) -> Tight reaction shot (1.8s) -> Macro prop shot (2.2s).
   - Sequential poses: Break character actions into 2–3 progressive frames (e.g., raising arm -> holding spear aloft -> pointing forward).
   - Micro camera dynamics: Snappy 1.05x–1.12x punch-ins, Ken Burns subtle drifts, or horizontal pan shifts between cuts.
3. **2-Minute Target Benchmark:** A 120-second (2-minute) episode must feature between **45 and 55 unique visual beats/slides**.

---

## 2. The Mini-World Asset Kit Law (100% Visual Consistency)
Before generating any final slide prompts, every episode must first generate and lock its **Mini-World Asset Library**:
1. **Character Anchor Sheets (`assets/characters/`):**
   - Head: Pure white circular pill/sphere (`#FFFFFF`) with uniform 6px black ink contour.
   - Face: Black dot eyes, bold angled eyebrows (carrying all emotion), clean mouth line.
   - Body & Wardrobe: Stickman limbs with styled flat-color garments (e.g. fur tunic, Greek toga, modern hoodie) and distinctive hairstyle (e.g. spiky brown caveman hair).
   - Poses: Front view, 3/4 view, side profile, and emotional variations (neutral, smirk, scheming, panic, shock, triumph).
2. **Environment Master Backdrops (`assets/environments/`):**
   - Clean, full-color illustrated 2D cartoon environments with **zero characters** present (empty plates).
   - Warm, cel-shaded color palettes (e.g. Golden Savanna `#D2A65D` with cyan sky `#5CB8E6`; Night Cave `#213045` with warm orange firelight `#D97724`).
   - Clean black outlines for all rocks, clouds, tools, trees, and architecture.
3. **Prop & Metaphor Anchors (`assets/props/`):**
   - Isolated doodle items (spears, flutes, coins, stone tablets, cell phones) drawn in the same clean black line art and flat color fills.

---

## 3. Google Flow Prompt Engineering Architecture
All prompts for Google Flow / Gemini Imagen 3 must strictly follow this exact 5-part anatomical syntax so that **every generated slide succeeds on the first try without iteration**:

```text
[Style Anchor] + [Asset References: @Character + @Environment] + [Subject Action & Emotional Pose] + [Framing & Camera Perspective] + [Lighting & Negative Guardrails]
```

### Prompt Formula Template:
- **Style Anchor:** `"Minimalist 2D hand-drawn cartoon comic style in the signature Ink Explainer aesthetic, clean uniform black ink line art (6px stroke weight), flat vibrant cel-shaded color fills, soft ground contact shadow, clean digital illustration, no 3D rendering, no paper textures."`
- **Asset References:** `"Referencing @Character for exact face, spiky brown hair, and fur tunic; referencing @Environment for the savanna landscape backdrop."`
- **Action & Pose:** `"[Character Name] is [specific action, e.g. crouching on one knee holding a wooden flint spear, eyes narrowed with a scheming half-smile directed off-camera]."`
- **Framing:** `"[Shot Type: e.g. Cinematic medium shot / Wide establishing shot / Tight close-up], eye-level angle, 16:9 widescreen composition with subject balanced in the left third."`
- **Strict Negative Guardrails (Enforced on Every Generation):**
  `"Avoid: photorealism, 3d render, cgi, gradients, bevels, drop shadows, grainy paper texture, watercolor wash, sketches, messy lines, realistic human face, realistic anatomy, text, watermark, logos, blurry details, distortion."`

---

## 4. Audio, Voiceover & Sound Design Standards
1. **Narration Voice:** Google Gemini Flash TTS (Character voice `"Ludo"`) or matched high-energy narrator. Tone: conversational, witty, suspenseful, curious, with natural conversational breathing and rhythmic pauses.
2. **Audio Ducking:** Background music (ambient lo-fi, curiosity acoustic) master-leveled to -18 LUFS under active speech, ducking down automatically by -4 dB when voice speaks.
3. **Foley & Sound Effects:** Every major visual cut or dramatic action must trigger a crisp, punchy cartoon SFX (whoosh, pop, thud, wooden clack, chime, flame sizzle) mastered between -12 dB and -16 dB.
4. **Subtitles:** SubStation Alpha (`.ass`) karaoke word-highlight subtitles (crisp white text, bold black outline, golden active word pop) placed in lower third with safe-zone clearance.

---

## 5. High-CTR Thumbnail Architecture (The 3-Element Law)
Every thumbnail must pass the **168px Mobile Feed Test** with a score ≥ 90/100:
1. **Element 1: Massive Expressive Face:** An extreme close-up or medium 2-shot of the stickman showing an intense, unmistakable human emotion (shock, conspiratorial smirk, existential dread).
2. **Element 2: One High-Contrast Prop:** A vibrant, story-carrying object (e.g. blazing torch, carved bone flute, glowing phone, bloody spear).
3. **Element 3: 2 to 3 Giant Words:** Hand-drawn marker lettering (`Permanent Marker` / `Bangers`) readable at tiny mobile thumbnail size in under 0.5s (e.g. `THE FIRST LIE`, `THEY KNEW`, `SECRET PLEASURE`).
4. **Clean Background:** 2D colored environment backdrop with edge margins (80px margin, bottom-right timecode box kept completely clear).

---

## 6. Production Roadmap & Monetization Velocity
1. **Direct Focus on Episode 2:** Episode 1 is archived. Episode 2 is the flagship launch designed for rapid viral reach.
2. **Video Length:** 2 minutes (120 seconds).
3. **Execution Plan:**
   - Phase 1: High-retention research thesis & script (120 seconds, ~280–310 words).
   - Phase 2: Mini-World Asset Kit generation in Google Flow (Character sheet + 3 environment backdrops).
   - Phase 3: Storyboard & 50-slide Google Flow prompt generation.
   - Phase 4: Gemini TTS voiceover & word-level timing alignment.
   - Phase 5: High-CTR Thumbnail packaging (3 variants).
   - Phase 6: Post-production assembly & final export.
