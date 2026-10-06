# Audio & Timestamp Synchronization Rule (Comic-Sync Standard)

## 1. Narration Standard (Google Gemini TTS Engine)
* **Master Voice Profile:** `gemini-3.8-flash-tts` ("Ludo" persona — deep, calm, articulate, authoritative, seasoned senior mentor).
* **Storytelling & Expressive Modulation:**
  - Capable of per-dialogue emotional modulation (subtext, quiet confidence, vulnerability, micro-pauses).
  - Use conversational bridging phrases (e.g., *"Something like, 'What's the joke?'"*) to make storytelling sound like a real human in the room.
* **Acoustic Syllable Calibration:**
  - Syllable onsets derived from acoustic RMS energy profiles in [`voiceover_googleTTS.wav`](file:///f:/Arnav%20-%20YT/stickman-video-director/projects/shorts/ep05_how_to_handle_disrespect/audio/voiceover_googleTTS.wav).
* **Perceptual Audio Sync Delay:**
  - Mandatory `+70ms` (`SYNC_DELAY = 0.07`) offset applied to kinetic subtitle highlighting so visual pop hits in sync with spoken vowels.
* **Linguistic Semantic Chunking Law:**
  - Subtitle words MUST be grouped into natural grammatical phrases (e.g. `[A, SLICK, JOKE]`, `[AT, YOUR, EXPENSE]`).
  - NEVER strand prepositions or break idiomatic phrases across arbitrary chunk-size thresholds. Each chunk must remain on screen for at least 550ms–700ms.

## 2. Semantic Clause Duration Mapping & 100% Visual Sync Law
* Slide transitions are **never locked to arbitrary intervals or sliced mechanically by punctuation**.
* **Zero-Tolerance Desync Standard:** Every cut must be 100.000% frame-bound to what the viewer is seeing.

### The "Sentence Boundary Trap" (Strictly Prohibited):
Never split shots purely at periods or commas. Spoken sentences often serve as rhetorical bridges; slicing purely by syntax causes premature cuts (jumping ahead 2–4s) or delayed hangs (stale visuals idling 2–3s).

### The 4 Ironclad Sync Principles:
1. **The Visual Prop Retention Rule (Preventing Early Slide Cutaway):**
   - If a spoken clause, rhetorical question, or reflection refers to, describes, or questions a prop, diagram, or character state currently on screen (e.g., *"Will three cherries align, or will you lose everything?"* when the slide depicts spinning reels with cherries), **that slide MUST remain visible until that clause concludes**.
   - NEVER cut to the next slide while the narrator is still discussing elements depicted in the previous slide.
2. **The Text Card & Stamp Zero-Latency Rule (Preventing Delayed/Idle Cards):**
   - If a slide is a text card, rubber stamp, typography punch, or label diagram (e.g., `[RELIABLE] [SAFE] [BORING]`, `DOPAMINE ≠ PLEASURE`), the cut to that slide **MUST hit exactly on the first spoken word that corresponds to that text**.
   - NEVER bundle an introductory preamble sentence into a text punch card. Preamble sentences belong to the preceding scene so the text card punches in with immediate, zero-latency impact.
3. **The Dramatic Reveal & Punchline Snapping Rule:**
   - In dramatic pivots, character reactions, or punchline reveals (e.g., transitioning from a calm setup to a manic/obsessed character), the cut to the reaction visual MUST snap on the punchline trigger clause itself (e.g., *"What did the pigeon do? It became completely obsessed."*).
   - Any concluding setup clause (e.g., *"The reward was completely unpredictable."*) belongs to the preceding diagram/setup slide, NOT the reaction slide.
4. **Mandatory Pre-Render Visual-Audio Audit Gate:**
   - Before compiling `storyboard.json` or rendering video segments:
     - Audit every shot boundary: verify that the spoken clause starts and ends strictly within the visual context of that slide.
     - Match against exact word timestamps (`word_timestamps.json`).
     - Reject any segmentation where a slide appears before its visual cue is spoken or remains after its visual subject has changed.
5. **The 1:1 Idea-to-Visual Allocation Rule (Anti-Static Audio Overhang Law):**
   - **Zero Static Audio Overhang:** Never lump multiple distinct narrative sentences, actions, or psychological transitions into a single static slide.
   - If a script passage contains multiple distinct thoughts, behaviors, or actions (e.g., *"They smile too broadly. They follow you down the aisle. They offer you discounts..."* or *"They have their own orbit. They are not auditioning for your approval. And because they refuse to sell themselves..."*), **each distinct sentence/action MUST have its own dedicated visual slide**.
   - **No Idle Graphic Lingering:** A slide designed around one specific metaphor or action (e.g., celestial orbit, discount sign, bear trap) must NEVER linger statically while subsequent audio advances to new psychological concepts.
   - **Maximum Duration Ceiling:** Informative and narrative shots should naturally sit in the 2.0s–5.5s window. Any shot approaching or exceeding 6.0s that contains multiple sentences/clauses is an immediate red flag for an unrepresented visual gap and MUST be decomposed so each beat gets its own frame.
   - **1:1 Idea-to-Visual Parity:** Every meaningful sentence in `script.txt` must map 1:1 to a distinct, dedicated visual beat in `storyboard.json`.

## 3. The 0.380s Inter-Sentence Pause Law & Pause-Center Cut Alignment
* **Locked Inter-Sentence Pause:** Strictly **0.380 seconds** (`PAUSE = 0.380s`).
* **Pause-Center Visual Cut Law:**
  - Visual transitions NEVER happen abruptly on the first syllable or trailing breath of speech.
  - Slide cuts switch at the exact acoustic center of the 0.380s breath:
    - `cut_start = speech_start - 0.190s`
    - `cut_end = speech_end + 0.190s`
  - **Effect:** The slide is established 190ms before narration begins, giving zero visual lag and 100% viewer anticipation.

## 4. Audio Mastering & Deep Masculine EQ Chain
* **Master Voice Profile:** Google Gemini TTS (`Ludo` voice, en-US).
* **Deep Masculine EQ Chain:**
  - 115Hz: `+4.2dB` (chest resonance / authoritative vocal weight, Q=1.2).
  - 250Hz: `+2.0dB` (warmth & body, Q=1.0).
  - 3.5kHz: `+2.5dB` (crisp articulation & presence, Q=1.2).
* **Vocal Compand:** `attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6`
* **Integrated Loudness:** Strictly normalized to **-11.9 LUFS** (`loudnorm=I=-11.9:TP=-1.0:LRA=6.0`).
* **Continuous BGM Bed:** Lo-fi / dark ambient synth bed at `volume=0.08` ducked under speech.

## 5. Kinetic Subtitles (.ass) Standard
* **Typography:** `Arial Black`, Size: `54pt` (for 1080p landscape).
* **Colors & Styling:**
  - Active word: Radiant Gold highlight pop (`&H0000D7FF&`) with scale bounce `\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)`.
  - Inactive words: Solid pure white (`&H00FFFFFF&`).
  - Outline: 5.5px deep ink black (`&H000A0D14&`).
  - Shadow: 2.0px semi-transparent black (`&HA0000000&`).
* **Positioning:**
  - 16:9 Landscape: `MarginV: 110` to `120` (lower third, clear of player seekbar).
  - 9:16 Vertical: `MarginV: 400` (safe zone above Shorts UI).
* **Burst Size:** 2–3 words per burst.
* **CRITICAL FFmpeg Pipeline Law (The Constant Frame Rate Rule):**
  - When rendering subtitles over concatenated still images in FFmpeg, the video stream MUST pass through `fps=25` (or `fps=30`) BEFORE the `subtitles=` filter.
  - Variable frame rate (VFR) streams cause libass to drop frames or fail to render subtitle animations.


