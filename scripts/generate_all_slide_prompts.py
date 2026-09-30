import json
import re
from pathlib import Path

# Paths
ep_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them")
ep_sb_path = ep_dir / "storyboard.json"

with open(ep_sb_path, "r", encoding="utf-8") as f:
    ep_data = json.load(f)

shots = ep_data["shots"]

# Load ch01 specific storyboard if available for exact durations
ch01_sb_path = ep_dir / "chapter_01_the_pedestal_paradox" / "storyboard.json"
ch01_durations = {}
if ch01_sb_path.exists():
    with open(ch01_sb_path, "r", encoding="utf-8") as f:
        ch01_data = json.load(f)
        for s in ch01_data["shots"]:
            ch01_durations[s["shot_id"]] = s["duration_sec"]

chapter_titles = {
    1: "CHAPTER 01: THE PEDESTAL PARADOX",
    2: "CHAPTER 02: THE CASINO EFFECT",
    3: "CHAPTER 03: THE ECONOMY OF AVAILABILITY",
    4: "CHAPTER 04: THE MAGNETISM OF THE UNOCCUPIED MIND",
    5: "CHAPTER 05: DETACHMENT WITHOUT CRUELTY",
}

chapter_folder_names = {
    1: "chapter_01_the_pedestal_paradox",
    2: "chapter_02_the_casino_effect",
    3: "chapter_03_the_economy_of_availability",
    4: "chapter_04_the_magnetism_of_the_unoccupied_mind",
    5: "chapter_05_detachment_without_cruelty",
}

def clean_visual_composition(comp_text):
    text = comp_text.replace("\n", " ").strip()
    
    # Strip out audio cues and storyboard animation loop directives
    text = re.sub(r"A subtle sub-bass thud plays\.?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"A subtle sub-bass[^\.]*\.?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"A low frequency[^\.]*\.?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"with a click sound\s*`\*CLICK\*`\.?", "clicking the lever.", text, flags=re.IGNORECASE)
    text = re.sub(r"with a chime\s*`\*DING\*`\.?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"2-step animation loop:?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"1\.\s*", "", text)
    text = re.sub(r"2\.\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def determine_references(shot):
    scene_type = shot.get("scene_type", "")
    comp_raw = shot.get("visual_composition_16_9", "")
    text = (
        shot.get("title", "") + " " +
        comp_raw + " " +
        shot.get("spoken_clause", "") + " " +
        shot.get("psychological_intent", "")
    ).lower()

    # Pure text/title cards without any character mention should NOT attach character/environment references
    is_pure_text = any(t in scene_type for t in ["title_card", "text_card", "text_punch_card", "transition_card", "outro_card", "fade_out"])
    has_character_figure = any(c in comp_raw for c in ["CHAR_01", "CHAR_02", "CHAR_03", "CHAR_04", "CHAR_05", "CHAR_06", "CHAR_07", "stickman", "person", "silhouette", "figure", "pigeon", "salesman", "scientist"])

    if is_pure_text and not has_character_figure:
        return "None (Pure typography card on paper canvas)"

    refs = []

    # Characters
    if any(k in text for k in ["sovereign", "backbencher", "char_01"]) or "CHAR_01" in comp_raw:
        refs.append("@char_01_sovereign.jpg")
    if any(k in text for k in ["overgiver", "anxious", "char_02", "people-pleas", "pleasing", "text", "replied", "frantic"]) or "CHAR_02" in comp_raw:
        refs.append("@char_02_overgiver.jpg")
    if any(k in text for k in ["observer", "char_03", "female", "girl", "woman", "classmate", "crush", "walks past"]) or "CHAR_03" in comp_raw:
        refs.append("@char_03_observer.jpg")
    if any(k in text for k in ["salesman", "salesperson", "char_04", "discount", "megaphone", "cheap suit"]) or "CHAR_04" in comp_raw:
        refs.append("@char_04_salesman.jpg")
    if any(k in text for k in ["scientist", "skinner", "char_05", "lab coat"]) or "CHAR_05" in comp_raw:
        refs.append("@char_05_scientist.jpg")
    if any(k in text for k in ["pigeon", "char_06", "beak", "peck", "pellet"]) or "CHAR_06" in comp_raw:
        refs.append("@char_06_pigeon.jpg")
    if any(k in text for k in ["inner child", "char_07", "child", "chest cavity", "vulnerable"]) or "CHAR_07" in comp_raw:
        refs.append("@char_07_inner_child.jpg")

    # Environments
    if any(k in text for k in ["bedroom", "bed", "2:14", "02:14", "midnight", "night stand"]):
        refs.append("@env_01_bedroom.jpg")
    if any(k in text for k in ["skinner lab", "lever", "cage", "operant", "slot machine", "casino", "gambler"]):
        refs.append("@env_02_skinner_lab.jpg")
    if any(k in text for k in ["library", "bookshelf", "bookshelves", "studying", "study table"]):
        refs.append("@env_03_library.jpg")
    if any(k in text for k in ["cafe", "coffee", "umbrella", "latte", "dining"]):
        refs.append("@env_04_campus_cafe.jpg")
    if any(k in text for k in ["brain", "mindscape", "neural", "scale", "balance scale", "value scale", "dopamine", "graph", "metric", "psychological"]):
        refs.append("@env_05_abstract_mind.jpg")
    if any(k in text for k in ["pedestal", "pillar", "column", "marble", "throne"]) and "title_card" not in scene_type:
        refs.append("@env_06_pedestal_pillar.jpg")

    if not refs:
        refs.append("@char_01_sovereign.jpg (for ink style & line weight)")

    return ", ".join(refs)

def build_prompt(shot, ref_str):
    comp = clean_visual_composition(shot.get("visual_composition_16_9", ""))
    accent = shot.get("color_accent", "").replace("\n", " ").strip()
    accent = re.sub(r"\s+", " ", accent)
    accent_str = f"Color Accent: {accent}. " if accent else ""

    ref_clause = f"Using references {ref_str}: " if ref_str != "None (Pure typography card on paper canvas)" else ""

    prompt_text = (
        f"A single edge-to-edge 16:9 widescreen hand-drawn 2D vector ink illustration in the minimalist Ink Explainer style, "
        f"drawn on an off-white textured paper canvas (#FAF9F6). Bold wobbly organic black ink pen outlines (6px-8px stroke weight), "
        f"flat solid color blocking, zero gradients, zero 3D rendering, zero photorealism, zero CAD perspective. "
        f"Widescreen 16:9 landscape aspect ratio (1920x1080). {ref_clause}{comp}. "
        f"{accent_str}"
        f"Clean minimalist line art with generous negative space. "
        f"STRICT NEGATIVE: Single full-frame 16:9 landscape image only. NO multiple panels, NO comic book strips, NO cards, NO black borders, NO frames, NO grid layouts, NO split screens, NO speech bubbles, NO realistic human skin."
    )
    return prompt_text

# 1. Generate Episode-wide Nano Banana Slide Prompts Markdown
ep_md_path = ep_dir / "nano_banana_slide_prompts.md"
ep_txt_path = ep_dir / "quick_batch_copypaste.txt"

# Group shots by chapter
chapters_data = {1: [], 2: [], 3: [], 4: [], 5: []}
for s in shots:
    ch = s["chapter"]
    chapters_data[ch].append(s)

with open(ep_md_path, "w", encoding="utf-8") as md, open(ep_txt_path, "w", encoding="utf-8") as txt:
    md.write("# Nano Banana Pro (Google Flow AI) Scene Slide Prompts: Complete Episode 01\n")
    md.write("## Episode 01: Why People Fall For Who Ignores Them\n")
    md.write("### Complete Production Packet: All 148 Slides (Chapters 01 – 05)\n\n")
    md.write("> **Aspect Ratio:** `16:9` Widescreen (`1920x1080` Landscape)  \n")
    md.write("> **Global Aesthetic:** 2D Minimalist Vector Ink Explainer on Textured Paper  \n")
    md.write("> **Model:** Nano Banana Pro (Gemini 3 Pro Image) via Google Flow  \n")
    md.write("> **Framing Rule:** Every single slide must be generated as a single full-screen edge-to-edge landscape frame. Do not select vertical/comic formats.\n\n")
    md.write("---\n\n")

    txt.write("==================================================================\n")
    txt.write("  EPISODE 01: WHY PEOPLE FALL FOR WHO IGNORES THEM\n")
    txt.write("  Model: Nano Banana Pro (Gemini 3 Pro Image) via Google Flow\n")
    txt.write("  Aspect Ratio: 16:9 Widescreen Landscape (1920x1080)\n")
    txt.write("  Style: Minimal Hand-Drawn 2D Ink Explainer (Single Full Frame)\n")
    txt.write("  Total Slides: 148 | All 5 Chapters\n")
    txt.write("==================================================================\n\n")

    for ch_num, ch_shots in chapters_data.items():
        ch_title = chapter_titles[ch_num]
        md.write(f"## {ch_title} (Shots {ch_shots[0]['shot_id']:03d} – {ch_shots[-1]['shot_id']:03d})\n\n")
        
        txt.write("==================================================================\n")
        txt.write(f"  {ch_title} (Shots {ch_shots[0]['shot_id']:03d} - {ch_shots[-1]['shot_id']:03d})\n")
        txt.write("==================================================================\n\n")

        ch_folder = ep_dir / chapter_folder_names[ch_num]
        ch_md_path = ch_folder / "nano_banana_prompts.md"
        ch_txt_path = ch_folder / "quick_batch_copypaste.txt"
        
        ch_md_lines = []
        ch_txt_lines = []

        ch_md_lines.append(f"# Nano Banana Pro (Google Flow AI) Scene Slide Prompts: {ch_title}\n")
        ch_md_lines.append("## Episode 01: Why People Fall For Who Ignores Them\n\n")
        ch_md_lines.append("> **Aspect Ratio:** `16:9` Widescreen Landscape (`1920x1080`)  \n")
        ch_md_lines.append("> **Global Aesthetic:** 2D Minimalist Vector Ink Explainer on Textured Paper  \n")
        ch_md_lines.append("> **Model:** Nano Banana Pro (Gemini 3 Pro Image) via Google Flow  \n\n")
        ch_md_lines.append("---\n\n")

        ch_txt_lines.append("==================================================================\n")
        ch_txt_lines.append(f"  EPISODE 01 - {ch_title}\n")
        ch_txt_lines.append("  Model: Nano Banana Pro (Gemini 3 Pro Image) via Google Flow\n")
        ch_txt_lines.append(f"  Aspect Ratio: 16:9 Widescreen Landscape (1920x1080)\n")
        ch_txt_lines.append("  Style: Minimal Hand-Drawn 2D Ink Explainer (Single Full Frame)\n")
        ch_txt_lines.append(f"  Total Slides: {len(ch_shots)}\n")
        ch_txt_lines.append("==================================================================\n\n")

        for s in ch_shots:
            shot_id = s["shot_id"]
            title = s["title"]
            dur = ch01_durations.get(shot_id, s["duration_sec"])
            clause = s.get("spoken_clause", "")
            scene_type = s.get("scene_type", "")
            ref_str = determine_references(s)
            prompt = build_prompt(s, ref_str)

            # Write to Episode MD
            md.write(f"### Slide {shot_id:03d} (`slide_{shot_id:03d}.png`)\n")
            md.write(f"- **Title / Action:** {title}\n")
            md.write(f"- **Duration:** `{dur}s`\n")
            md.write(f"- **Voiceover Phrase:** *\"{clause}\"*\n")
            md.write(f"- **Scene Type:** `{scene_type}`\n")
            md.write(f"- **Bound References:** `{ref_str}`\n")
            md.write(f"- **Flow AI Prompt (16:9 Widescreen):**\n")
            md.write("```text\n")
            md.write(prompt + "\n")
            md.write("```\n\n")
            md.write("---\n\n")

            # Write to Episode TXT
            txt.write(f"--- SLIDE {shot_id:03d} ({dur}s) --- [Voiceover: \"{clause}\"]\n")
            txt.write(f"{prompt}\n\n")

            # Chapter MD
            ch_md_lines.append(f"### Slide {shot_id:03d} (`slide_{shot_id:03d}.png`)\n")
            ch_md_lines.append(f"- **Title / Action:** {title}\n")
            ch_md_lines.append(f"- **Duration:** `{dur}s`\n")
            ch_md_lines.append(f"- **Voiceover Phrase:** *\"{clause}\"*\n")
            ch_md_lines.append(f"- **Scene Type:** `{scene_type}`\n")
            ch_md_lines.append(f"- **Bound References:** `{ref_str}`\n")
            ch_md_lines.append(f"- **Flow AI Prompt (16:9 Widescreen):**\n")
            ch_md_lines.append("```text\n")
            ch_md_lines.append(prompt + "\n")
            ch_md_lines.append("```\n\n")
            ch_md_lines.append("---\n\n")

            # Chapter TXT
            ch_txt_lines.append(f"--- SLIDE {shot_id:03d} ({dur}s) --- [Voiceover: \"{clause}\"]\n")
            ch_txt_lines.append(f"{prompt}\n\n")

        with open(ch_md_path, "w", encoding="utf-8") as f_ch_md:
            f_ch_md.writelines(ch_md_lines)
        with open(ch_txt_path, "w", encoding="utf-8") as f_ch_txt:
            f_ch_txt.writelines(ch_txt_lines)

print("Slide prompts successfully updated across all files!")
