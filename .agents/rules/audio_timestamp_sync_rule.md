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

## 3. Audio Mastering & Sound Bed
* **Integrated Loudness:** Strictly normalized to **-11.9 LUFS** with compressed dynamic range (**LRA: 2.0 LU**).
* **Continuous BGM Bed:** Lo-fi / dark ambient synth bed at `-22dB` to `-24dB` running non-stop.
* **Diegetic Foley:** Real-world sound effects anchored to visual actions (footsteps, keys, locker slams, phone chimes, whispering).

## 4. Kinetic Subtitles (.ass)
* SubStation Alpha karaoke subtitles generated from word timestamps.
* Safe zone: `MarginV: 400` (Lower-third, clear of Shorts UI).
* Active word: Gold highlight pop (`&H0000D7FF`) at 108% scale.
* Inactive words: Crisp solid white (`&H00FFFFFF`) with 4.5px black outline.

