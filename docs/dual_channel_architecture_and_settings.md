# Dual-Channel Master Architecture & YouTube Studio Setup

---

## 🏛️ Part 1: Channel 2 (`Stone Age Tales`) Complete YouTube Studio Settings

Open **YouTube Studio** (`studio.youtube.com`) for the new channel and apply the following settings across the tabs:

---

### 1. Customization → Basic Info Tab

#### Channel Name
```text
Stone Age Tales
```

#### Handle
```text
@StoneAgeTales112
```
*(If taken, use `@StoneAgeTalesOfficial` or `@StoneAgeTales`)*

#### Channel Description (About Section)
*Copy and paste directly into the **Description** box:*

```text
40,000 years ago, our ancestors survived freezing ice ages, lethal predators, and near-extinction—not because they had sharp claws, but because of what happened inside their minds.

Stone Age Tales explores the untold, mind-bending stories of human evolution, prehistoric survival, and how our ancient ancestors accidentally invented the world we live in today.

From the very first lie ever told, to how humans first fell in love, to the bizarre rituals ancient tribes used to survive the dark.

Every video is grounded in real evolutionary anthropology, archaeological discoveries, and peer-reviewed science—brought to life through minimal 2D comic animation.

Subscribe to uncover how the Stone Age still lives inside you.
```

---

### 2. Customization → Branding Tab

Upload the two pre-built, calibrated master files:

* **Picture (Profile):**  
  Upload 👉 [`assets/branding/stone_age_tales/profile_picture_800x800.png`](file:///f:/Arnav%20-%20YT/stickman-video-director/assets/branding/stone_age_tales/profile_picture_800x800.png)  
  *(Circular avatar of stickman caveman winking in fur pelt holding flint tool)*

* **Banner Image:**  
  Upload 👉 [`assets/branding/stone_age_tales/banner_2048x1152.jpg`](file:///f:/Arnav%20-%20YT/stickman-video-director/assets/branding/stone_age_tales/banner_2048x1152.jpg)  
  *(Bright daylight savanna with prehistoric tribe, stalking leopard, acacia monkey, soaring hawk, and Canary Gold "STONE AGE TALES • SUBSCRIBE & LIKE •")*

---

### 3. Settings ⚙️ (Bottom Left) → Channel Tab

#### Basic Info → Keywords (Channel Tags)
*Copy and paste this entire block directly into the **Keywords** box (this trains the YouTube algorithm to recommend your videos alongside Kurzgesagt, Stefan Milo, and anthropology documentaries):*

```text
stone age tales, ancient humans, human evolution, prehistoric humans, anthropology, early humans, homo sapiens, neanderthals, evolutionary biology, stone age documentary, ice age, ancient history, animated documentary, human origins, evolutionary psychology, archaeological discoveries, paleolithic, prehistoric survival, cognitive revolution
```

#### Advanced Settings Tab
* **Audience:** Select **`No, set this channel as not made for kids`**  
  *(CRITICAL: Do NOT choose "Yes". Selecting "No" enables comments, bell notifications, end cards, and recommends your video to teenagers and adults).*
* **Google Ads account linking:** Leave empty.
* **Automatic captions:** Check `Don't show potentially inappropriate words`.
* **Clips:** Check `Allow viewers to clip my content`.

---

### 4. Settings ⚙️ → Upload Defaults Tab

Set this once so every future upload automatically pre-fills with your boilerplate and social links.

#### Basic Info → Description Boilerplate:
```text
🔔 Subscribe to Stone Age Tales for weekly animated stories on human evolution and ancient survival: https://www.youtube.com/@StoneAgeTales112?sub_confirmation=1

---------------------------------------------------
📚 SCIENTIFIC RESEARCH & SOURCES:
[SOURCES_INSERT_HERE]
---------------------------------------------------

#AncientHumans #HumanEvolution #StoneAgeTales #Anthropology #AnimatedDocumentary
```

#### Visibility:
* Set to **`Unlisted`** by default *(Best practice: Upload as Unlisted, wait 20-30 minutes for HD/4K processing and copyright check to complete, then switch to Public at scheduled peak hour)*.

#### Basic Info → Default Tags:
```text
stone age tales, ancient humans, human evolution, prehistoric humans, anthropology, early humans, homo sapiens, animated documentary, evolutionary psychology
```

#### Advanced Settings Tab:
* **Category:** Select **`Education`** (or **`Film & Animation`**). `Education` is recommended as anthropology and science algorithms prioritize educational classification.
* **Video language:** `English`.
* **Title and description language:** `English`.
* **Caption certification:** `None`.
* **Comments:** `On` (with `Hold potentially inappropriate comments for review`).

---

## 📁 Part 2: Proposed Multi-Channel Folder Architecture

To allow this workspace to smoothly serve **both channels simultaneously** without mixing up characters, voiceovers, or metadata, we transition to a channel-scoped hierarchy:

```
f:\Arnav - YT\stickman-video-director\
│
├── channels/
│   ├── sticky_in_dark/                        # CHANNEL 1: DARK PSYCHOLOGY & MINDSET
│   │   ├── branding/                          # PFP, Banner, Watermarks
│   │   ├── channel_settings.md                # Keywords, descriptions, niche rules
│   │   ├── shorts/                            # High-velocity 9:16 Shorts
│   │   │   ├── s01_when_someone_insults_you/
│   │   │   ├── s02_the_pull/
│   │   │   └── s03_texting_anxiety/
│   │   └── long/                              # Long-form psychological deep dives
│   │
│   └── stone_age_tales/                       # CHANNEL 2: ANTHROPOLOGY & HUMAN EVOLUTION
│       ├── branding/                          # Profile picture & 2048x1152 banner
│       │   ├── profile_picture_800x800.png
│       │   └── banner_2048x1152.jpg
│       ├── channel_settings.md                # Copy of this setup kit
│       ├── master_assets/                     # Permanent character & environment library
│       │   ├── characters/ (Grog, Tribe Elder, Tribe Hunter)
│       │   ├── environments/ (Savanna Day, Cave Fire, Ridge)
│       │   └── animals/ (Leopard, Monkey, Hawk, Lion)
│       ├── episodes/                          # 5-minute animated short films
│       │   ├── ep01_how_humans_invented_the_first_lie/
│       │   ├── ep02_how_humans_first_fell_in_love/
│       │   └── ep03_why_ancient_humans_painted_caves/
│       └── shorts/                            # Funneling shorts (clips from episodes)
│
├── pipeline/                                  # SHARED AUTOMATION ENGINE (Tools work for both)
│   ├── synthesize_voiceover.py                # 164 WPM voiceover with micro-pause tuning
│   ├── build_stone_age_banner.py              # Automated banner generator
│   └── render_film.py                         # FFmpeg video stitcher & audio master (-11.9 LUFS)
│
└── docs/                                      # CHANNEL ROADMAPS & STANDARDS
    ├── stone_age_tales_channel_setup_kit.md
    ├── dual_channel_architecture_and_settings.md
    └── audio_cadence_and_pause_standards.md
```

### Migration Plan (Safe & Non-Destructive):
1. **Existing Ep02** (`ep02_how_humans_invented_the_first_lie`) becomes **Episode 01 of Stone Age Tales** (Video #1).
2. **Current Ep03** (`ep03_how_humans_first_fell_in_love`) becomes **Episode 02 of Stone Age Tales** (Video #2).
3. **Existing Shorts** stay in `channels/sticky_in_dark/shorts/` where they belong to keep the mindset/psychology audience thriving.
4. Shared scripts in `pipeline/` remain universal so we don't duplicate code.

---

## 🚀 Part 3: Video #1 Launch Details (Stone Age Tales Flagship)

When you are ready to upload the first video to the new channel, use these exact files and metadata:

* **Video File (1080p Master):**  
  👉 [`renders/long/ep02_how_humans_invented_the_first_lie/HOW_HUMANS_INVENTED_THE_FIRST_LIE_MASTER.mp4`](file:///f:/Arnav%20-%20YT/stickman-video-director/renders/long/ep02_how_humans_invented_the_first_lie/HOW_HUMANS_INVENTED_THE_FIRST_LIE_MASTER.mp4)

* **Thumbnail:**  
  👉 [`renders/long/ep02_how_humans_invented_the_first_lie/HOW_HUMANS_INVENTED_THE_FIRST_LIE_THUMBNAIL.jpg`](file:///f:/Arnav%20-%20YT/stickman-video-director/renders/long/ep02_how_humans_invented_the_first_lie/HOW_HUMANS_INVENTED_THE_FIRST_LIE_THUMBNAIL.jpg)

* **Title:**  
  ```text
  The Day Ancient Humans Invented The First Lie
  ```

* **Description (With Scientific Citations):**  
  ```text
  For 99% of human evolution, lying was physically impossible. If you didn’t share your meat, the tribe starved. If you ran from a predator, everyone saw you. 

  So how on Earth did a species that depended on 100% honesty accidentally invent deception? 

  In this episode of Stone Age Tales, we travel back two million years to the African savanna to uncover the cognitive revolution, the Machiavellian Intelligence Hypothesis, and the exact biological moment a human first withheld the truth.

  🔔 Subscribe to Stone Age Tales for weekly animated stories on human evolution and ancient survival: https://www.youtube.com/@StoneAgeTales112?sub_confirmation=1

  ---------------------------------------------------
  📚 SCIENTIFIC RESEARCH & SOURCES:
  • Byrne, R. W., & Whiten, A. (1988). "Machiavellian Intelligence: Social Expertise and the Evolution of Intellect in Monkeys, Apes, and Humans." Oxford University Press.
  • Dunbar, R. I. (1998). "The Social Brain Hypothesis." Evolutionary Anthropology: Issues, News, and Reviews.
  • Trivers, R. (2011). "The Folly of Fools: The Logic of Deceit and Self-Deception in Human Life." Basic Books.
  • Tomasello, M. (2014). "A Natural History of Human Thinking." Harvard University Press.
  ---------------------------------------------------

  #AncientHumans #HumanEvolution #StoneAgeTales #Anthropology #AnimatedDocumentary
  ```

* **Video Tags:**  
  ```text
  how humans invented lying, ancient humans, the first lie, human evolution, prehistoric humans, stone age tales, anthropology, evolutionary psychology, homo sapiens, early humans, machiavellian intelligence, social brain hypothesis, history animation, evolutionary biology
  ```
