# Standardized Prompt Presentation & Veo Audio Rule

### 1. Mandatory Prompt Presentation Format
Whenever providing prompts for generation, the Prompt Engineer must ALWAYS output using this exact structure:
- **Input / Ingredients to attach:** (e.g., None for anchor image, or Upload shot_X.jpg for Veo I2V)
- **Model:** (e.g., Nano Banana Pro / Google Veo 3.1)
- **Duration / Type:** (e.g., Static 2D Image for Phase 1 / 8 seconds for Phase 2)
- **Dimension:** (e.g., 9:16 Vertical / 1080x1920)
- **Camera:** (e.g., Static fixed camera hold)
- **Copyable Prompt Box:** (fenced code block containing the exact copy-pasteable prompt)

### 2. Veo 3.1 Native Audio Inclusion
Veo 3.1 generates native audio, dialogue, and sound effects when instructed. Every Veo prompt must include both:
- **[Visual Motion]:** Narrow 1s-1.5s intervals, subtle micro-actions, anti-hallucination guardrail.
- **[Audio Cues]:** 
  - **Voice Profile (Mandatory for Consistency):** Deep, mature, calm, authoritative male narrator with steady pacing and quiet confidence (American accent, clear studio microphone quality).
  - **Narration:** Strictly 14 to 16 words per 8-second clip.
  - **Sound Effects (SFX):** Diegetic sounds (e.g., `high-heel clicks`, `bicycle pump squeak`, `coffee sip`).
  - **Atmosphere/Ambience:** Environmental room tone.

### 3. Audio Responsibility Division
- **Veo 3.1 (In-Clip Audio):** Generates synchronized character speech, Foley SFX, and room tone.
- **FFmpeg-Assembler (Post-Production):** Merges the clips, layers subtle background music (`-18dB` to `-22dB`), standardizes loudness to -14 LUFS, and burns kinetic animated subtitles.
