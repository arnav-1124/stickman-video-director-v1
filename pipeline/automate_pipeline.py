import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import argparse
import json
import os
import shutil
from pathlib import Path

def init_episode_status(project_dir):
    """Initializes or loads the episode production state tracker."""
    project_dir = Path(project_dir).resolve()
    status_file = project_dir / "status.json"
    storyboard_file = project_dir / "storyboard.json"
    
    if status_file.exists():
        with open(status_file, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    if not storyboard_file.exists():
        print(f"[Error] storyboard.json not found in {project_dir}")
        return None
        
    with open(storyboard_file, 'r', encoding='utf-8') as f:
        sb = json.load(f)
        
    status = {
        "project_id": sb.get("project_id", project_dir.name),
        "stage": "CHARACTER_ANCHORS",
        "style": "INK_EXPLAINER",
        "shots": []
    }
    
    for shot in sb.get("shots", []):
        status["shots"].append({
            "shot_id": shot.get("shot_id"),
            "anchor_image": {"status": "pending", "file": None},
            "raw_video": {"status": "pending", "file": None},
            "audio": {"status": "pending", "file": None}
        })
        
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2)
        
    print(f"[STATUS] Initialized episode status tracker at: {status_file}")
    return status

def ingest_downloads(project_dir, source_dir=None, media_type="video"):
    """
    Ingests downloaded files from Downloads folder, sorts them by creation time,
    and cleanly places them into raw/ or anchors/.
    """
    project_dir = Path(project_dir).resolve()
    if not source_dir:
        source_dir = Path.home() / "Downloads"
    else:
        source_dir = Path(source_dir).resolve()

    if not source_dir.exists():
        print(f"Error: Source directory {source_dir} not found.")
        return

    exts = ['.mp4', '.mov', '.webm'] if media_type == "video" else ['.png', '.jpg', '.jpeg', '.webp']
    target_dir = project_dir / ("raw" if media_type == "video" else "anchors")
    target_dir.mkdir(parents=True, exist_ok=True)

    files = [f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() in exts]
    # Sort by modification time (most recent first)
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    storyboard_file = project_dir / "storyboard.json"
    num_shots = 0
    if storyboard_file.exists():
        with open(storyboard_file, 'r', encoding='utf-8') as f:
            sb = json.load(f)
        num_shots = len(sb.get("shots", []))

    if num_shots > 0 and len(files) < num_shots:
        print(f"Warning: Found {len(files)} {media_type} files in {source_dir}, but episode expects {num_shots} files.")
    
    count_to_take = num_shots if (num_shots > 0 and len(files) >= num_shots) else len(files)
    selected = files[:count_to_take]
    selected.reverse()  # Chronological order

    print(f"\nIngesting {len(selected)} {media_type} files into {target_dir}:")
    for idx, src_file in enumerate(selected, start=1):
        target_name = f"shot_{idx}{src_file.suffix.lower()}"
        target_path = target_dir / target_name
        shutil.copy2(src_file, target_path)
        print(f"  [{idx}/{len(selected)}] {src_file.name} -> {target_name}")

    print(f"\n[INGESTION_COMPLETE] Ingested {len(selected)} files into: {target_dir}")

def export_batch_prompts(project_dir):
    """Exports structured copy-paste batches for Nano Banana Pro (Images) and Google Veo 3.1 (Videos)."""
    project_dir = Path(project_dir).resolve()
    prompts_path = project_dir / "prompts.json"
    if not prompts_path.exists():
        print(f"[Error] prompts.json not found in {project_dir}")
        return

    with open(prompts_path, 'r', encoding='utf-8') as f:
        prompts = json.load(f)

    # 1. Export quick_batch_copypaste.txt
    export_file = project_dir / "quick_batch_copypaste.txt"
    with open(export_file, 'w', encoding='utf-8') as f:
        f.write("=================================================================\n")
        f.write("      AI ANIMATION STUDIO: QUICK BATCH COPY-PASTE PACKET         \n")
        f.write(f"      Project: {project_dir.name}\n")
        f.write("=================================================================\n\n")
        
        f.write("--- PHASE 1: NANO BANANA PRO (IMAGE ANCHOR PROMPTS) ---\n")
        f.write("Aspect Ratio: 9:16 Vertical | Style: Ink Explainer / Vector Doodle\n\n")
        for shot in prompts.get("shots", []):
            sid = shot.get("shot_id")
            anchor_prompt = shot.get("nano_banana_prompt") or shot.get("anchor_prompt") or shot.get("imagen_3_prompt", "")
            f.write(f"--- SHOT {sid} (Anchor Image) ---\n")
            f.write(f"{anchor_prompt}\n\n")

        f.write("\n--- PHASE 2: GOOGLE VEO 3.1 (IMAGE-TO-VIDEO MOTION PROMPTS) ---\n")
        f.write("Platform: Google Flow / VideoFX | Format: 9:16 Vertical\n")
        f.write("Workflow: Upload Anchor Image as Starting Frame -> Paste Motion Prompt\n\n")
        for shot in prompts.get("shots", []):
            sid = shot.get("shot_id")
            veo_prompt = shot.get("veo_prompt") or shot.get("video_prompt", "")
            f.write(f"--- SHOT {sid} (Veo 3.1 Motion) ---\n")
            f.write(f"{veo_prompt}\n\n")

    # 2. Export nano_banana_prompts.md
    nano_file = project_dir / "nano_banana_prompts.md"
    with open(nano_file, 'w', encoding='utf-8') as f:
        f.write(f"# Nano Banana Pro (Imagen 3) Prompts: {project_dir.name}\n\n")
        f.write("**Style Core:** 2D Ink Explainer, clean off-white textured paper (`#FAF9F6`), smooth circular white stickman head, bold solid black ink strokes (`#0A0D14`), 1-color accents.\n\n")
        f.write("### Global Negative Prompt\n```text\n")
        f.write(prompts.get("negative_prompt", "photorealistic, 3d render, claymation, blurry, human skin, realistic faces") + "\n```\n\n---\n\n")
        for shot in prompts.get("shots", []):
            sid = shot.get("shot_id")
            anchor_prompt = shot.get("nano_banana_prompt") or shot.get("anchor_prompt") or shot.get("imagen_3_prompt", "")
            f.write(f"### Shot {sid} Anchor Frame\n")
            f.write(f"```text\n{anchor_prompt}\n```\n\n")

    # 3. Export veo_prompts.md
    veo_file = project_dir / "veo_prompts.md"
    with open(veo_file, 'w', encoding='utf-8') as f:
        f.write(f"# Google Veo 3.1 Directorial Prompts: {project_dir.name}\n\n")
        f.write("**Directorial Standard:** 7-Layer formula with narrow temporal intervals and anti-hallucination guardrails.\n\n---\n\n")
        for shot in prompts.get("shots", []):
            sid = shot.get("shot_id")
            veo_prompt = shot.get("veo_prompt") or shot.get("video_prompt", "")
            f.write(f"### Shot {sid} Veo 3.1 Motion\n")
            f.write(f"```text\n{veo_prompt}\n```\n\n")

    print(f"[EXPORT_COMPLETE] Quick batch packet exported to: {export_file}")
    print(f"[EXPORT_COMPLETE] Nano Banana guide saved to: {nano_file}")
    print(f"[EXPORT_COMPLETE] Google Veo 3.1 guide saved to: {veo_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Animation Studio Pipeline Automator")
    parser.add_argument("project_dir", help="Path to project episode directory")
    parser.add_argument("--init-status", action="store_true", help="Initialize status tracker")
    parser.add_argument("--export-batch", action="store_true", help="Export clean batch prompts for web UI")
    parser.add_argument("--ingest-videos", action="store_true", help="Auto-ingest downloaded videos into raw/")
    parser.add_argument("--ingest-images", action="store_true", help="Auto-ingest downloaded images into anchors/")
    parser.add_argument("--source-dir", default=None, help="Custom folder for ingestion (defaults to Downloads)")
    args = parser.parse_args()

    if args.init_status or not (Path(args.project_dir) / "status.json").exists():
        init_episode_status(args.project_dir)
        
    if args.export_batch:
        export_batch_prompts(args.project_dir)

    if args.ingest_videos:
        ingest_downloads(args.project_dir, args.source_dir, media_type="video")
        
    if args.ingest_images:
        ingest_downloads(args.project_dir, args.source_dir, media_type="image")
