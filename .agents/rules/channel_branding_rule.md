# Channel Branding & Watermark Replacement Rule

## Mandatory Branding & Watermark Eradication Standard

Every episode produced in this repository must adhere to the official channel branding guidelines:

### 1. Master Channel Logo
- **Asset Location:** [`assets/branding/channel_logo.png`](file:///f:/Arnav%20-%20YT/stickman-video-director/assets/branding/channel_logo.png)
- **Visual Subject:** Stickman in academic graduation cap and black gown, holding the "A PhD" book in a circular badge.
- **Tracking:** Permanently version-controlled in Git.

### 2. Mandatory Slide Post-Processing Gate
Before building the final video or compiling `build_manifest.json`:
1. All slide images in `slides/` generated from Google Imagen / Gemini Image must be inspected for the bottom-right corner 4-pointed sparkle watermark at `(1423, 2635)`.
2. The agent or pipeline MUST run [`pipeline/apply_channel_logo_branding.py`](file:///f:/Arnav%20-%20YT/stickman-video-director/pipeline/apply_channel_logo_branding.py).
3. The script executes:
   - OpenCV Telea inpainting on the watermark region.
   - Compositing of [`assets/branding/channel_logo.png`](file:///f:/Arnav%20-%20YT/stickman-video-director/assets/branding/channel_logo.png) (150x150) at `(1348, 2560)` over the bottom-right corner.
   - 98% JPEG re-save without chroma subsampling.
4. **Prohibition:** NEVER build or deliver a video containing raw AI platform watermarks.
