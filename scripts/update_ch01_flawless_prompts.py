import json
from pathlib import Path

ep_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them")
ch1_dir = ep_dir / "chapter_01_the_pedestal_paradox"

# Handcrafted, precise shot specifications for Chapter 1
ch1_updates = {
    1: {
        "title": "Chapter Title Card",
        "scene_type": "title_card",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "Centered minimalist hand-drawn title in heavy solid black ink lettering: CHAPTER 01: THE PEDESTAL PARADOX. Centered directly underneath the text, a clean horizontal slate-blue divider line (#2563EB) stretching across the frame. Generous, quiet negative space on textured off-white paper canvas. Zero characters, zero objects.",
        "accent": ""
    },
    2: {
        "title": "The Opening Riddle",
        "scene_type": "character_vignette",
        "refs": "@env_01_bedroom.jpg, @char_02_overgiver.jpg",
        "comp": "Wide shot of the quiet late-night bedroom matching @env_01_bedroom.jpg. In the center, an expressive 2D doodle stickman with a smooth round white circular head, wearing a simple blue sweater (CHAR_02_OVERGIVER), sits hunched on the edge of the wooden bed with his head buried in his hands in deep melancholy. Floating gently above his head are three hand-drawn doodle question marks in crimson red (#FF3B30) and warm amber (#F59E0B). The small bedside lamp casts a soft warm amber puddle of light.",
        "accent": "Warm amber lamp glow (#F59E0B) and crimson question marks (#FF3B30)."
    },
    3: {
        "title": "The 3-Second Reply",
        "scene_type": "split_screen_vignette",
        "refs": "@char_02_overgiver.jpg",
        "comp": "Extreme close-up of a smartphone screen. A message notification pops up instantly with a loud doodle buzz. Timestamp reads: Sent 10:42 PM -> Replied 10:42 PM. On the left side of the frame, CHAR_02_OVERGIVER is hunched over, sweating with frantic motion lines, fingers frantically tapping the glass.",
        "accent": "Glowing crimson red phone screen outline (#FF3B30)."
    },
    4: {
        "title": "The Aggressive Agreeableness",
        "scene_type": "character_interaction",
        "refs": "@char_02_overgiver.jpg, @char_03_observer.jpg, @env_04_campus_cafe.jpg",
        "comp": "Two-shot at a small wooden café table inside the campus café matching @env_04_campus_cafe.jpg. CHAR_03_OBSERVER (the girl in beige sweater) is talking with one hand raised. Sitting opposite her, CHAR_02_OVERGIVER is nodding so violently that multiple motion lines blur his head, giving an exaggerated agreeable thumbs-up with an eager people-pleasing smile.",
        "accent": ""
    },
    5: {
        "title": "The Schedule Collapse",
        "scene_type": "metaphor_diagram",
        "refs": "@char_01_sovereign.jpg (for ink style & line weight)",
        "comp": "A large hand-drawn weekly calendar on an off-white paper wall. All the busy schedule blocks ('Gym', 'Study', 'Dinner with Friends') are furiously scribbled out with violent red ink lines, replaced by a single heavy handwritten note across the entire page: 'WAITING FOR HER CALL'.",
        "accent": "Heavy crimson red marker scribbles (#FF3B30)."
    },
    6: {
        "title": "The Checklist Illusion",
        "scene_type": "prop_closeup",
        "refs": "@char_01_sovereign.jpg (for ink style & line weight)",
        "comp": "Close-up of a clean hand-drawn clipboard with a paper checklist: '[✔] Always replies', '[✔] Never argues', '[✔] Always compliments', '[✔] 100% Available'. All checkboxes are firmly marked in crisp slate-blue ink.",
        "accent": "Slate blue checkmarks (#2563EB)."
    },
    7: {
        "title": "The Perfect Partner on Paper",
        "scene_type": "character_vignette",
        "refs": "@char_02_overgiver.jpg, @char_03_observer.jpg",
        "comp": "Outdoor sidewalk in pouring rain in front of large glass building windows. CHAR_02_OVERGIVER stands politely holding a large black umbrella over CHAR_03_OBSERVER, holding a warm steaming coffee cup out to her with both hands, smiling eagerly with complete devotion. Raindrops splash into puddles on the ground.",
        "accent": "Soft warm amber steam rising from the coffee cup (#F59E0B)."
    },
    8: {
        "title": "The Instinctive Pullback",
        "scene_type": "character_interaction",
        "refs": "slide_007.png, @char_03_observer.jpg",
        "comp": "Direct continuity shot of the rainy outdoor scene from slide 007. On the right side of the frame, CHAR_02_OVERGIVER remains standing under his black umbrella holding out the warm coffee cup. On the left side of the frame, CHAR_03_OBSERVER crosses her arms over her beige sweater in defensive, uncomfortable body language and steps backward into the cold rain, physically pulling away from him and his umbrella. A noticeable cold empty distance widens between them on the wet pavement.",
        "accent": "Cold muted blue atmosphere with warm coffee cup contrast."
    },
    9: {
        "title": "The Suffocation of Text Bubbles",
        "scene_type": "metaphor_diagram",
        "refs": "@char_02_overgiver.jpg",
        "comp": "Surreal psychological metaphor. A minimalist stickman holding a glowing phone, buckling under massive physical weight as gigantic, heavy stone-textured speech bubbles fall from the sky onto his shoulders like 50-pound boulders, bending his spine downward.",
        "accent": "Heavy charcoal gray shading on the speech bubbles."
    },
    10: {
        "title": "Emotional Exhaustion",
        "scene_type": "character_closeup",
        "refs": "@char_03_observer.jpg",
        "comp": "Close-up of CHAR_03_OBSERVER staring down at her buzzing phone with heavy, half-closed exhausted eyes, letting out a visible hand-drawn doodle sigh cloud. A tiny battery icon floating above her head blinks at 8% in red ink.",
        "accent": "Blinking red battery icon (#FF3B30)."
    },
    11: {
        "title": "Taken for Granted",
        "scene_type": "character_vignette",
        "refs": "@char_02_overgiver.jpg, @char_03_observer.jpg",
        "comp": "Campus hallway lined with metal school lockers. On the left, CHAR_02_OVERGIVER waits anxiously beside a locker door, tentatively raising his hand with an eager hopeful smile. Walking straight past him toward the right, CHAR_03_OBSERVER checks her wristwatch with mild indifference, barely offering a glance or wave. The boy slowly lowers his raised hand in disappointment.",
        "accent": ""
    },
    12: {
        "title": "The Paradigm Shift",
        "scene_type": "transition_card",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "Graphic transition slate. The widescreen frame splits cleanly down the center with a sharp vertical black ink divider line. The left half fades to soft muted grey tone; the right half illuminates with crisp off-white paper canvas and a warm spotlight puddle in the center.",
        "accent": "Warm amber spotlight puddle (#FEF3C7)."
    },
    13: {
        "title": "The Arrival of The Sovereign",
        "scene_type": "character_vignette",
        "refs": "@char_01_sovereign.jpg",
        "comp": "Medium full-body shot of CHAR_01_SOVEREIGN leaning casually against an outdoor campus railing matching @char_01_sovereign.jpg. Dark charcoal hoodie, hands tucked comfortably into his front pocket, staring calmly and serenely toward the distant horizon with tranquil posture. A gentle breeze moves his messy hair.",
        "accent": ""
    },
    14: {
        "title": "The Ignored Device",
        "scene_type": "prop_closeup",
        "refs": "@char_01_sovereign.jpg",
        "comp": "Close-up on a clean wooden study desk. A smartphone lies face down on the table next to an open notebook. Three doodle notification vibration lines shake the phone, but no hand reaches for it. In the background, CHAR_01_SOVEREIGN's steady hand holds a fountain pen, calmly continuing to write notes without glancing at the screen.",
        "accent": ""
    },
    15: {
        "title": "The Three-Word Economy",
        "scene_type": "character_interaction",
        "refs": "@char_01_sovereign.jpg",
        "comp": "Two-shot side-by-side profile view of two 2D doodle stick figures with smooth solid white circular heads (#FFFFFF) and simple black ink outlines. On the left, an over-excited classmate stickman wearing a simple striped t-shirt gestures frantically with both hands, accompanied by a giant chaotic speech bubble filled with scribbled squiggly doodle lines representing non-stop rambling. On the right, CHAR_01_SOVEREIGN stands completely relaxed, wearing his oversized black hoodie with hands tucked in his pocket (matching @char_01_sovereign.jpg), calmly looking back with half-lidded unbothered eyes, offering a single small clean speech bubble containing only: 'Yes, that\\'s correct.'",
        "accent": ""
    },
    16: {
        "title": "No Clown Shoes",
        "scene_type": "metaphor_vignette",
        "refs": "@char_01_sovereign.jpg, @char_02_overgiver.jpg",
        "comp": "Surreal conceptual cartoon. An imaginary flaming circus hoop stands in the center of the frame. CHAR_02_OVERGIVER is frantically diving through the burning hoop wearing oversized clown shoes, while CHAR_01_SOVEREIGN stands calmly to the right, sipping coffee from a mug, observing the circus theatrics with serene detachment.",
        "accent": "Crimson and amber flames around the hoop (#FF3B30, #F59E0B)."
    },
    17: {
        "title": "Immune to Fake Politeness",
        "scene_type": "character_interaction",
        "refs": "@char_01_sovereign.jpg",
        "comp": "Close-up on a crowded social circle. Three background 2D doodle stickman students with smooth white circular heads are throwing their heads back in theatrical, forced, exaggerated fake laughter over a mediocre joke. In the center of the group, CHAR_01_SOVEREIGN maintains a steady, serene, neutral half-smile with half-lidded eyes, completely immune to peer pressure.",
        "accent": ""
    },
    18: {
        "title": "The Clean Refusal",
        "scene_type": "character_vignette",
        "refs": "@char_01_sovereign.jpg, @char_03_observer.jpg",
        "comp": "Campus hallway outside a doorway. CHAR_03_OBSERVER holds up two event tickets with an open, inviting posture. CHAR_01_SOVEREIGN offers a polite, warm half-nod, raises one hand in a calm respectful farewell gesture, and turns to walk toward the library.",
        "accent": ""
    },
    19: {
        "title": "The Broken Logic",
        "scene_type": "metaphor_diagram",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "A hand-drawn school blackboard illustration on paper canvas. A simple formula written in neat white chalk: 'Ignored = Forget & Move On'. Suddenly, a massive bold crimson red ink [ERROR] rubber stamp slams directly over the equation at an angle.",
        "accent": "Bright crimson rubber stamp (#FF3B30)."
    },
    20: {
        "title": "The Annoyance That Hooked You",
        "scene_type": "character_closeup",
        "refs": "@char_03_observer.jpg, @env_01_bedroom.jpg",
        "comp": "Inside her bedroom. Close-up of CHAR_03_OBSERVER sitting in a wooden desk chair, crossing her arms tightly over her beige sweater, pouting slightly with an annoyed furrow in her brow as she stares into space, clearly unable to stop thinking about him.",
        "accent": ""
    },
    21: {
        "title": "The 2:00 AM Screen Stare",
        "scene_type": "environment_vignette",
        "refs": "@env_01_bedroom.jpg, @char_03_observer.jpg",
        "comp": "Cinematic wide shot of the dark bedroom matching @env_01_bedroom.jpg. CHAR_03_OBSERVER is lying in the wooden bed under the blankets, holding up a glowing blue-white smartphone that illuminates her face in the dark room. On the bedside nightstand, the digital clock displays '02:14 AM' in glowing red digits.",
        "accent": "Cold blue phone glow contrasting with crimson red clock digits (#FF3B30)."
    },
    22: {
        "title": "The Mental Rewind",
        "scene_type": "metaphor_vignette",
        "refs": "@char_03_observer.jpg",
        "comp": "Profile silhouette head of CHAR_03_OBSERVER. Inside her transparent skull cavity, a vintage hand-drawn film projector reel is spinning backwards at high speed, projecting tiny miniature doodle stickmen replaying the hallway conversation in an endless loop.",
        "accent": ""
    },
    23: {
        "title": "The Black Hole of Mystery",
        "scene_type": "split_screen_contrast",
        "refs": "@char_03_observer.jpg",
        "comp": "Three hand-drawn doodle thought bubbles floating above the thinker: Bubble 1 shows a quiet desk with blueprints and a glowing lamp (Are they working?). Bubble 2 shows a café table with anonymous distant silhouettes (Are they with someone else?). Bubble 3 shows a heavy brass padlock over a smiling face (Why can't I unlock them?).",
        "accent": "Amber glow on the lamp and brass padlock (#F59E0B)."
    },
    24: {
        "title": "The Fundamental Question",
        "scene_type": "text_punch_card",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "Minimalist off-white paper canvas with giant hand-drawn black ink typography centered: 'WHY?' followed by a single bold crimson red question mark (#FF3B30). Generous, quiet negative space.",
        "accent": "Crimson question mark (#FF3B30)."
    },
    25: {
        "title": "The Core Dilemma",
        "scene_type": "metaphor_diagram",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "Wide psychological diagram showing two magnetic poles on paper: On the left, a stick figure holding wide open arms labeled '100% AVAILABLE'—a character is visibly running away from it. On the right, a solitary figure walking into distant fog labeled 'UNATTAINABLE'—the character is desperately reaching out, chasing after it.",
        "accent": "Slate blue for Available pole, crimson red for Unattainable pole."
    },
    26: {
        "title": "Not An Accident",
        "scene_type": "character_closeup",
        "refs": "@char_01_sovereign.jpg (for ink style & line weight)",
        "comp": "Clean centered illustration of a human brain drawn in elegant, minimalist black ink doodle outlines on cream paper canvas. Generous negative space.",
        "accent": ""
    },
    27: {
        "title": "De-shaming The Viewer",
        "scene_type": "metaphor_vignette",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "Minimalist concept card showing two hand-drawn rectangular stamp labels crossed out with thick, decisive crimson red X marks: '[✘ BAD LUCK]' and '[✘ BROKEN / TOXIC]'.",
        "accent": "Crimson red X marks (#FF3B30)."
    },
    28: {
        "title": "Evolutionary Wiring",
        "scene_type": "metaphor_diagram",
        "refs": "slide_026.png",
        "comp": "Direct continuation of the brain illustration from slide 026. The black ink brain illuminates from within with three glowing circuit pathways in slate blue and gold labeled: '[1. VALUE]', '[2. STATUS]', '[3. DESIRE]', with clean mechanical gear doodles meshing smoothly together.",
        "accent": "Golden nodes and gears lighting up along the neural pathways (#F59E0B)."
    },
    29: {
        "title": "The Pedestal Paradox Defined",
        "scene_type": "text_card",
        "refs": "@env_06_pedestal_pillar.jpg",
        "comp": "Clean typographic slate-blue banner across the upper third: 'THE PEDESTAL PARADOX'. Below it, matching @env_06_pedestal_pillar.jpg, a towering classical Greek marble column rising from the bottom edge of the paper canvas, with a tiny wooden ladder leaning against its base.",
        "accent": "Slate blue banner (#2563EB)."
    },
    30: {
        "title": "The Celebrity vs The Fan",
        "scene_type": "character_interaction",
        "refs": "slide_029.png, @char_03_observer.jpg, @char_02_overgiver.jpg",
        "comp": "Direct continuation of the pedestal scene from slide 029. High atop the classical marble pillar stands CHAR_03_OBSERVER under a warm golden spotlight puddle. Down on the dirt ground at the base of the pillar, CHAR_02_OVERGIVER stands holding an autograph book and camera, looking straight up with adoring cartoon eyes.",
        "accent": "Warm amber spotlight on top of the pedestal (#F59E0B)."
    },
    31: {
        "title": "Looking Up, Looking Down",
        "scene_type": "character_interaction",
        "refs": "@char_02_overgiver.jpg, @char_03_observer.jpg",
        "comp": "A graphic two-panel split screen divided cleanly by a single vertical black ink line down the center of the 16:9 widescreen canvas. On the left panel: Close-up profile of CHAR_02_OVERGIVER (an expressive 2D doodle stickman with a smooth round white circular head and blue sweater, normal neck and head proportions). He tilts his head slightly upward looking toward the top right with wide adoring starry eyes. Below him is a neat hand-drawn label: 'LOOKING UP'. On the right panel: Close-up profile of CHAR_03_OBSERVER (smooth round white circular head, brown ponytail, beige sweater). She looks downward toward the bottom left with uncomfortable, distant, detached eyes. Below her is a neat hand-drawn label: 'LOOKING DOWN'.",
        "accent": ""
    },
    32: {
        "title": "The Unconscious Valuation",
        "scene_type": "metaphor_diagram",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "Conceptual diagram. A hand-drawn digital cash register with a long receipt tape rolling out from a brain illustration. The printed receipt reads: 'ATTENTION RECEIVED: 100% | EFFORT REQUIRED: 0% | COMPUTED VALUE: $0.00'. The zero value is boldly highlighted in crimson red ink.",
        "accent": "Crimson red zero value (#FF3B30)."
    },
    33: {
        "title": "The Brutal Internal Monologue",
        "scene_type": "text_punch_card",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "Clean cream paper canvas with hand-drawn ink typography displaying the quote: 'If this person is offering me their complete devotion without me having to earn it, their time must not be worth very much.' In the background, a faint doodle stickman shrugging dismissively.",
        "accent": ""
    },
    34: {
        "title": "The Free Tap Water Metaphor",
        "scene_type": "metaphor_vignette",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "Minimalist kitchen sink illustration. A clean chrome faucet running clear water into a drain. A doodle stickman walks right past it holding a dirty cup without even glancing at the running water.",
        "accent": "Clear blue water flow (#2563EB)."
    },
    35: {
        "title": "The Buried Diamond",
        "scene_type": "metaphor_vignette",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "Geological cross-section view of the earth in minimalist ink lines. The ground surface is calm and empty; 5 miles below dense charcoal rock strata, a single glowing golden diamond radiates bright light. Tiny doodle stickman miners are furiously tunneling with pickaxes.",
        "accent": "Radiant golden gem sparkle (#F59E0B)."
    },
    36: {
        "title": "The Law of Value",
        "scene_type": "metaphor_diagram",
        "refs": "None (Pure typography card on paper canvas)",
        "comp": "A hand-drawn mechanical balance scale in slate-blue ink. On the left pan sits a heavy block labeled 'SCARCITY'; on the right pan sits an equally heavy block labeled 'EFFORT REQUIRED'. The scale rests in perfect equilibrium.",
        "accent": "Slate blue scale (#2563EB)."
    }
}

# Apply to storyboards
for sb_file in [ch1_dir / "storyboard.json", ep_dir / "storyboard.json"]:
    with open(sb_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    for s in data["shots"]:
        sid = s["shot_id"]
        if sid in ch1_updates:
            up = ch1_updates[sid]
            s["title"] = up["title"]
            s["scene_type"] = up["scene_type"]
            s["visual_composition_16_9"] = up["comp"]
            if up["accent"]:
                s["color_accent"] = up["accent"]
    with open(sb_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated Chapter 1 storyboards with flawless reference and composition logic!")
