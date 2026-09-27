# Generation Workflow Rule

## The Agent Chain & JSON Contract Protocol
All Stickman & Ink Explainer productions strictly follow this sequential 5-stage lifecycle. Each agent completes its scope of work, writes its designated JSON contract, outputs `[TASK_COMPLETE]`, and recommends the next responsible agent:

```mermaid
graph TD
    A["1. creative-researcher<br/>(creative_research.json)"] --> B["2. storyboard-director<br/>(storyboard.json)"]
    B --> C["3. prompt-engineer<br/>(prompts.json & batch sheets)"]
    C --> D["Phase 1: Nano Banana Pro (Anchor Images)<br/>Phase 2: Google Veo 3.1 (Video Clips)"]
    D --> E["4. ffmpeg-assembler<br/>(build_manifest.json & render)"]
    E --> F["5. youtube-publisher<br/>(youtube_metadata.json)"]
```

### Directorial Ground Rules:
1. **Nano Banana Pro (Imagen 3)** is the ONLY image generation tool for scene anchors.
2. **Google Veo 3.1** in Google Flow / VideoFX is the ONLY tool for video clips (Image-to-Video).
3. **Phase Separation**:
   - Provide the exact prompt text for **Phase 1: Nano Banana Pro** anchor images FIRST.
   - Wait for user generation / confirmation before moving to **Phase 2: Google Veo 3.1**.
4. **Agent Handoff Requirement**:
   - Once an agent finishes its JSON contract, it must signal `[TASK_COMPLETE]` and explicitly recommend proceeding to the next responsible agent.
