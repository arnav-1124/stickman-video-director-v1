# Helper Scripts & Automation Taxonomy

This directory contains utility, calibration, diagnostic, and automation scripts organized into modular subdirectories.

> **Production Pipelines Note:** Core production builders and generative pipelines are housed in [`pipeline/`](file:///f:/Arnav%20-%20YT/stickman-video-director/pipeline/). The scripts here provide specialized sub-tasks, diagnostics, and legacy chapter utilities.

---

## Directory Architecture

```
scripts/
├── audio_calibration/       # Speech onset, TTS diagnostics, and word boundary profiling
├── flow_browser_automation/ # Chrome DevTools (CDP) & browser-assisted asset generation
├── chapter_audits/          # Historical chapter audits, gap analysis, and batch builders
└── experimental_tests/      # Timing, PTS cadence, and video stitcher experiment benchmarks
```

---

### 1. `audio_calibration/` (Acoustic & Subtitle Diagnostics)
- **`align_google_tts.py`**: Aligns Gemini TTS output with word boundaries.
- **`analyze_exact_word_timings.py`**: Inspects sub-millisecond word onsets from audio envelopes.
- **`analyze_pacing.py`**: Computes words-per-minute and clause density metrics.
- **`forensic_audio_analysis.py`**: Detailed spectral and waveform analysis.
- **`generate_google_tts.py`**: Standalone helper for testing Google TTS voices.
- **`generate_ludo_subtitles.py`**: Experimental subtitle generation for Ludo voice passes.
- **`generate_ep05_audio.py`**: Episode 05 voiceover synthesis script.
- **`prepare_ep05_build_manifest.py`**: Build manifest builder and timing assembler.
- **`render_sample_cadence_videos.py`**: Generates visual timing comparisons for pacing review.

### 2. `flow_browser_automation/` (CDP & Browser Automation)
- **`flow_cdp_controller.py`**: Chrome DevTools Protocol controller for browser automation.
- **`trigger_flow_slide.py`**: Sends automated prompt triggers to web-based generation interfaces.
- **`send_enter.py`**: Low-level keystroke injector for automated prompt submission.
- **`inspect_flow_images.py`**: Audits downloaded image assets from web generation flows.
- **`download_slide_variants.py`**: Batch downloader for variant generations.

### 3. `chapter_audits/` (Longform Chapter Tools & Audits)
- **`analyze_ch02_word_boundaries.py`**: Word timing analysis for Chapter 02.
- **`audit_ch03_visual_gaps.py`**: Identifies unrepresented visual clauses in Chapter 03.
- **`audit_chapter_02.py` / `audit_chapter_03.py`**: Narrative and visual completeness audits.
- **`audit_chapter_prompts.py`**: Consistency checks on prompt parameters across chapters.
- **`audit_master_assets.py`**: Verifies presence and integrity of master character assets.
- **`forensic_master_audit.py`**: Comprehensive asset and script audit tool.
- **`generate_all_slide_prompts.py`**: Bulk generator for multi-chapter slide prompts.
- **`build_chapter_01_video.py` / `build_chapter_02_video.py` / `build_chapter_03_video.py`**: Legacy assembly scripts for Chapters 01–03.
- **`rebuild_flawless_chapter_01.py` / `rebuild_flawless_chapter_03.py`**: Pacing rebuilders.
- **`update_ch01_flawless_prompts.py` / `update_ch01_pacing.py`**: Chapter 01 prompt & pacing revisions.
- **`verify_ch03_slides.py`**: Slide existence and resolution validator for Chapter 03.

### 4. `experimental_tests/` (Test Benches)
- **`test_cadence_variants.py`**: Compares different visual transition cadences (fast vs slow cuts).
- **`test_natural_pipeline.py`**: Prototype for end-to-end natural narration and assembly.
- **`test_pacing_rates.py`**: Tests speaker speed variations (135wpm to 160wpm).
- **`test_pts.py`**: Tests presentation timestamp (PTS) accuracy across concatenated MP4 clips.
- **`test_segment_build.py`**: Test script for segmented rendering passes.
- **`test_silence_trim.py`**: Tests leading and trailing silence trimming on voiceovers.
- **`test_split_durations.py`**: Verifies mathematics of multi-cut duration splitting.
