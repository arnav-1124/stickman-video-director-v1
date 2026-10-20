# Workspace Instructions: Stickman AI Animation Studio

## Critical Operational Rules

### 1. Mandatory Skills Pre-Flight (Rule: `skills_preflight_rule.md`)
**FOR EVERY AGENT SESSION AND FOR EVERY PROMPT**:
Before taking any action, writing code, executing pipeline commands, or designing animation architectures:
1. Identify all domains involved (e.g. 2D/3D animation, Three.js, GSAP, Remotion, FFmpeg, TTS, YouTube retention).
2. Look up the corresponding skills in `.agents/skills/` and global skills.
3. Read the `SKILL.md` file using `view_file`.
4. Apply the exact standards, schemas, and best practices documented in those skills.

### 2. Production Standards Law
All video rendering and audio mastering must adhere to `pipeline/production_standards.json`:
- Audio loudness: `-11.9 LUFS`, True Peak `-1.0 dBFS`.
- Subtitles: `.ass` SubStation Alpha, Arial Black, active gold highlight `&H0000D7FF&`.
- Frame rate & Canvas: 30fps (or 25fps for European sync standards), textured paper canvas `#FAF9F6`.
- Visual Pacing: 2.0s to 3.8s cut density floor.
