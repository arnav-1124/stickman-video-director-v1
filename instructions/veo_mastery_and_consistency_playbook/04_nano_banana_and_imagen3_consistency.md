# Chapter 04: Nano Banana Pro & Imagen 3 Consistency

> "A video can only be as consistent as the anchor image you feed it."

To produce studio-grade episodes, you must first master **Character DNA Anchoring** in Nano Banana Pro (Imagen 3). If your character's clothes or facial features shift between image anchors, the video generation will inherit that drift.

---

## 1. Building the "Character DNA" Reference Pack

Before generating a single scene, create a dedicated reference image for each character with these strict rules:

1. **Clean Studio Isolation:** Generate the character on a neutral, soft grey or white studio backdrop. Never generate character references with busy backgrounds (e.g., in a playground or bedroom), as the background elements will "bleed" into future scenes.
2. **Standard Eye-Level Full-Body:** Show head-to-toe with neutral expression, clear clothing details, and signature colorways.
3. **Locked Character Bible Tokens:** Write a rigid, immutable 2-sentence description for each character that is never altered.

### Example Character DNA Tokens:
* **Tommy:** `5-year-old boy, messy bright blonde hair, large curious blue eyes, wearing a vibrant turquoise-blue t-shirt with a small green cartoon dinosaur graphic, dark denim shorts, and white sneakers.`
* **Emily:** `9-year-old girl, shoulder-length curly chestnut-brown hair with yellow ribbon bow, warm hazel eyes, wearing a mustard-yellow zip-up hooded jacket over a white tee, dark blue jeans, and brown canvas sneakers.`
* **Barnaby:** `Giant cuddly mythical creature, 9 feet tall, covered in thick fluffy pastel-teal fur, soft cream-colored chest fur patch, large rounded fuzzy teddy-bear ears, warm puppy-dog brown eyes, gentle toothy smile.`

---

## 2. The 3-Asset Attachment Strategy in Google Flow

Google Flow allows up to **3 reference images** attached per prompt. To maximize continuity across complex scenes, follow this attachment matrix:

| Scene Type | Attachment 1 | Attachment 2 | Attachment 3 | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Character Close-Up** | `@Character` (DNA) | `@Character` (Alternate Angle) | Previous Approved Shot | Perfect facial likeness & lighting match. |
| **Two Characters Interacting** | `@Character_A` (DNA) | `@Character_B` (DNA) | Approved Scene Environment | Both characters retain exact clothes & hair. |
| **Scene Continuity Cut** | Previous Scene Anchor | `@Main_Character` | `@Secondary_Character` | Background geometry and characters stay 100% locked. |

---

## 3. Google AI Safety & Policy Filter Bypass

Google Flow and Imagen 3 utilize strict automated safety classifiers. Innocent words common in fantasy or animation can trigger false-positive blocks (e.g., *"Prompt violated safety policies"*).

Always use **Studio-Approved Policy-Safe Substitutes**:

| ❌ Trigger Word | Why It Triggers | ✅ Safe Studio Substitute |
| :--- | :--- | :--- |
| `"Monster"` | Flagged under horror, threat, or demonic entity classifiers. | `"lovable fluffy mythical forest creature"` or `"gentle giant woodland companion"` |
| `"Horns"` | Flagged as demonic or aggressive imagery. | `"cute rounded fuzzy ears"` or `"soft curved fuzzy antennae"` |
| `"Creamy tummy"` | Flagged by automated child safety/nudity filters. | `"soft cream-colored chest fur"` or `"light beige furry belly patch"` |
| `"Non-scary"` / `"Harmless"` | The negative token "scary" is often parsed positively by diffusion attention. | Emphasize purely positive terms: `"cheerful, cuddly, smiling, sweet, friendly"` |
| `"Crying hysterically"` | Can trigger mental distress filters. | `"pouting sadly, rubbing a tear from eye, sniffling gently"` |
## 4. Stickman & Ink Explainer Character DNA Anchoring

For stickman psychological explainer channels (*The Paint Explainer* / *Ink Explainer* style), Nano Banana Pro must lock the 2D minimalist vector doodle aesthetic:

### Character DNA Tokens (Stickman):
* **The Performative Alpha:** `Minimalist 2D doodle stick figure with a smooth circular white head and bold black ink strokes (#0A0D14), wearing exaggerated black outline doodle sneakers, standing on a wooden desk with an oversized black ink megaphone, clean off-white textured paper background (#FAF9F6), high contrast monochrome.`
* **The Quiet Sigma / Observer:** `Minimalist 2D doodle stick figure with a smooth circular white head and bold solid black ink strokes, sitting upright at a simple wooden desk, holding a steaming coffee cup, serene and unbothered posture, clean off-white paper canvas (#FAF9F6), crisp line drawing.`

### Crucial Nano Banana Pro Rules for 2D Stickman:
1. **Never ask for photorealism or 3D shading:** Always specify `"2D vector line art, clean doodle illustration, flat line drawing, zero 3D depth, off-white textured paper"`.
2. **Prevent Realistic Faces:** Always specify `"smooth solid white circular head with zero facial features or simple tiny dot eyes"`.
3. **Preserve High Contrast:** Pure black ink lines on light warm cream paper.
