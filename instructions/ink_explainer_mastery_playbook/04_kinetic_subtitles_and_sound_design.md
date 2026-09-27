# 04: Kinetic Subtitles & Sound Design

## 1. High-Retention Karaoke Word-Level Captions
YouTube Shorts viewers drop off instantly if subtitles are static, low-contrast, or placed in unsafe UI areas.

### Subtitle Standards:
- **Font**: `Arial Black` or `Montserrat ExtraBold`
- **Case**: UPPERCASE for immediate readability at glancing speeds
- **Chunk Size**: Max 2–3 words visible at once
- **Color Coding**:
  - Inactive words: Crisp White (`&H00FFFFFF&`)
  - Active word pop: Vivid Glowing Gold (`&H0000D7FF&` BGR format)
  - Outline: Deep Charcoal/Black (`&H000A0D14&`), 4.5px thickness to guarantee 100% legibility over both paper and dark scenes.
- **Safe Zone**:
  - For 9:16 Shorts (1080x1920): `MarginV: 440` (Above the title, channel icon, and sound button).
  - For 16:9 Widescreen (1920x1080): `MarginV: 85`.

---

## 2. Audio Mastering & Sound Design

### Sound Layers:
1. **Voiceover Narration**:
   - Mastered to -14 LUFS integrated loudness.
   - Paced with subtle 0.3s breathing pauses between logical beats.
2. **Background Music (BGM)**:
   - Subtle lo-fi, contemplative piano, or dark synth drone (`assets/bgm/`).
   - Sidechain compressed (automatically ducked by -12dB whenever narration speaks).
3. **Foley & Sound Effects (SFX)**:
   - `subtle_pen_scratch.mp3`: On text or diagram drawing.
   - `bass_drop_thud.mp3`: On harsh psychological truths or hook punchlines.
   - `woosh_fast.mp3`: On camera punch-in or scene transitions.
