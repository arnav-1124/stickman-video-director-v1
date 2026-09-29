# Modular Asset Consistency Rule (100% Locked Standard)

## The Core Rule: Zero Character Drift
In Ink Explainer's production style, **characters never change proportions, head sizes, or stroke weights across scenes**.

### How 100% Consistency is Guaranteed:
1. **The Circular Head Standard:**
   - Head is an exact digital vector circle (`#FFFFFF` fill, 6.5px solid black outline).
   - Never randomly re-prompt a generative AI model to create new stickman heads from scratch.
2. **Modular Layer Compositing:**
   - Scenes are constructed from layered transparent assets:
     - **Layer 1: Background** (e.g. `bg_lecture_hall.png`, `bg_backbench.png`, `bg_hallway.png`).
     - **Layer 2: Character Rig** (e.g. `silent_guy_leaning.png`, `frontbencher_hand_up.png`).
     - **Layer 3: Props** (e.g. `laptop.png`, `phone_glow.png`, `backpack.png`).
     - **Layer 4: Text Card** (Handwritten comic font + arrow on off-white background).
3. **Background Reuse:**
   - Backgrounds are drawn once and reused across multiple scenes (e.g. wide lecture hall, close-up back row).
