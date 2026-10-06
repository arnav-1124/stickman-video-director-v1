# ⚙️ Automation Roadmap — killing the manual work

**User pain (verbatim):** "currently I've no automation, I've to work a lot manually like generating slides, saving with naming conventions, etc."
**Date:** 2026-10-06

---

## 1. What already exists (verified in repo) — you have more automation than you think

| Capability | Script | Status |
|---|---|---|
| Episode scaffolding | `pipeline/new_episode.py --name X` | ✅ Works (copies canonical template, sets project_id) |
| Status tracking | `pipeline/automate_pipeline.py --init-status` | ✅ Works (creates `status.json` cut tracker) |
| **Slide ingestion + naming** | `pipeline/automate_pipeline.py --ingest-slides` | ⚠️ **Exists but likely broken for you** — writes `slide_NN.png`, while ep01 slides are `.jpg`; downloads from Flow arrive as random names and it relies on Downloads-folder mtime ordering |
| Voiceover TTS | `pipeline/generate_gemini_tts.py`, `generate_audio.py` | ✅ Works — `GEMINI_API_KEY` verified present in `.env`, `google-genai` SDK installed |
| Subtitles | `pipeline/generate_subtitles.py` + calibrate scripts | ✅ Works (ep01 shipped 5 subtitle iterations) |
| Final assembly | `pipeline/build_video.py` + `build_manifest.json` | ✅ Works (4 rendered ep01 versions prove it) |
| Flow browser automation | `scripts/flow_browser_automation/` (CDP controller, prompt trigger, batch downloader) | ⚠️ Exists but unwired into the main flow — this is the missing link |

**Root cause of the manual pain:** the *generation* step (Flow) and the *naming* step (slides) are automated on paper but broke in practice (`.png` vs `.jpg` mismatch, Downloads-folder race conditions), so the workflow silently regressed to copy-paste-36-prompts-and-rename-by-hand. Evidence: `quick_batch_copypaste.txt` is a 119-line hand-copied prompt sheet.

## 2. Verified environment (no guessing)
- `GEMINI_API_KEY` present in `.env` ✅
- `google-genai` SDK installed, Python 3.14.2 ✅
- Antigravity + Flow Pro subscriptions (browser UI generation); no local AI ❌
- Existing CDP browser-automation experiments in `scripts/flow_browser_automation/`

## 3. The 6 manual steps to automate (ranked by hours saved)

### A. Fix slide ingest (30 min, highest ROI)
Repair `ingest_slides` in `pipeline/automate_pipeline.py`:
1. Accept `.jpg`/`.jpeg`/`.webp`/`.png` output naming per project config (not hardcoded `.png`).
2. Sort by file *creation* time with a collision-safe rename; never trust mtime alone on copied files.
3. Dry-run mode (`--dry-run` prints the rename map) so a bad sort never overwrites good slides.
4. Delete-after-copy option once verified.
**Acceptance:** drop 37 Flow downloads into Downloads → one command → correctly named `slides/slide_01.jpg…slide_37.jpg` with a printed manifest.

### B. Generate slide prompts from the script (1 hour)
You already have `generate_all_slide_prompts.py` and `storyboard.json`. Extend so one command reads `script_upgraded.txt` + `storyboard.json` → writes `quick_batch_copypaste.txt` **and** a machine-readable `prompts.json` (the copypaste sheet is the fallback, not the primary).

### C. Wire Flow automation end-to-end (2–3 hours, the big one)
Finish the job `scripts/flow_browser_automation/` started:
- CDP controller opens Flow, iterates `prompts.json`, submits each prompt, waits for render, downloads, and feeds results straight into the fixed ingest from step A with the right name **at download time**.
- Resume support: a local `generation_state.json` tracks which slide indexes are done so a crashed run continues where it stopped.
- Fallback: if CDP breaks after a Flow UI update, the copypaste sheet + ingest command still works (degrade gracefully, never hard-block).
- This runs alongside you (browser is visible); it is not headless black-box automation.

### D. One-command audio + subs + build (already 90% done)
Chain the existing scripts into `pipeline/make_episode.py --project X --from-audio`: TTS → word boundaries → subtitles → manifest → `build_video.py`. Each stage already works standalone; this is glue code + stage-skip flags for re-runs.

### E. Thumbnail variant batch (30 min)
Script to batch 3–4 thumbnail candidates via Gemini image gen (free AI Studio tier) directly into `thumbnails/` with naming conventions (`thumb_A_<concept>.jpg`), ready for the `thumbnail-critic` skill and Studio Test & Compare.

### F. Publishing kit generation (already templated)
`youtube_publishing_kit.md`/`.json` generation is rule-driven — make the publisher skill emit both files automatically from the manifest (title/description/tags/pinned comment) instead of hand-editing per episode.

## 4. Suggested agent work order (for the Gemini agent)
1. Step A (ingest fix) — safe, isolated, testable on a copy of ep01 slides.
2. Step D (make_episode glue) — pure orchestration of proven scripts.
3. Step B (prompts.json pipeline).
4. Step C (Flow CDP loop) — build LAST, behind a feature flag, after A–C make the manual path fast. Test with 2 prompts before a 37-slide run.
5. Steps E–F in parallel whenever convenient.

**Rule for the agent:** never modify files inside an active episode folder without a backup copy first; add `--dry-run` to every script that moves, renames, or overwrites; keep all existing CLI flags working (backwards compatibility).

## 5. What this buys you
Per long-form chapter: from an estimated 2–3 hours of copy-paste/rename/sync drudgery down to ~15 minutes of supervision. That is what makes the 2–3 chapters/week cadence from the gap analysis physically sustainable for one person.
