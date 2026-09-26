# Stickman & Whiteboard Animation Studio (v2.0)

Automated, high-retention vertical short-form video engine for **@code_animation_studio** (YouTube Shorts, Reels, TikTok).

## Channel Focus
- **Niches:** Dark Psychology, Behavioral Economics, Systemic Finance Traps, Cognitive Biases.
- **Audience:** Adults, professionals, curious thinkers.
- **Pacing:** Strict 60-second runtime, sub-second word-level audio synchronization, high APV (>85%).

## Architecture Overview
- **Visuals:** Deterministic vector animations (Stickman line art, whiteboard chalk/marker animations, kinetic spotlight cones, aura effects).
- **Audio:** `edge-tts` (authoritative voices: Christopher / Brian) with exact word-level timestamp alignment.
- **Pipeline:**
  1. `psychology-researcher`: High-CTR hooks & counter-intuitive mechanisms.
  2. `retention-scriptwriter`: 60-second 5-beat clock (Hook -> Mechanism -> Contrast -> Actionable Rule -> Seamless Loop).
  3. `stickman-animator`: Vector keyframing driven by word timestamps.
  4. `ffmpeg-master`: Kinetic captions, dark ambient BGM ducking, -14 LUFS mastering.
  5. `youtube-publisher`: SEO title options, psychology tags, publishing metadata.

## Execution Modes
- **Dry-Run Preview (10 seconds, zero compute cost):**
  ```bash
  python pipeline/run_short.py --topic "The Spotlight Effect" --preview
  ```
- **Autonomous Master Render (60 seconds):**
  ```bash
  python pipeline/run_short.py --topic "The Spotlight Effect"
  ```
