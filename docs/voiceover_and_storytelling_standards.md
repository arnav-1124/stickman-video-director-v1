# Voiceover & Human Storytelling Standards (Google Gemini TTS Engine)

## 1. Engine & Voice Persona Architecture

### 1.1 The Engine Selection: Google Gemini Flash TTS
We have transitioned the core narration pipeline from robotic/generic TTS engines (Edge-TTS / standard neural voices) to **Google Gemini TTS** (`gemini-3.8-flash-tts` / `gemini-2.0-flash-exp`).

**Why Google Gemini TTS:**
- **Dynamic Emotional Depth:** The engine understands subtext, sarcasm, dramatic pauses, and psychological tension rather than reading words with monotonic pitch.
- **Micro-Dialogue & Character Modulation:** Allows modulating tone, pacing, depth, and timbre per dialogue line, sentence, or specific phrase.
- **Conversational Storytelling Realism:** Conveys the presence of a real, experienced human talking directly to the viewer—delivering advice with seasoned authority, warmth, and reflective pause.

### 1.2 The Master Voice Profile: "Ludo"
- **Voice Name:** `Ludo`
- **Archetype:** Experienced Senior / Calm Psychologist / Grounded Big Brother.
- **Vocal Characteristics:** Deep, warm, measured, reflective, articulate, and conversational.
- **Audio Specification:** PCM WAV, 24kHz / 44.1kHz, mono or stereo, dynamic range preserved for studio sidechain ducking.

---

## 2. Storytelling Dialogue & Tone Direction Principles

### 2.1 The "Living Conversation" Law (Anti-Robotic Narration)
The voice must never sound like a textbook lecture or an audio-book narrator reciting text. It must feel like an intimate conversation across a coffee table:
1. **Conversational Bridging:**
   Use natural framing phrases that humanize quotes and examples.
   - *Example:* Instead of abrupt quotes (`"What's the joke?"`), use conversational bridges:
     > `"Wait, I didn't get it." Something like, "What's the joke?"`
   - This differentiates general narration from specific real-world scripts.
2. **Pacing & Emotional Weight:**
   - **Setups:** Measured, steady pace (140–150 wpm) establishing tension and relatable friction.
   - **Pivots & Realizations:** Deliberate micro-pauses (300ms–500ms) before delivering key psychological insights (e.g., *"Most guys freeze."* or *"Notice what happens next."*).
   - **Punchlines / Actionable Scripts:** Crisp, quiet confidence. Never aggressive, never hurried.

### 2.2 Dialogue & Voice Customization Capabilities
With the Gemini TTS engine, each line can be shaped with targeted vocal direction prompts:
- **Intimacy / Whispered Wisdom:** Lower register, closer mic proximity for philosophical secrets.
- **Empathy / Vulnerability:** Softer attack on words describing social anxiety or feeling disrespected.
- **Authority / Reassurance:** Firm, unshakeable resonance when delivering psychological counter-tactics.

---

## 3. Pipeline Automation & Scripting

### 3.1 Script Location & Configuration
- **Script:** [`pipeline/generate_gemini_tts.py`](file:///f:/Arnav%20-%20YT/stickman-video-director/pipeline/generate_gemini_tts.py)
- **API Key Management:** Kept strictly in project root `.env` (`GEMINI_API_KEY`), never inside episode folders, and protected by `.gitignore`.
- **Command Syntax:**
  ```bash
  python pipeline/generate_gemini_tts.py --project projects/shorts/ep05_how_to_handle_disrespect --voice Ludo
  ```

---

## 4. Acoustic Calibration & Subtitle Synchronization

### 4.1 The 0.380-Second Inter-Sentence Pause Law (User-Locked Standard)
Natural storytelling pacing requires measured, intentional breathing space without dead silence:
- **Locked Inter-Sentence Pause:** **0.380 seconds** (`PAUSE_DURATION = 0.380s`).
- **Acoustic Pause-Center Visual Cut Law:**
  - Visual transitions NEVER happen at the beginning or end of speech.
  - Slide cuts switch at the exact acoustic midpoint of the 0.380s breath:
    - `cut_start = speech_start - 0.190s`
    - `cut_end = speech_end + 0.190s`
  - **Effect:** The incoming visual frame is already established on screen 190ms before the narrator begins speaking, eliminating the perception of visual lag and creating instantaneous cognitive anticipation.

### 4.2 Syllable Energy & Onset Profiling
- Speech boundaries are extracted based on true RMS vocal energy profiles.
- Never use simple word-count division over raw unsegmented audio.

### 4.3 Kinetic Subtitle Specifications (16:9 Landscape & 9:16 Portrait)
Subtitles are formatted as SubStation Alpha (`.ass`) karaoke events:
- **Font & Typography:** `Arial Black`, Size: `54pt` (for 1080p landscape).
- **Colors:**
  - Base Inactive Text: Pure White (`&H00FFFFFF&`)
  - Active Word Highlight: Radiant Gold / Amber (`&H0000D7FF&`) with subtle pop bounce `\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)`.
  - Outline: 5.5px deep ink black (`&H000A0D14&`).
  - Shadow: 2.0px semi-transparent black (`&HA0000000&`).
- **Positioning:**
  - 16:9 Landscape: `Alignment: 2` (Bottom Center), `MarginV: 110` (lower third, above UI progress bars).
  - 9:16 Vertical: `Alignment: 2` (Bottom Center), `MarginV: 400` (safe zone above Shorts interaction rail).
- **Chunking:** 2 to 3 words per burst for rapid scanning and zero screen crowding.
- **CRITICAL FFmpeg Pipeline Law (The Constant Frame Rate Rule):**
  - When rendering subtitles over image sequences via FFmpeg concat demuxer, the video stream MUST pass through `fps=25` (or `fps=30`) BEFORE the `subtitles=` filter.
  - *Example:* `[0:v]fps=25,scale=1920:1080,...[v_fps];[v_fps][logo]overlay=...[v_masked];[v_masked]subtitles=sub.ass[v_out]`
  - Without `fps=25`, FFmpeg defaults to Variable Frame Rate (0.39 fps), causing `libass` to drop or fail to render subtitle animations.

---

## 5. Audio Mastering & Deep Masculine EQ Chain
To achieve maximum masculine resonance, vocal presence, and broadcast polish, every voiceover track passes through the calibrated DSP chain:
1. **Chest Resonance Boost:** `equalizer=f=115:width_type=o:w=1.2:g=4.2` (+4.2dB at 115Hz for authoritative vocal weight).
2. **Body Warmth:** `equalizer=f=250:width_type=o:w=1.0:g=2.0` (+2.0dB at 250Hz for rich harmonic foundation).
3. **Articulation & Presence:** `equalizer=f=3500:width_type=o:w=1.2:g=2.5` (+2.5dB at 3.5kHz for crisp vocal clarity).
4. **Vocal Pressure Compand:** `compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6` (tames peaks, thickens subtle whispers).
5. **Broadcast Loudness:** `loudnorm=I=-11.9:TP=-1.0:LRA=6.0` (punchy, broadcast-standard loudness).
6. **BGM Bed:** Continuous lo-fi / dark ambient synth bed at `volume=0.08` with ducking during speech.

---

## 6. Channel Branding & Watermark Replacement Standard
- **Official Channel Name:** **Sticky in Dark**
- **Channel Identity:** Dark psychological explainer cartoons exploring human nature, relationship dynamics, and cognitive traps.
- **Watermark Masking:**
  - 16:9 Landscape: Channel logo badge (`assets/branding/channel_logo.png`) scaled to `110x110` overlaid at `(1800, 960)` covering Google Imagen bottom-right watermark.
  - 9:16 Vertical: Channel logo badge scaled to `150x150` overlaid at `(1348, 2560)`.

---

## 7. Long-Form Packaging & Publishing Standards (Day One Films Architecture)
For all 16:9 long-form episodic animated short films, packaging strictly follows the minimalist, high-CTR template inspired by **Day One Films**:
- **Title Signature Formula:** `[VISCERAL PAIN POINT / PROVOCATION] | An Animated Short Film (Chapter X)`
  - Primary example: `YOU REPLIED INSTANTLY - Problem? | An Animated Short Film (Chapter 1)`
  - Ultra-clean alternate: `YOU REPLIED INSTANTLY | An Animated Short Film (Chapter 1)`
  - Emotional pain: `LEFT ON READ | An Animated Short Film (Chapter 1)`
  - Behavioral core: `CHASING | An Animated Short Film (Chapter 1)`
- **Thumbnail Layout:** 1920×1080 canvas, single atmospheric emotional scene (e.g. 2:00 AM dark room with phone screen glow). Centered hand-drawn bold typography with generous negative space (>80px margin) matching the title dilemma.
- **Outro Hook & Teaser Structure:** Every film concludes with an Open Loop slide teasing the next chapter (e.g., Slide 37 teasing *Chapter 02: The Casino Effect*), with elevated subtitles (`OutroWordSub`, `MarginV=240`) avoiding CTA button collision and a 1.5s–2.0s silent visual hold with smooth BGM fadeout.

---

## 8. Standing Pacing & Version Preservation Policy
1. **Natural Pacing Baseline:** Default to 100% natural, unhurried conversational cadence from the initial generation for all future chapters.
2. **Strict Version Preservation:** Never overwrite or delete prior master renders; all versions (`V1_MASTER.mp4`, `V2_CALIBRATED.mp4`, `V3_WITH_OUTRO.mp4`) must be preserved in dedicated deliverable files.


