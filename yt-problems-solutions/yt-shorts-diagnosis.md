# YouTube Shorts Diagnosis — @code_animation_studio

**Compared against:** Ink Explainer (@Inkexplainer96)
**Data period:** Sep 6 – Oct 4, 2026 (8 Shorts, all published Sep 20–29)
**Sources:** YouTube Studio Content export (3 CSVs, in `temp/yt-studio-export/`), production scripts in `projects/shorts/` and `productions/shorts/`, 2026 Shorts benchmarks, public Ink Explainer data.

---

## 1. Direct answer: is it tags, hashtags, or stories?

**No — it is not tags, and it is not hashtags.** Stories are *good but leaky at the first seconds*. The real problem is **packaging (title/hook) + zero audience compounding + copying a long-form channel model into Shorts.**

| Suspect | Verdict | Evidence |
|---|---|---|
| **Tags** | Not the cause | You already ship a deliberate 462-char tag block (`publishing-kit.md`). Best and worst videos use identical tag practice — tags cannot explain a **7.2x CTR spread** inside one channel. |
| **Hashtags** | Not the cause | Your best-CTR video used **only `#shorts`** ("Why Girls Like The Silent Boy", 17.93%). Your worst used **`#shorts #mindset #brainhacks`** (2.48%). More hashtags → *lower* CTR in your own data. Hashtags are a weak ranking signal; stop expecting them to move views. |
| **Stories** | Partial | Retention on people who *stayed* is strong — 88.15% APV on Dark Psychology, 71.14% on 5-Second Rule. But only **45.42% stay** means ~55% swipe away in the first seconds. The story is not weak; the **cold open** is. |
| **Packaging (title → click)** | **Primary lever** | CTR runs from **2.48% to 17.93%** across your own videos. Same style, same tags, same niche. |
| **Distribution/loyalty** | **Structural ceiling** | **4 returning viewers total** out of 1,916 new. 24 subs from 2,268 views. Every video starts cold and dies in 1–4 days. |
| **Format mismatch** | **Strategic root** | Ink Explainer has **never posted a Short**. You are copying a 15-video, long-form, 1/week channel style into a feed with different rules. |

---

## 2. Your funnel, by the numbers

### Channel totals
- **2,268** engaged views · **3,841** unique reach · **1,793** thumbnail impressions
- **5.63%** CTR · **45.42%** stayed to watch · **56.44%** avg % viewed
- **1,916** new viewers · **4** returning viewers · **24** subscribers · **21.45 h** watch time

### Per video (sorted by engaged views)

| Video | Views | Impr. | CTR% | Stay% | APV% | Subs |
|---|---:|---:|---:|---:|---:|---:|
| The Hallway Rule (Sep 27) | 734 | 353 | 5.67 | **54.49** | 46.06 | 9 |
| Why Girls Like The Silent Boy (Sep 29) | 393 | 184 | **17.93** | 35.73 | 53.39 | 3 |
| The Spotlight Effect (Sep 20) | 250 | 114 | 5.26 | 48.63 | 49.55 | 4 |
| The Dark Psychology of Silence (Sep 21) | 238 | 282 | 5.67 | 47.79 | **88.15** | 2 |
| The 5-Second Rule (Sep 20) | 215 | 169 | 3.55 | 45.94 | 71.14 | 5 |
| How To Destroy An Insult (Sep 26) | 177 | 145 | 3.45 | 36.49 | 63.10 | 0 |
| Looking Rich vs Being Rich (Sep 20) | 158 | 224 | 3.13 | 50.48 | 45.92 | 3 |
| Alpha vs Sigma Quiet Student (Sep 26) | 102 | **323** | **2.48** | 38.20 | 46.85 | 0 |

### What the correlations say (8 videos)
- Views ↔ **stay-to-watch: +0.45** (strongest actionable signal)
- Views ↔ **CTR: +0.37** · Views ↔ impressions: +0.40
- Views ↔ **APV: −0.23** — high retention did **not** produce views

**Read:** YouTube gave every video a small test batch (114–353 impressions). What decided whether it earned more was **the title click + first-seconds stay**, not how good the rest of the story was.


### Decay curves (Chart data.csv)
- **The Hallway Rule:** 660 of 734 views (**90%**) on day 1 → then 7, 3, 0, 1
- **Silent Boy:** 135 → 144 → 111 → then collapse to 1, 2 (only video with a 4-day runway — because CTR was 17.93%)
- **Spotlight Effect:** 194 on day 1 → ~0 by day 3
- **Alpha vs Sigma:** 323 impressions served (2nd-most), worst CTR 2.48%, lifetime stalled at **102 views** — lowest of all 8 (its daily series is absent from the Chart export)

This is the standard Shorts test-then-stop pattern: **weak CTR/swipe → YouTube truncates the test → video is permanently capped.**

---

## 3. Ranked root causes

### #1 — Title/hook packaging: label-bait instead of curiosity questions (CTR 2.48% vs 17.93%)
Your worst-performing title — *"Why The Quiet Student Runs The Room (Alpha vs Sigma Psychology)"* — got **the 2nd-most impressions of any video (323)**, the **worst CTR (2.48%)**, and **0 subs**. YouTube showed it widely; viewers refused it. Parenthetical label-bait ("Alpha vs Sigma") reads as recycled sigma content.
Your best — *"Why Girls Like The Silent Boy"* — is a plain, specific, emotionally concrete question with no labels and only `#shorts`.

### #2 — First-seconds cold open: ~55% swipe away before the story starts
Stay-to-watch ceiling is 54.49% (your best). Story evidence from your own project files:
- **Best hook (ep03, 734 views):** opens with a *scene + paradox* — "In every hallway, ten guys stare at her. She only notices the one who didn’t."
- **Best CTR (ep04, 17.93%):** opens with a *concrete character* — "In every college lecture hall, there is one boy in the last row who never raises his hand."
- **Worst (ep02, 2.48%):** opens with an *abstract lecture* — "In psychology, the Alpha needs the hierarchy. He rules the pack…" — concept-first, no scene, no question, no "you".
- **Dark Psychology = 88.15% APV**: once people stay, your stories hold them. The leak is the first 2 seconds, not the middle.

### #3 — Zero audience compounding (4 returning viewers, 24 subs)
1,916 new viewers, **4** who watched more than one video. Two videos gained **0 subs**. Nothing in the experience tells a viewer this is a series worth coming back to, so each Short restarts from zero reach.

### #4 — Niche positioning: saturated identity-bait vs Ink Explainer open lane
Ink Explainer owns a wide-open, evergreen lane: *mundane daily life of ancient humans* ("What Did Ancient Humans Actually Do All Day?" → 7.8M). You are in **alpha/sigma/stoic psychology** — the most crowded faceless-Shorts lane, where viewers instantly pattern-match and swipe.

### #5 — Format mismatch: you are copying a long-form channel scorecard
Ink Explainer: **95K subs, 13.5M views from ~15 videos, ~1 upload/week, 20-minute videos, zero Shorts.** Their success = long-form watch time + click-driven browsing/search. Shorts = swipe feed with different packaging. The *curiosity principles* transfer; the *strategy* does not.

### #6 — Upload pattern
Three videos on Sep 20, then singles. Burst-then-sparse gives YouTube no consistent signal and no appointment-to-watch.


---

## 4. Benchmarks (2026) vs you

| Metric | 2026 benchmark | Your channel | Gap |
|---|---|---|---|
| Avg % viewed (APV) | **≥70%** healthy (humbleandbrag); 40–50% avg for 30–60s Shorts (retensis) | 56.44% | Below viral bar; above average for length |
| CTR | 2–10% typical; **>6% good**, <2% bad (vidIQ/YouTube) | 5.63% avg, median ~4.4% | Middle of pack — half your titles underperform |
| Stayed to watch | Your own best = 54.49%; majority-swipe is the common failure mode | 45.42% | ~55% of swipes lost at second 0–2 |
| Returning viewers | Should grow with every upload | **4** | No compounding at all |

---

## 5. Ink Explainer formula (what actually transfers)

**Their machine:** one question everyone has wondered about → simple stick characters → simple animation → day-in-the-life payoff.
**Title patterns (proven by their outliers):**
- "What Did Ancient Humans Actually Do All Day?" — 7.8M
- "What Did Ancient Humans Do When It Rained All Week?" — 1.5M
- "Why Are We the Only Human Species Left?" — 1.2M
- "When Did Ancient Humans Start Drinking Alcohol?" — 879K

**What transfers to you:** concrete question titles with an instantly pictureable situation; mundane/evergreen topics; no identity labels; stakes you can *see in one frame*.
**What does not:** their long-form runtime, their prehistoric niche, their weekly-long-form cadence.

### Rewrite templates for psychology Shorts (≤50 chars, `#shorts` only)
1. "What Happens When You Go Silent On Them?"
2. "Why Do You Rehearse Arguments In The Shower?"
3. "The 3AM Thought That Exposes Your Brain"
4. "Why Strangers Tell You Their Problems"
5. "What A Nervous Laugh Really Signals"
6. "Why Nobody Remembers Your Speech"

Cold-open rule (from your own winners): **frame 1 = a specific scene with a visible paradox**, line 1 spoken within 2 seconds. Never open with "In psychology…" or a label ("Alpha/Sigma").


---

## 6. 30-day test plan

**Weeks 1–2 — packaging test (change ONE thing):**
- 8–10 Shorts, **one per day** (no same-day bursts)
- Titles: **question-form, ≤50 chars, no labels, no parentheticals**, `#shorts` only (drop `#mindset #brainhacks`)
- Cold open: scene-first paradox in the first 2 seconds
- Keep animation/story style unchanged (it is not the problem)
- **Targets:** CTR >6% (from 5.63), stay-to-watch >55% (from 45.42)

**Weeks 3–4 — loyalty test:**
- Give every video an explicit series name ("Silence Rules 1/7") spoken in the first 5 s + pinned question comment (you already build these — use them for *series*, not random questions)
- Follow-up episodes to any video >500 views (ride the algorithm existing interest)
- **Targets:** returning viewers >25/week, subs >15/week

**Decision gate (day 30):**
- Median CTR ≥6% and stay ≥55% → double down, scale to 1/day
- Still stuck → **test one Ink-Explainer-style long-form** (8–12 min, e.g. "What Actually Happens In Your Brain During An Awkward Silence?") — your APV numbers prove you can hold attention; long-form is where your model actually wins

**Metrics to watch weekly (Studio → Advanced mode):** CTR, stayed-to-watch, returning viewers, impressions per video. Ignore APV as a growth predictor — in your own data it correlates **−0.23** with views.

---

## 7. Verification appendix

- All per-video figures transcribed from `Table data.csv`; totals cross-checked against `Totals.csv` (per-video rows sum to 2,267 (734+393+250+238+215+177+158+102); Totals row and daily Chart sum = 2,268 — 1-view rounding difference inside the export)
- Decay claims from `Chart data.csv` (140 rows; 5 videos had nonzero daily series in period)
- Correlations computed on the 8 video rows (Pearson r)
- Ink Explainer figures: OutlierKit (98K subs / 14.5M views / 15 videos) and ShortFast (95.1K subs / 13.5M views) — both cited, range given
- Benchmarks: humbleandbrag.com (Mar 2026), retensis.com (Apr 2026), gyre.pro/vidIQ (Jun 2026)
