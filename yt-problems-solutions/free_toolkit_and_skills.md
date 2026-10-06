# 🧰 Free Toolkit & Skills Booster — maximizing your Antigravity + Flow Pro setup

**Your constraints:** Antigravity (Pro) + Google Flow (Pro) only. No other paid tools. No local AI. Everything below is **free** and selected to plug into your existing `.agents/` pipeline.
**Date:** 2026-10-06

---

## 1. Free agent-skill packs you can install today

Your pipeline already uses the `.agents/skills/` folder format (markdown-defined personas). Skills are just folders with a `SKILL.md` — they cost nothing and transfer between agents:

| Pack | Where | What it gives your agent |
|---|---|---|
| **Anthropic official skills** | `github.com/anthropics/skills` (Apache-2.0) | Document creation, structured outputs, file handling — reference implementations of the SKILL.md format worth copying structure from |
| **Superpowers** | `github.com/obra/superpowers` | Battle-tested skills for brainstorming, planning, debugging, writing — the most-starred free skills library; several transfer directly to scriptwriting workflows |
| **awesome-claude-skills lists** | search `awesome-claude-skills` on GitHub | Curated index of free community skills — mine it monthly for new packs |

**Highest-leverage move: write your OWN skills from the findings in these docs.** They're free, they encode your decisions permanently, and any agent (this one, Antigravity, anything that reads markdown) can execute them:

1. `thumbnail-critic` — pastes a thumbnail + feed-size mockup rules; agent scores face visibility, text size at 168px width, contrast, and Day One formula compliance (face + emotion + 2–3 words + one accent color). Kill anything below threshold before upload.
2. `packaging-auditor` — takes title+thumbnail+first-3-lines; audits against the rules in `longform-chapter1-gap-analysis.md` (curiosity gap present? chapter tag justified? story-first description? AI disclosure reviewed?). Blocks upload until it passes.
3. `title-lab` — generates 5 candidate titles per video in the proven patterns (question-form ≤50 chars for Shorts; `[STATEMENT] | An Animated Short Film` for long-form), scores curiosity-gap strength, flags banned labels automatically.
4. `retention-doctor` — reads your script + slide timing; flags any stretch >4.5s without a new visual, >12s without a scene change, and verifies first spoken syllable <0.8s and frame-1 title congruence.
5. `cadence-keeper` — reads the upload log in `AGENT_HANDOFF.md` §5/§7 and nags when long-form cadence drops below 2/week or Shorts below 1/day.

*(Ask your agent to scaffold these into `.agents/skills/` following your existing `youtube-publisher/SKILL.md` format.)*

## 2. Free tools mapped to your production stages

| Stage | Free tool | Use |
|---|---|---|
| **Competitor research** | YouTube RSS feeds (`youtube.com/feeds/videos.xml?channel_id=…`) | No script exists in the repo yet — one small fetch+parse script gives weekly Day One/Ink Explainer catalog pulls into `assets/analytics/`, zero API cost |
| **Competitor research** | **YouTube Data API v3** — free 10,000 units/day | Build one small script: weekly competitor view counts + your own stats into CSVs. 10k units ≈ hundreds of catalog pulls. No paid analytics needed |
| **Outlier discovery** | ViewStats (viewstats.com) free tier, vidIQ free extension, 1of10 free tier | Spot outlier packaging in your niche before scripting |
| **Thumbnail A/B testing** | **YouTube Test & Compare** — built into Studio, free for all channels | This is your thumbnail experiments lab. Test "3 SECONDS." vs "LEFT ON READ." — never guess |
| **Thumbnail editing** | Photopea (photopea.com, browser, free) — Photoshop-grade | Fix text size/contrast on Ch1 thumbnail in 20 minutes without any AI |
| **Thumbnail fonts** | Google Fonts: `Permanent Marker`, `Bangers`, `Caveat` (your own rules already reference these) | Free, hand-drawn feel, huge at feed size |
| **Thumbnail variants** | Gemini image gen (Nano Banana) via free AI Studio tier | Batch 3–4 thumbnail candidates per the Iterative Visual Review standard |
| **Music & SFX** | YouTube Audio Library (Studio → Audio Library) | Free, copyright-safe BGM; your `assets/sfx/` gaps get filled here |
| **Motion (Phase 1)** | FFmpeg `zoompan`/`overlay` — CPU rendering, not AI, runs on any machine | The entire micro-motion plan in `animation_strategy.md` needs zero AI credits |
| **Motion (Phase 2)** | Flow Pro credits you already pay for | Only for the 3–5 money shots — don't spend credits on slides FFmpeg can move |
| **Script research** | Google AI Studio free tier (Gemini with search grounding) | Originality audits per your `creative-researcher` stage, free quota |
| **Knowledge** | Paddy Galloway & Film Booth YouTube channels (free) | The packaging/CTR/retention playbooks these docs echo, straight from the source |
| **Community data** | r/NewTubers + the free monthly YouTube Partner roundups | Benchmark sanity checks when deciding gates |

## 3. What your Pro plan already covers — stop paying attention to paid alternatives
- **Antigravity multimodal review:** your Gemini agent can *look at* thumbnails and slides — use it as the `thumbnail-critic` skill's engine (screenshot at 168px feed width, ask "can you read this? what emotion is the face showing?").
- **Flow Pro = your only video-gen budget.** Guardrail from `animation_strategy.md`: money shots at emotional peaks only; if credits run low, first/last 30 seconds get priority.
- **TTS:** Gemini TTS "Ludo" is already in your pipeline at plan-covered quota; no ElevenLabs needed.

## 4. Concrete next build (free, high ROI)
A single `scripts/competitor_watch.py` using YouTube Data API v3 (free key from Google Cloud console): weekly CSV of Day One Films + Ink Explainer + 5 emerging clones (title, views, published, thumbnail URL) appended to `assets/analytics/`. Combined with `title-lab`, your agent starts every episode with fresh, evidence-based packaging references instead of memory. Ask for it whenever you're ready.
