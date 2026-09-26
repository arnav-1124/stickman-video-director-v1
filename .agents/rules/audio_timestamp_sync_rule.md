# Audio Timestamp Synchronization Rule

## 1. Voice Synthesis Engine
- Primary engine: `edge-tts`.
- Recommended voice profiles:
  - `en-US-ChristopherNeural` (Pitch `-4Hz`, Rate `+0%`): Authoritative, deep, analytical.
  - `en-US-BrianNeural` (Pitch `-2Hz`, Rate `+3%`): Crisp, sophisticated, narrative.

## 2. Millisecond Timestamp Extraction
- TTS generation must output word-level boundary events:
  `{"word": "Silence", "start_ms": 1250, "end_ms": 1720}`
- Keyframe animations, kinetic subtitles, and audio sound effects MUST trigger within $\pm 40\text{ms}$ of word onset.
