# 🎬 Animation Strategy — Static slides vs animated videos

**Question asked:** "Should I move to animated videos instead of static slides, since Ink Explainer also uses static slides?"
**Date:** 2026-10-06
**Verdict:** **No full switch. Hybrid:** keep static ink panels as the base, add micro-motion to every slide, and generate 3–5 animated "money shots" per long-form. **Density of new visuals matters more than motion within visuals — and motion still raises the outlier ceiling.**

---

## 1. What the evidence actually shows

### Ink Explainer: static images, but NOT static video
From ShortFast's stick-figure style breakdown (Sep 2026) — the same style family as Ink Explainer:
- Default pace: **a new drawing every 2–4 seconds** (15–30 drawings per 60s short); "calm explainer" pace changes visuals every ~5s.
- Direct quote: *"At the fast pace a new visual appears every two to four seconds… That density is what stops a simple style from feeling static."*
- The plain style works because attention goes to the idea; a small posture/expression change reads instantly.

**Your Ch1 benchmark:** 37 slides over 2:47 ≈ **one new visual every 4.5s**. That is already inside Ink Explainer's calm band — but each of your slides is a hard-still frame, while theirs ship with motion/animation options layered on. You are at the density floor, not below it.

### Day One Films: fully animated, original sound
*"Every frame, sound and note of music in this film was made from scratch."* Their DISCIPLINE outlier (825K) sits in a lane where every winner (Lofi Cinema's "The Real Worth" 2.7M, etc.) is genuinely moving animation. Their visual *style* is also simple — the difference is motion, pacing, and sound design.

### Your own data
- Once viewers stay, your stories hold (88.15% APV on one Short). The leak is first-seconds packaging — **fix that before spending cycles on animation**.
- Views correlate −0.23 with APV in your 8-Short dataset: making the middle better doesn't buy reach; the first 2 seconds and the click do.

---

## 2. The cost/benefit under your constraints

| Path | Cost (you: Antigravity + Flow Pro only, no local AI) | Expected payoff | Risk |
|---|---|---|---|
| **Keep pure static slides** | Zero | Retention ceiling stays low vs long-form peers; "slideshow" perception | Ch2 underperforms like Ch1 |
| **Micro-motion on every slide** (Ken Burns pan/zoom, parallax 2–3 layers, breathing, blink/smile on faces, SFX per cut) | FFmpeg only — pipeline already renders via FFmpeg; no new paid tool | Removes the "slideshow" feel for near-zero cost. This is the minimum bar | Almost none; do it now |
| **3–5 animated money shots per video** (Flow/Veo clips, 2–4s, at emotional peaks: the 2AM stare, the pedestal collapse, the casino lever pull) | Flow Pro credits you already pay for | Matches Day One's feel at the moments retention is won/lost; ~10–20% of runtime | Credit budget; style drift — prompt-armor needed |
| **Full animation switch** (everything generated/moving) | Highest credit burn + heaviest QC + morph-control problems | Diminishing returns: viewers can't tell 50% vs 100% motion, only "does it feel alive" | Breaks your zero-morph rule; slowest cadence; you'd ship 1/week instead of 2–3/week — cadence is the bigger lever |

**Why not full animation:** Day One shipped 7 films in 9 days — volume fed the algorithm that found their outlier. Full animation would cut your cadence, and cadence is your weakest metric (9 Shorts then silence; 1 long-form alone). A motion-heavy pipeline that ships half as often loses more than it gains.

---

## 3. Phased plan (fold into production_standards.json when approved)

**Phase 0 — fix packaging first (today, free):** thumbnail + title + disclosure + description (see gap-analysis §3 Option A). Animation cannot save a video nobody clicks.

**Phase 1 — micro-motion everywhere (Ch2 onward, FFmpeg-only):**
1. Every slide gets motion for its full duration: slow zoom 1.0→1.06, or lateral pan; alternate direction per slide to avoid predictability.
2. Two-layer parallax on foreground character vs background where the slide permits.
3. SFX from `assets/sfx/` on every cut (pen scratch, whoosh, thud) — you already have the library.
4. Implement once in `pipeline/build_video.py` as a filter chain (zoompan + overlay); no per-slide manual work.
5. Acceptance check: no still frame visible for more than 4.5s anywhere in the render.

**Phase 2 — money shots (Ch2 or Ch3 onward, Flow):**
1. Pick the 3–5 emotional-peak beats per script (the hook moment, the lowest point, the turn, the payoff).
2. Generate 2–4s clips in Flow at your existing 16:9 ink style; static-slide style anchor must match (`nano_banana_prompts.md` conventions).
3. QC gate: no morphing, no character redesign mid-clip (your Iterative Visual Review standard applies — 3–4 candidates, zero compromise).
4. Budget: if credits run short, money shots go in the first 30 seconds and the final 30 seconds only — those are where browse retention is decided.

**Phase 3 — re-evaluate at 10 long-forms:** if CTR ≥4% and APV still <50%, extend money shots to 8–10 per video before touching full animation.

---

## 4. What NOT to do
- ❌ Do not switch niches to "fully animated cartoon stories" — your ink identity + Ludo voice is the brand.
- ❌ Do not add motion by re-generating every slide as video (credit burn, QC explosion).
- ❌ Do not let motion replace the cold-open fix: frame 1 must still show the title promise within 1.5s (`.agents/rules/narrative_persona_and_hook_rule.md`).
- ❌ Do not buy new paid tools for this — FFmpeg + your existing Flow Pro covers Phases 1–2.
