# Channel Branding & Watermark Replacement Protocol

## 1. Official Channel Brand Identity

### 1.1 The Master Channel Asset
The channel's official visual signature is the **PhD Stickman Graduate**:
- **Description:** A stickman character wearing a black graduation cap with tassel, black academic gown with white collar accents, happily holding a black book titled `"A PhD"` with a credential seal, encased in a circular badge with a subtle gradient and dark perimeter rim.
- **Master File Path:** [`assets/branding/channel_logo.png`](file:///f:/Arnav%20-%20YT/stickman-video-director/assets/branding/channel_logo.png)
- **Format:** 160×160 RGBA PNG with 4x supersampled, anti-aliased circular alpha transparency.

---

## 2. AI Watermark Eradication Protocol

### 2.1 The Google Imagen / Gemini Watermark
Raw AI images generated via Google Imagen 3 / Gemini Image contain an automated, translucent 4-pointed sparkle star watermark in the bottom-right corner.
- **Default Slide Canvas:** `1536 × 2752` (9:16 vertical ratio).
- **Watermark Coordinates:**
  - Center: `(x=1423, y=2635)`
  - Dimensions: ~48px × 48px
  - Margins: 113px from right edge, 117px from bottom edge.

### 2.2 Dual-Stage Eradication & Branding Pipeline
Every slide generated for any episode MUST pass through the dual-stage branding script before final video assembly:

1. **Stage 1: OpenCV Telea Inpainting (Deep Watermark Eradication)**
   - A circular mask of radius `28px` is centered at `(1423, 2635)`.
   - `cv2.inpaint(img, mask, inpaintRadius=4, flags=cv2.INPAINT_TELEA)` restores the background texture/color under the watermark.
   - This ensures **zero residual watermark pixels** remain, even if the image is cropped or re-framed.

2. **Stage 2: Channel Bug Placement (Branded Overlay)**
   - The master channel logo is resized to `150 × 150` pixels (~9.8% of image width).
   - Centered directly over the bottom-right corner at `(x=1423, y=2635)` (top-left: `x=1348, y=2560`).
   - Composited with alpha blending using Lanczos resampling.
   - The image is saved at **98% JPEG quality with no chroma subsampling (`subsampling=0`)**.

---

## 3. Automation Script & Usage

### 3.1 Pipeline Script
- **Path:** [`pipeline/apply_channel_logo_branding.py`](file:///f:/Arnav%20-%20YT/stickman-video-director/pipeline/apply_channel_logo_branding.py)
- **Execution:**
  ```bash
  python pipeline/apply_channel_logo_branding.py
  ```
- **Custom Directory Flag:**
  Can be targeted at any episode's slides directory:
  ```python
  apply_channel_branding(slides_dir="projects/shorts/ep06_example/slides")
  ```

---

## 4. Production Enforcement
1. **Never Ship Raw Slides:** No video may be rendered using raw, unbranded slides from AI generators.
2. **Channel Watermark Consistency:** The channel badge must appear on all slides in the bottom-right corner to reinforce creator ownership and protect content against unauthorized re-uploads.
3. **Git Asset Tracking:** [`assets/branding/channel_logo.png`](file:///f:/Arnav%20-%20YT/stickman-video-director/assets/branding/channel_logo.png) is explicitly tracked in Git via `.gitignore` exclusion (`!assets/branding/channel_logo.png`) to ensure permanent cross-device availability.
