# Chapter 06: Audio Cues & Native Dialogue Grounding

> "Sound is 50% of the cinematic experience. Veo 3.1 is the first frontier model that generates video and audio as a single multimodal entity."

Veo 3.1 features native audio synthesis. When prompted properly, it generates synchronous character dialogue, Foley sound effects, and acoustic room tone directly within the `.mp4` container.

---

## 1. The 3-Track Audio Prompt Structure

To get clean, professional audio from Veo 3.1 without garbled speech or missing sound effects, format your audio block with **explicit 3-track separation**:

```text
[Audio Cues]:
- Dialogue (at Xs): [Character Name] [vocal tone]: "[Short, crisp spoken sentence]"
- Sound Effects (at Xs): [Specific physical acoustic impact sound]
- Ambience: [Continuous environmental room tone and acoustic texture]
```

### Directorial Rules for Dialogue:
1. **Short, Simple Sentences:** Diffusion speech synthesis performs best on punchy, 3-to-7 word phrases (e.g., *"Look! Giant fluffy footprints!"*). Avoid dense, run-on sentences.
2. **Specify Timestamp:** Always give Veo an exact time cue (e.g., `Dialogue (at 3s):`) so the model aligns lip-sync and jaw movements with the corresponding video frame.
3. **Specify Vocal Emotion:** Include the tone in brackets (e.g., `in a serious detective whisper:`, `shouts with joyful laughter:`).

---

## 2. Foley Sound Design Vocabulary

The more specific your acoustic description, the more realistic the sound synthesis:

| Vague (Poor) | Studio-Grade Foley Term (Effective) |
| :--- | :--- |
| *"Footsteps"* | `Crisp running sneakers stomping on lush green turf` |
| *"Robot sound"* | `High-tech electronic scanner laser chirp and ascending discovery chime` |
| *"Ball sound"* | `Clean, solid soccer ball kick followed by hollow goal net thwack` |
| *"Sigh"* | `Deep, gentle, heavy creature sigh with soft fluttering exhale ("Huuuuh...")` |
| *"Cheering"* | `Loud, enthusiastic crowd applause and children laughing in unison` |

---

## 3. Post-Production Audio Pipeline (FFmpeg Mixing)

Even though Veo generates native audio, professional YouTube Shorts require an **overarching background music (BGM) score** and **loudness compliance**.

Our studio script [`pipeline/build_video.py`](file:///e:/yt-shorts-animation-v1/pipeline/build_video.py) automates this:
1. **Preserves Native Veo Sound:** Extracts the dialogue and Foley audio from each raw clip.
2. **BGM Sidechain Ducking:** When a character speaks, the background music volume automatically ducks by -12dB.
3. **YouTube Loudness Standard:** Normalizes master audio to **-14 LUFS** (integrated loudness) and **-1.0 dB True Peak**, ensuring your Shorts play at full, crystal-clear volume on mobile devices without clipping or distortion.
