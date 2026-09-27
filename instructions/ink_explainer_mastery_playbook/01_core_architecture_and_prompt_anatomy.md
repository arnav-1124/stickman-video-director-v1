# 01: Core Architecture & Prompt Anatomy

## 1. Visual DNA of "The Paint Explainer" & "Ink Explainer"
Viral psychology channels (like *The Paint Explainer*, *Ink Explainer*, and *Casually Explained*) achieve millions of views not through hyper-realistic 3D rendering or complex manual keyframing, but through **clarity, contrast, and visual metaphor**.

### The 4 Visual Pillars:
1. **Canvas**: Clean off-white textured paper (`#FAF9F6` or `#F4F3EE`). Never pure `#000000` or plain blinding `#FFFFFF`.
2. **Character**: A 2D doodle stickman with:
   - A smooth, clean circular white head (like a ping-pong ball with black ink contour).
   - Minimalist solid black ink lines for torso, arms, and legs (uniform 6px-8px stroke weight).
   - Simple facial dots for eyes or expressive eyebrow angles.
3. **Props & Metaphors**: Hand-drawn black ink doodle objects (e.g., balance scales, brain gears, floating hearts, chains, crowns, pedestals).
4. **Selective 1-Color Accent Rule**:
   - 95% of the frame is monochrome (black ink on off-white paper).
   - Only **ONE** accent color per scene (e.g., Crimson Red `#FF2A4D` for danger/ego, or Electric Cyan `#00F0FF` for insight/clarity).

---

## 2. The Universal Prompt Anatomy

Every prompt submitted to AI video generators (Hailuo MiniMax, Kling, Flow/Veo, Luma) follows this 5-part structure:

```
[Style Anchor] + [Subject & Appearance] + [Action & Visual Metaphor] + [Environment/Canvas] + [Camera & Motion]
```

### Breakdown of the 5 Components:
1. **Style Anchor**:
   `"Minimalist 2D ink explainer animation, hand-drawn vector doodle aesthetic, crisp black line art on off-white textured paper background."`
2. **Subject & Appearance**:
   `"An expressive minimalist stick figure with a smooth white circular head and bold solid black ink strokes."`
3. **Action & Visual Metaphor**:
   `"The stickman points to an intricate black ink brain diagram floating next to him. Small gear wheels turn inside the brain."`
4. **Environment/Canvas**:
   `"Clean off-white cream paper texture, high contrast monochrome with a single subtle red ink accent."`
5. **Camera & Motion**:
   `"Static eye-level camera with a snappy 1.1x punch-in zoom on the central concept. Fluid 2D line animation, no 3D morphing, no photorealism."`

---

## 3. Negative Prompt Vault (Crucial for Cloud AI Engines)
Always include or enforce these negative prompt terms in engines that support them:

```
photorealistic, 3d render, cgi, claymation, realistic human skin, human face, realistic anatomy, colorful gradients, messy textures, blurry, artifacting, text watermarks, 3d lighting, glossy reflections
```
