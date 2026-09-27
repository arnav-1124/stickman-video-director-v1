# Ink Explainer Studio: Mastery Playbook

Comprehensive guidelines and technical specifications for generating viral minimalist stickman psychological animations in the style of **The Paint Explainer** and **Ink Explainer**.

## Table of Contents
1. [01: Core Architecture & Prompt Anatomy](01_core_architecture_and_prompt_anatomy.md)
   - Visual DNA, 4 pillars, 5-part prompt anatomy, negative prompt vault.
2. [02: Cinematography & Motion Control](02_cinematography_and_motion_control.md)
   - The 2.5s-4s pacing rule, anti-morphing directives, kinetic choreography.
3. [03: AI Video Engines & Free Cloud Workflows](03_ai_video_engines_and_free_workflows.md)
   - Hailuo AI, Kling AI, Flow/Veo, Luma, Leonardo AI workflows and automation.
4. [04: Kinetic Subtitles & Sound Design](04_kinetic_subtitles_and_sound_design.md)
   - Word-level active gold highlights, safe zones, loudness standards, SFX library.

## Quick CLI Reference
```bash
# 1. Scaffold new episode from template
python pipeline/new_episode.py --name ep01_topic_name

# 2. Export prompt batch for web UI generation
python pipeline/automate_pipeline.py projects/ep01_topic_name --export-batch

# 3. Ingest generated videos from Downloads folder into raw/
python pipeline/automate_pipeline.py projects/ep01_topic_name --ingest-videos

# 4. Generate voiceover and word boundary timestamps
python pipeline/generate_audio.py projects/ep01_topic_name

# 5. Build kinetic ASS subtitles
python pipeline/generate_subtitles.py projects/ep01_topic_name --aspect 9:16

# 6. Assemble production video with FFmpeg
python pipeline/build_video.py projects/ep01_topic_name/build_manifest.json
```
