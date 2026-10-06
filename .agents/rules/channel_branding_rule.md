# Channel Branding & Watermark Replacement Rule

## Mandatory Channel Identity & Watermark Eradication Standard

Every episode produced in this repository must adhere to the official channel branding guidelines:

### 1. Official Channel Identity
- **Channel Name:** **Sticky in Dark**
- **Niche & Format:** Episodic dark psychological explainer films and dynamic comic shorts exploring human relationships, attraction paradoxes, and cognitive behavioral blindspots.
- **Narrative Archetype:** Seasoned, calm mentor providing unvarnished psychological truths through expressive 2D stickman animations.

### 2. Master Channel Logo
- **Asset Location:** [`assets/branding/channel_logo.png`](file:///f:/Arnav%20-%20YT/stickman-video-director/assets/branding/channel_logo.png)
- **Visual Subject:** Stickman in academic graduation cap and black gown, holding the "A PhD" book in a circular badge.
- **Tracking:** Permanently version-controlled in Git.

### 3. Watermark Masking Standards (Landscape & Portrait)
Before building the final video or compiling `build_manifest.json`:
1. All slide images generated from Google Imagen / Gemini Image have the bottom-right AI watermark covered by the channel logo badge:
   - **16:9 Landscape (1920x1080):** Channel logo scaled to `110x110` composited at `(1800, 960)`.
   - **9:16 Portrait (1080x1920 / 1536x2752):** Channel logo scaled to `150x150` composited at `(1348, 2560)` (or `(900, 1780)` on 1080x1920).
2. **Prohibition:** NEVER build or deliver a video containing raw AI platform watermarks.

