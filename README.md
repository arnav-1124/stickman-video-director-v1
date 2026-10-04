# Stickman AI Animation Studio (Ink Explainer Edition)

A modern, prompt-based AI animation production pipeline for viral psychology and behavioral economics videos in the signature aesthetic of **The Paint Explainer** and **Ink Explainer**.

Engineered with the exact workflow architecture of **`yt-shorts-animation-v1`**, transitioning completely away from manual coordinate math into prompt-based AI video generation (Hailuo AI, Kling AI, Google Flow / Veo, Leonardo AI) combined with local studio-grade post-production assembly.

---

## 🎨 Visual Aesthetic ("The Paint Explainer")
1. **Canvas**: Clean off-white textured paper (`#FAF9F6`).
2. **Character**: Expressive 2D doodle stickman with a smooth circular white head and bold black ink strokes (`#0A0D14`).
3. **Pacing**: Rapid visual cuts every 2.5s to 4.0s (preventing AI morphing while keeping viewer retention high).
4. **Selective 1-Color Rule**: 95% monochrome, with only ONE accent color per scene (Crimson Red `#FF2A4D` for ego/danger, Electric Cyan `#00F0FF` for truth/clarity).
5. **Captions**: Kinetic SubStation Alpha (`.ass`) karaoke word-highlight subtitles (glowing gold active word, crisp white text, bold black outline).

---

## 📁 Repository Architecture
stickman-video-director/
├── .agents/
│   ├── rules/                 # Production rules (ink style, Gemini TTS, channel branding)
│   └── skills/                # Agent personas (storyboard-director, prompt-engineer, ffmpeg-master)
├── assets/
│   ├── branding/              # Official channel logo badge (PhD Stickman Graduate)
│   ├── bgm/                   # Ambient lo-fi & dark psychological background music
│   ├── sfx/                   # Pen scratches, thuds, wooshes, glass cracks
│   └── characters/            # Character blueprints and visual anchors
├── docs/
│   ├── voiceover_and_storytelling_standards.md # Google Gemini TTS ("Ludo"), dialogue & pacing
│   ├── channel_branding_and_watermark_protocol.md # Watermark inpainting & channel bug placement
│   ├── cloud_video_generation_roadmap.md      # Scaling blueprint
│   └── longform_topics_vault.md               # Longform topic library
├── instructions/
│   └── ink_explainer_mastery_playbook/        # 4-part master prompt engineering guide
├── pipeline/
│   ├── generate_gemini_tts.py                 # Google Gemini Flash TTS ("Ludo") synthesis
│   ├── apply_channel_logo_branding.py         # Telea inpainting & channel badge overlay
│   ├── calibrate_subtitles_ep05.py            # Linguistic semantic chunking & audio sync engine
│   ├── build_video.py                         # Studio-grade FFmpeg video builder & audio mixer
│   └── new_episode.py                         # Scaffolds new episodes from canonical template
├── scripts/                                   # Modular automation & diagnostic tools
│   ├── audio_calibration/                     # Word boundary profiling & acoustic analysis
│   ├── flow_browser_automation/               # Chrome DevTools (CDP) prompt automation
│   ├── chapter_audits/                        # Multi-chapter audits & gap analysis
│   └── experimental_tests/                    # Timing, PTS cadence, and video tests
├── projects/
│   ├── shorts/ep05_how_to_handle_disrespect/  # Active production episode
│   └── templates/canonical_episode/           # Canonical episode template
└── renders/                                   # Exported final production videos
```

---

## 🚀 The 5-Step Production Workflow

### Step 1: Scaffold Episode
```bash
python pipeline/new_episode.py --name ep02_the_silent_killer
```
*Creates a project folder initialized with `storyboard.json`, `prompts.json`, `build_manifest.json`, `raw/`, and `audio/`.*

### Step 2: Export Prompts for Cloud AI Generation
```bash
python pipeline/automate_pipeline.py projects/ep02_the_silent_killer --export-batch
```
*Generates `quick_batch_copypaste.txt` with formatted prompts for Hailuo AI (MiniMax), Kling AI, Flow AI, or Leonardo AI.*

### Step 3: Ingest Generated Video Clips
Download the generated clips into your default `Downloads` folder, then run:
```bash
python pipeline/automate_pipeline.py projects/ep02_the_silent_killer --ingest-videos
```
*Automatically sorts, renames, and moves downloaded MP4 files into `projects/ep02_the_silent_killer/raw/shot_1.mp4`, `shot_2.mp4`...*

### Step 4: Generate Voiceover & Kinetic Subtitles
```bash
# Generate voiceover with word-level boundary timestamps
python pipeline/generate_audio.py projects/ep02_the_silent_killer --voice christopher

# Generate active gold-highlight karaoke subtitles (9:16 Shorts or 16:9)
python pipeline/generate_subtitles.py projects/ep02_the_silent_killer --aspect 9:16
```

### Step 5: Studio FFmpeg Video Assembly
```bash
python pipeline/build_video.py projects/ep02_the_silent_killer/build_manifest.json
```
*Normalizes clips to 1080x1920 @ 30fps, concats video sequence, ducks background music under voiceover (-14 LUFS standard), burns kinetic subtitles, and exports the final video into `renders/`.*
