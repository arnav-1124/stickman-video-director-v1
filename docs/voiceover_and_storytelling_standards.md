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

### 4.1 Acoustic Syllable Calibration
Because Gemini TTS breathes, pauses, and inflects like a real human, mechanical word-spacing algorithms will fail if uncalibrated.
- Audio energy profiles (RMS energy across 20ms–50ms sliding windows) must be evaluated to detect true vocal onsets.
- Never rely on static sentence-duration averaging.

### 4.2 The +70ms Perceptual Audio Sync Delay
Human vision detects animated motion faster than the auditory cortex processes phonemes.
- **Rule:** A `SYNC_DELAY = +0.07s` (70ms) offset is applied to all `.ass` subtitle highlight events.
- **Effect:** The gold pop animation hits *precisely* on the spoken vowel peak, completely eliminating the distracting sensation of captions appearing "a few milliseconds faster" than the speaker's voice.

### 4.3 Linguistic Semantic Chunking (No Stranded Phrases)
Subtitles must group words into complete semantic and grammatical units:
- **Prohibited:** Splitting idiomatic phrases (e.g., `["slick", "joke", "at"]` followed by `["your", "expense"]`).
- **Enforced:** Complete semantic phrases on screen together:
  - `[A, SLICK, JOKE]` (Noun phrase)
  - `[AT, YOUR, EXPENSE]` (Prepositional phrase)
  - `[SOMETHING, LIKE,]` (Conversational bridge)
  - `["WHAT'S, THE, JOKE?"]` (Dialogue punchline)
- Each chunk remains on screen for **at least 550ms–700ms**, allowing effortless reading comprehension.

---

## 5. Audio Mastering & Loudness Standards
- **Voiceover Track:** Normalized to **-14 LUFS** integrated loudness (compliant with YouTube mobile standards) with a true peak ceiling of `-1.0 dBFS`.
- **BGM Bed:** Continuous lo-fi / dark ambient synth bed at `-22dB` to `-24dB`.
- **Dynamic Sidechain Ducking:** BGM ducks automatically when speech is present (`attack=50ms`, `release=400ms`, `ratio=4:1`).
