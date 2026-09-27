# Mandatory Video Prompt Anchor Analysis Rule

> **RULE:** You MUST NEVER generate final Veo / Image-to-Video (I2V) prompts before inspecting and thoroughly analyzing the approved anchor image for that exact scene, regardless of its filename (e.g., `shot_06.jpg`, `shot_6.png`, `shot_06_approved.jpg`, `scene_03.webp`, etc.).

## Why This Rule Exists
In Image-to-Video diffusion models (like Google Veo 3.1), the starting image frame dictates reality. 
If a prompt describes characters entering, stepping out, or positioned in a depth/location that contradicts the starting image, the model will hallucinate duplicate characters (e.g., spawning a duplicate set of kids in the foreground while keeping the original set in the background). This wastes valuable user credits.

## Mandatory Pre-Flight Checklist Before Writing ANY Video Prompt
1. **Locate & View the Approved Anchor Image First**:
   - Dynamically inspect the corresponding shot image in `anchors/` (do NOT assume a rigid naming convention; check for any match like `shot_0X*`, `shot_X*`, or whatever image file is present for that shot).
2. **Catalog Exact Character Presence**:
   - List exactly who is in the image.
   - Note their precise screen positions (e.g., *Barnaby: center foreground; Tommy & Emily: upper-right hill behind tree*).
   - If a character is NOT in the anchor image, NEVER mention them in the video prompt.
3. **Respect Starting Poses & Spatial Depths**:
   - The video prompt must ONLY describe the natural, chronological continuation of the exact pose frozen in the anchor image.
   - NEVER say "steps out into view", "sprints into frame", or describe a background character as being in the foreground.
4. **Explicit Anti-Hallucination Clause**:
   - Explicitly instruct the video model: `"Only the characters already present in the starting frame animate. No new characters appear anywhere in the frame."`
5. **Master Playbook Reference**:
   - For complete guidelines on spatial depth locking, 1s-2s interval choreographies, and lens vocabulary, see the standalone module: [`instructions/veo_mastery_and_consistency_playbook/`](file:///e:/yt-shorts-animation-v1/instructions/veo_mastery_and_consistency_playbook/README.md).
