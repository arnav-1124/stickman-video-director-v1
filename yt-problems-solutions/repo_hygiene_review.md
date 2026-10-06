# 🧹 Repository Hygiene & Redundancy Review — for Gemini agent verification & safe action

**Requested by user:** "analyse my project see if there're any kind of redundancy or unnecessarily big files, or unnecessary files, basically whether the project is optimised or not. Write your review on this too in that file so gemini agent can read and verify everything and take safest actions."
**Date:** 2026-10-06 · **Audit method:** read-only (`du`, `find`, `git ls-files`, `git count-objects`). No files were modified.

---

## 1. Verdict

The repo holds **~1.2 GB**, of which only **~11.4 MB is git content** (820 loose objects). Your tracked source (scripts, JSON, docs) is clean and healthy. The bloat is **untracked media**: duplicate renders, superseded WAV/MP3 narration versions, versioned render folders kept inside project dirs, and browser-automation debris. Roughly **450–550 MB can be reclaimed** with zero loss of anything that contributed to a shipped video — **but the .gitignore has two traps that will undo the cleanup if not fixed first** (§5).

## 2. Measured state (2026-10-06)

| Path | Size | Files | Notes |
|---|---:|---:|---|
| `projects/` | 732 MB | 626 | ep01 alone = 481 MB (5 chapters) |
| `renders/` | 286 MB | 11 | mirrors of project renders (see D1) |
| `temp/` | 71 MB | 165 | render intermediates — gitignored |
| `productions/` | 62 MB | — | legacy longform/shorts scenes |
| `scratch/` | 16 MB | 166 | experiments — gitignored |
| `.git` | 13 MB | — | healthy, tiny |
| `assets/` | 12 MB | 28 | fine |
| scripts/pipeline/docs | <1 MB | — | fine |

## 3. Redundancy findings (ranked)

**D1 — Every final render is stored 2–3 times (~140 MB reclaimable).**
Identical files verified by size: each final exists in `projects/…/renders/` **and** `renders/…` (and Ch2/Ch3 previews exist in *three* places incl. a `_no_bgm` variant). Pairs confirmed: `YOU_REPLIED_INSTANTLY_*` V4/V3/MASTER, `ch02`+`ch03` previews ×3 copies each, `ep03`/`ep02` shorts finals ×2 each.
→ **Action (agent):** keep exactly one canonical copy per video under `renders/` (channel-level archive); delete project-dir copies *after* byte-size verification (or checksum) — and only the copies, never the canonical.

**D2 — Superseded audio versions (~60 MB reclaimable).** Ch1 audio holds 4 full WAV masters (v2 14MB, v3 15MB, v4 16MB, mastered 15MB) + matching MP3s + `ch01_master_ludo_038s` (12MB) + `google_tts/` 15MB. Only the **shipped V4** mattered. WAVs are 15–16MB each because they're uncompressed.
→ **Action (agent):** keep `ch01_master_narration_v4_with_hook.wav` + its MP3; move older versions to a dated `audio/archive/` or delete after user confirms; **do not** delete `google_tts/` word-boundary JSONs (subtitle calibration depends on them) or the `en/` directory without asking.

**D3 — Legacy duplicate of the reference video.** `DISCIPLINE-An-Animated-Short-Film_002_720p.mp4` exists at repo root **and** in `assets/references/` (6.6MB each).
→ **Action (agent):** delete the root copy, keep `assets/references/`.

**D4 — Version-litter render folders.** Project `renders/` dirs keep every superseded build (MASTER, V2, V3, V4, preview, preview_no_bgm). Historical value is zero once the final is archived.
→ **Action (agent):** after D1, adopt the rule "project renders/ holds only the current master"; archive or delete the rest. Ch2 preview (46MB) and Ch3 preview (43MB) are unpublished drafts — user decides: keep (working videos) or archive.

**D5 — `temp/` + `scratch/` = 87 MB of gitignored debris** (perfect_clips_038s 14MB, tight_clips* 24MB, v2/v3/v4 intermediates, ink_analysis 16MB).
→ **Action (agent):** safe to delete **except** `temp/yt-studio-export/` (Analytics source data — move it to `assets/analytics/` first if not already there) and anything referenced by active subtitle-calibration scripts. Verify no script hardcodes these paths before deleting (grep first).

**D6 — `productions/` legacy tree (62 MB).** Old `productions/longform/stickman/01-…` scenes carry **both** `raw_animation.mp4` and `scene_XX_final.mp4` per scene; the raw files are intermediates. The Shorts diagnosis (§5) already documented this channel-model pivot.
→ **Action (agent):** propose to user: archive whole `productions/` tree to cold storage (external drive/cloud) — it's legacy format. Do not delete without explicit approval.

**D7 — Gitignore has no render extensions for video masters.** Already covered: `*.mp4` etc. are ignored (good). **But see the traps in §5 before acting.**

**NOT problems:** `assets/` (12MB incl. branding/fonts/BGM — all justified), `.git` (13MB, healthy), scripts/pipeline/docs/instructions (tiny), `.env` properly ignored.

## 4. Code-level redundancies (minor, safe)
- `pipeline/build_hindi_final.py`, `build_natural_hindi_no_subs.py`, `generate_hindi_samples.py` — Hindi workflow was abandoned (generation rule: "English only"). Keep but mark deprecated in a README note, or move to `scripts/legacy/` — user's call.
- `scripts/chapter_audits/` has ~8 one-off ch01/ch02/ch03 audit scripts; after ep01 ships they're historical. Move to `scripts/legacy/` (do NOT delete — they document methodology).
- `pipeline/__pycache__/` + `scripts/**/__pycache__/` — ignored by git; safe to delete anytime (regenerates).
- Root-level `DISCIPLINE…mp4` → D3.

## 5. ⚠️ Gitignore traps the agent MUST handle first

```
*.jpg / *.png are globally ignored, with exceptions:
  !assets/branding/channel_logo.png
  !**/thumbnail.jpg
  !**/thumbnails/*.jpg
```
1. **Slide files are invisible to git.** `slides/slide_01.jpg` etc. are NOT tracked. If a disk failure hits, your slides are gone forever (Flow generations are not re-downloadable). Same for `master_assets/`, subtitle `.ass` files are text so they ARE tracked.
→ **Recommended fix (ask user):** add explicit exception `!projects/**/slides/*.jpg` + `!projects/**/master_assets/*` and `git add` them (~24MB for ep01 — acceptable for irreplaceable AI-generated assets). Alternative: keep ignoring them but back up `projects/**/slides` + `master_assets` to cloud/external on a schedule.
2. `!assets/fonts/*.ttf` is listed but no `assets/fonts/` dir exists (dead rule, harmless).
3. `temp/` and `scratch/` ignored (good) — but remember D5's exception: the Studio export must survive.

## 6. Safe-action protocol for the Gemini agent
1. **Order matters:** gitignore fixes (§5) → verification (checksums) → D1 dedupe → D2 audio → D3 → D5 → D4/D6 only with user approval.
2. **Never delete:** anything inside an active chapter folder without a dated archive copy first; `google_tts/` boundary JSONs; `.env`; anything matching the shipped-video chain (V4 WAV/MP3, V4 MP4, its thumbnail, publishing kit, `slides/`, `storyboard.json`, manifests).
3. **Checksum before every dedupe** (`certutil -hashfile <file> MD5` or `sha256sum`): only delete a "duplicate" if hashes match AND the canonical copy exists.
4. **Move-don't-delete** for anything with historical value (`productions/`, old audits, superseded audio) — destination: `_archive/2026-10/` at repo root or external drive, then let user purge.
5. **Report after each batch:** freed MB + exact list of what moved/deleted, appended to this file under "Cleanup log".
6. When in doubt: **ask the user**. Nothing here is urgent enough to risk a shipped asset.

## 7. Cleanup log (append-only)
*(no actions taken yet — audit only)*
