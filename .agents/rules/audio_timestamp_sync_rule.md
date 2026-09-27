# Audio & Video Generation Rule: Native Veo 3.1 Audio Standard

> **MANDATE:** As per studio directive, audio is NOT generated locally via TTS. The production pipeline exclusively utilizes Google Veo 3.1's native multimodal Video + Audio generation.

---

## 1. Google Veo 3.1 Native Audio Architecture
- **Primary Source:** Veo 3.1 generates both the visual motion and native audio track (narration dialogue, Foley effects, and room tone) simultaneously in Google Flow / VideoFX.
- **The 15-Word Rule (Strict Duration Constraint):**
  - Veo 3.1 clips have a strict 8-second limit.
  - To prevent Veo from mumbling or cutting off narration before 8 seconds, **each shot's narration text in `[Audio Cues]` MUST be strictly 12 to 18 words (target: 14-16 words)**.
  - ❌ *Never put 25+ word paragraphs in Veo `[Audio Cues]`.*

---

## 2. Assembly & Sound Layering
- **Primary Dialogue Track:** The native audio stream from `clip_0X.mp4` is preserved at full volume.
- **Background Music (BGM):** A subtle lo-fi contemplative drone or psychological track (`assets/bgm/`) is mixed underneath at low volume (`-18dB` to `-22dB`) to maintain consistent atmosphere across cuts without competing with Veo's dialogue.
- **Final Loudness:** Normalized to broadcast **-14 LUFS** standard.

---

## 3. Animated Kinetic Subtitles
- SubStation Alpha (`.ass`) kinetic karaoke subtitles are generated from the prompt's spoken narration text.
- Word boundaries are paced to match the 8.0s clip (onset at ~0.5s, active gold highlight `&H0000D7FF` with 108% scale pop, solid white inactive words, thick black outline).
- Subtitles are positioned in the safe lower-third (`MarginV: 350` to `400`) above platform UI overlays.
