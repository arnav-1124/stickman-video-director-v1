# 📋 AGENT HANDOFF — Sticky in dark Channel Growth

**Purpose:** Single source of truth for any agent working on this channel. Read this first, then the linked evidence docs. **Update this file after every decision or upload** (protocol in §7).
**Last updated:** 2026-10-06 (post-audit implementation) — Gitignore trap resolved, slide ingestion upgraded, master orchestrator built, 5 custom skills deployed, competitor RSS watch script active, superseded audio archived, temp debris cleaned.

---

## 1. Doc map (read in this order)

| Doc | Contents |
|---|---|
| `AGENT_HANDOFF.md` (this file) | Channel state, confirmed findings, decision log, open decisions, update protocol |
| `longform-chapter1-gap-analysis.md` | Evidence-backed audit of Chapter 1 long-form: 7 gaps ranked, Day One Films + Ink Explainer live data, 3 strategy options (A/B/C) |
| `yt-shorts-diagnosis.md` | Earlier Shorts-only audit (8 Shorts, Sep data): tags/hashtags exonerated, cold-open + packaging + zero compounding identified |
| `animation_strategy.md` | Static slides vs animated videos verdict with evidence, and the phased hybrid plan |
| `free_toolkit_and_skills.md` | Free tools, agent-skill packs, and custom skills to boost output under the user's tooling constraints |
| `automation_roadmap.md` | How to kill the manual slide-generation/naming/assembly work; 6 ranked steps, work order for the agent |
| `repo_hygiene_review.md` | Measured redundancy/bloat audit (~450–550MB reclaimable), gitignore traps, and the safe-action protocol for cleanup |

---

## 2. Channel snapshot (verified live 2026-10-06)

- **Handle:** `@stickyindark` (display: "Sticky in dark") — 30 subs, 10 videos (1 long-form + 9 Shorts)
- **Chapter 1 long-form:** `watch?v=-cmdUUguiBs` — `YOU REPLIED INSTANTLY | An Animated Short Film (Chapter 1)` — **139 views / 21h**, 3 likes. Watch page shows **"Made with AI"** disclosure label.
- **Top Shorts (views on Oct 6):** Free Attention 1.3K · Insults In Public 1.2K · Silent Boy 1K · then 285–548 range
- **Studio export (Sep 6–Oct 3, in `assets/analytics/yt-studio-export-direct/`):** 2,268 engaged views, 1,929 unique viewers, **4 returning viewers**, 24 subs, 5.63% avg CTR, 45.42% stayed-to-watch. Per-video CTR spread 2.48%–17.93%.
- **Pipeline:** static 2D ink panels (37 slides for Ch1 ≈ one new visual per 4.5s), Google Gemini TTS "Ludo", ASS karaoke subs, FFmpeg assembly. Rules in `.agents/rules/`, publishing skill in `.agents/skills/youtube-publisher/SKILL.md`.
- **User tooling constraints (hard):** Antigravity (Pro) + Google Flow (Pro) are the ONLY paid tools; no other subscriptions; **no local AI execution possible**. All tool recommendations must be free web services or already-covered plan features. See `free_toolkit_and_skills.md`.
- **User automation pain (verbatim):** "currently I've no automation, I've to work a lot manually like generating slides, saving with naming conventions, etc." → roadmap in `automation_roadmap.md`. Verified: `GEMINI_API_KEY` in `.env`, `google-genai` installed, Python 3.14.2 — API-driven generation is feasible.

---

## 3. Confirmed findings (do not re-litigate without new data)

1. **Tags & hashtags are NOT the problem.** Two independent audits (Shorts CSV + live Ch1 metadata) show identical tag practice on best and worst performers. Best CTR video used only `#shorts`; worst used 3 hashtags. Spend zero time here.
2. **Story/retention is NOT the core problem.** 88.15% APV on one Short proves stories hold once viewers stay. The leak is the **first 2 seconds** (~55% swipe away) and **packaging** (CTR 2.48%–17.93% spread).
3. **Labels (Alpha/Sigma/Dark Psychology) kill CTR** — worst title got the 2nd-most impressions and worst CTR. Already banned in `.agents/rules/narrative_persona_and_hook_rule.md`; keep it banned.
4. **Day One Films is not luck:** channel created Sep 27 2026; DISCIPLINE = 825K (a ~1% outlier), other 6 videos 15K–27K; 7 films in 9 days; fully animated with original sound/music; thumbnail formula = giant expressive face + 1 red prop + 2 huge hand-drawn words.
5. **Ink Explainer is not "static slides win" proof of long holds:** they change the drawing every ~2–4s (fast) / ~5s (calm) — density, not motion, is their trick. 115K subs, 17 videos, 10M outlier; 11 of 17 videos below 230K. Lane now flooded with clones.
6. **Packaging gaps on Ch1** (details + fixes in gap-analysis doc): thumbnail unreadable at feed size (no face, tiny text), title dropped the approved "Problem?" curiosity gap, "(Chapter 1)" is a dead-end promise until Ch2 exists, AI disclosure showing publicly, description sells mechanism instead of story, static panels with zero micro-motion, no Related-Video funnel from Shorts.

---

## 4. Strategy on the table (from gap-analysis §3)

- **Option A (recommended, active):** Fix Ch1 packaging (thumbnail Day One-style, retitle `YOU REPLIED INSTANTLY. Problem? | An Animated Short Film`, review AI disclosure, story-first description) → ship Ch2 "Casino Effect" in 3–4 days → add micro-motion → 2–3 long-forms/week + 1 Short/day as trailers linked via Related Video. Gate: CTR ≥4%, APV ≥50%, returning viewers >25/week by week 4.
- **Option B (proposed, needs user decision):** "Old Brain, New World" repositioning — merge psychology niche with Ink Explainer's curiosity-question machine (split-frame stone-age vs modern thumbnails; titles like "Why Your Brain Panics When Nobody Texts Back"). Start with video 2–3.
- **Option C (parallel):** Generated motion clips (Hailuo/Kling/Flow — pipeline already exports prompts) for 3–5 emotional-peak shots per video from Ch3 onward. See `animation_strategy.md` for the full verdict.

---

## 5. Decision log (append-only — newest first)

| Date | Decision | Rationale | Status |
|---|---|---|---|
| 2026-10-06 | Chapter 02 V3 Cinematic Master rendered (67 shots, 2-4s density, Ken Burns, acoustic sub sync) | Solved static slide lag (67 shots, max 3.8s hold), applied OpenCV bicubic Ken Burns with cosine easing, and locked 498 acoustic word-level karaoke subtitle events | ✅ Implemented |
| 2026-10-06 | 5 Production Laws locked: C2PA stripping, 0.35s pauses, 2-4s density, Ken Burns motion, acoustic subs | Eradicated 0dB C2PA screech, eliminated 9.8s dead air, enforced 1:1 clause-to-visual density floor, banned static stills, banned uniform word math | ✅ Locked in Docs |
| 2026-10-06 | 5 custom skills scaffolded + `scripts/competitor_watch.py` live | Deployed `thumbnail-critic`, `packaging-auditor`, `title-lab`, `retention-doctor`, `cadence-keeper`; competitor RSS pull active (22 videos parsed) | ✅ Implemented |
| 2026-10-06 | Pipeline automation upgraded: Ingestion fixed + `pipeline/make_episode.py` master orchestrator built | Solved manual naming/ingest pain: `.jpg` support, creation-time sorting, `--dry-run`; unified episode builder | ✅ Implemented |
| 2026-10-06 | Repo hygiene safe batches executed (D3, D2, D5) + legacy script isolation | Deleted root duplicate reference video (hash verified); moved 74.9MB superseded audio to `audio/_archive/`; cleaned 55.5MB temp intermediates; moved Hindi & audit scripts to `scripts/legacy/` | ✅ Implemented |
| 2026-10-06 | Gitignore trap resolved: slides & master assets whitelisted | Added `!projects/**/slides/*.jpg` and `!projects/**/master_assets/*` so irreplaceable AI art is tracked safely | ✅ Implemented |
| 2026-10-06 | Tooling locked: Antigravity Pro + Flow Pro only, no local AI | User constraint; all future tool/skill recommendations must respect `free_toolkit_and_skills.md` | ✅ Confirmed |
| 2026-10-06 | Stop optimizing tags/hashtags entirely | Exonerated by two audits | ✅ Confirmed |
| 2026-10-06 | Do NOT clone ancient-humans niche; propose "Old Brain, New World" merge instead | Lane flooded with clones; psychology voice/pipeline is the moat | ✅ Confirmed — launch for Ch3+ |
| 2026-10-06 | Static base + micro-motion everywhere + 3–5 animated "money shots" per long-form | Ink Explainer proves density>motion; Day One proves motion raises outlier ceiling; hybrid is cheapest path to both | ✅ Approved |

---

## 6. Open actions & Studio user tasks

### 👤 User Manual Actions in YouTube Studio (To do now):
1. **Retitle Chapter 1:** Update title to `YOU REPLIED INSTANTLY. Problem? | An Animated Short Film` (restores curiosity gap).
2. **Review AI Disclosure (Watch Page):** In Video Details $\to$ Altered Content, untick "Yes" if checked unnecessarily (stylized 2D stickman animation does not legally require an altered content viewer badge).
3. **Thumbnail Test & Compare:** In Studio, set up an A/B test comparing current bedroom shot against a close-up face candidate ("3 SECONDS." / "LEFT ON READ.").
4. **Link 9 Shorts to Chapter 1:** For each of your 9 published Shorts, edit details $\to$ set **"Related video"** $\to$ select Chapter 1 (`watch?v=-cmdUUguiBs`).

### 🤖 Agent Next Steps (For Chapter 02 Production):
1. Apply the new `pipeline/make_episode.py` and `pipeline/automate_pipeline.py` workflow to Chapter 02 ("The Casino Effect").
2. Run `thumbnail-critic` and `packaging-auditor` pre-flight checks before final render.

---

## 7. Update protocol for the next agent

1. **After every user decision:** add a row to §5 (date, decision, rationale, status) and delete the item from §6 if resolved. Update `Last updated` line.
2. **After every upload:** append to a new "Upload log" row — video, publish date, 48h CTR/stay/APV, 7-day views. Pull from Studio export; never from public counts alone (public views lag and round).
3. **Never overwrite history** in the evidence docs — append dated sections. If a finding is overturned, add a dated correction note; don't delete the original.
4. **Metrics that matter weekly:** CTR (≥4% target), stayed-to-watch (≥55% target), returning viewers (compounding), impressions per video. **Ignore APV as a growth predictor** (correlates −0.23 with views in this channel's own data).
5. **Keep evidence links alive:** re-verify live figures (Social Blade / RSS / channel pages) before citing them in new decisions; view counts drift daily.
6. Respect the existing pipeline rules in `.agents/rules/` — they encode prior decisions; change them only when the user decides.

---

## 8. Permanent Production Laws (Established 2026-10-06)

1. **Law of C2PA SynthID Stripping (Zero Digital Screech):**
   - Google Gemini TTS automatically embeds a 6,070-byte C2PA SynthID binary watermark box (`b'C2PA...'`) at the very end of inline audio streams.
   - Any script converting or concatenating Gemini TTS audio MUST slice the raw audio bytes before `raw.find(b'C2PA')`.
   - Never use FFmpeg `-f concat -c copy` on `.wav` files. Always concatenate decoded PCM frames natively with 15ms zero-crossing micro-crossfades.

2. **Law of Calibrated Cadence (0.35s Anti-Dead Air):**
   - Raw TTS outputs include 0.75s–1.0s pauses at sentence and paragraph boundaries.
   - Any vocal silence $>0.38\text{s}$ must be smoothly compressed down to exactly **0.35s** with cosine crossfades.
   - Preserves natural, unhurried breathing rhythm while eliminating ~10s of retention-killing dead air per episode.

3. **Law of Visual Density (2–4 Second Rule):**
   - No single static slide may ever stay on screen for longer than **3.8 seconds** (Ink Explainer / Day One standard).
   - Long-form episodes target **one visual cut every 2.0 to 3.2 seconds** (~55–68 visual shots per 3-minute video).
   - Achieved via:
     - 1:1 Narrative clause allocation (no lumping multiple distinct thoughts into one slide).
     - Multi-angle cinematic cuts on 2752x1536 master slides (Wide 1.0x $\rightarrow$ Close-Up Punch-in 1.35x on dials/characters).
     - High-impact hand-inked concept punch cards and diagrams on textured paper (`#FAF9F6`).

4. **Law of Purposeful Cinematic Ken Burns Motion:**
   - Pure static slides are strictly forbidden.
   - Camera motion must NEVER be randomized; it must follow deep narrative psychological intent:
     - `SLOW_PUSH` (1.00 $\rightarrow$ 1.08) for gradual audience focus.
     - `CREEPING_PULL_IN` (1.05 $\rightarrow$ 1.15) for rising psychological tension / anticipation.
     - `PULL_OUT_WIDE` (1.12 $\rightarrow$ 1.00) for reveals of emptiness, solitude, or boredom.
     - `TRACK_PAN` (horizontal drift across reels, dials, or crowds).
     - `PUNCH_IN_DETAIL` (1.28 $\rightarrow$ 1.35) for sudden punchlines and reveals.
   - Rendered using OpenCV bicubic sub-pixel interpolation (`cv2.INTER_CUBIC`) and smooth cosine ease-in/ease-out curves (zero linear robotic jitter).

5. **Law of Acoustic Word-Level Subtitle Alignment:**
   - Linear duration splitting (`sp_dur / len(words)`) is strictly banned.
   - Subtitles must be generated using acoustic word-level timestamps (`gemini-3.5-flash-lite` acoustic alignment).
   - Every active-word karaoke pop hits on the exact millisecond the vocal cord vibrates that specific word.
