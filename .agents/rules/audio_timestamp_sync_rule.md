# Audio & Timestamp Synchronization Rule (Comic-Sync Standard)

## 1. Narration Standard (English Only)
* **Voice Profile:** `en-US-ChristopherNeural` (Deep, calm, articulate, authoritative male voice with clear studio acoustics).
* **Pacing:** ~145–155 words per minute.
* **Sub-Millisecond Word Timestamps:**
  Every word boundary must be captured in `word_timestamps.json` (`word`, `start_time`, `end_time`) via `pipeline/generate_audio.py`.

## 2. Semantic Clause Duration Mapping
* Slide transitions are not locked to arbitrary intervals.
* Each visual beat is mapped to the exact start and end timestamps of its spoken semantic clause:
  - Micro-action verbs (e.g. *"locks the door"*): ~0.8s
  - Concept cards (e.g. *"THE SILENT TRAP"*): ~1.3s–1.6s
  - Narrative mechanisms: ~1.8s–2.5s

## 3. Audio Mastering & Sound Bed
* **Integrated Loudness:** Strictly normalized to **-11.9 LUFS** with compressed dynamic range (**LRA: 2.0 LU**).
* **Continuous BGM Bed:** Lo-fi / dark ambient synth bed at `-22dB` to `-24dB` running non-stop.
* **Diegetic Foley:** Real-world sound effects anchored to visual actions (footsteps, keys, locker slams, phone chimes, whispering).

## 4. Kinetic Subtitles (.ass)
* SubStation Alpha karaoke subtitles generated from word timestamps.
* Safe zone: `MarginV: 400` (Lower-third, clear of Shorts UI).
* Active word: Gold highlight pop (`&H0000D7FF`) at 108% scale.
* Inactive words: Crisp solid white (`&H00FFFFFF`) with 4.5px black outline.
