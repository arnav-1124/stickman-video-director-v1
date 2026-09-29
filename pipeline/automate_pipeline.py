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
        "stage": "MASTER_ASSETS",
        "style": "INK_EXPLAINER",
        "total_cuts": len(sb.get("cuts", [])),
        "cuts": []
    }
    
    for cut in sb.get("cuts", []):
        status["cuts"].append({
            "cut_id": cut.get("cut_id"),
            "slide_image": {"status": "pending", "file": f"slides/slide_{cut.get('cut_id'):02d}.png"},
            "duration": cut.get("duration", cut.get("duration_sec", 1.5))
        })
        
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2)
        
    print(f"[STATUS] Initialized episode status tracker at: {status_file}")
    return status

def ingest_master_assets(project_dir, source_dir=None):
    """
    Ingests 6 master reference assets from Downloads folder into master_assets/.
    """
    project_dir = Path(project_dir).resolve()
    if not source_dir:
        source_dir = Path.home() / "Downloads"
    else:
        source_dir = Path(source_dir).resolve()

    if not source_dir.exists():
        print(f"Error: Source directory {source_dir} not found.")
        return

    exts = ['.png', '.jpg', '.jpeg', '.webp']
    target_dir = project_dir / "master_assets"
    target_dir.mkdir(parents=True, exist_ok=True)

    files = [f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() in exts]
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    expected = 6
    selected = files[:expected]
    selected.reverse() # chronological order

    print(f"\nIngesting {len(selected)} master asset images into {target_dir}:")
    for idx, src_file in enumerate(selected, start=1):
        target_name = f"master_asset_{idx:02d}{src_file.suffix.lower()}"
        target_path = target_dir / target_name
        shutil.copy2(src_file, target_path)
        print(f"  [{idx}/{len(selected)}] {src_file.name} -> {target_name}")

    print(f"\n[INGESTION_COMPLETE] Master assets ingested into: {target_dir}")

def ingest_slides(project_dir, source_dir=None):
    """
    Ingests downloaded scene slides from Downloads folder, sorts them by creation time,
    and cleanly places them into slides/slide_01.png, slide_02.png, etc.
    """
    project_dir = Path(project_dir).resolve()
    if not source_dir:
        source_dir = Path.home() / "Downloads"
    else:
        source_dir = Path(source_dir).resolve()

    if not source_dir.exists():
        print(f"Error: Source directory {source_dir} not found.")
        return

    exts = ['.png', '.jpg', '.jpeg', '.webp']
    target_dir = project_dir / "slides"
    target_dir.mkdir(parents=True, exist_ok=True)

    files = [f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() in exts]
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    storyboard_file = project_dir / "storyboard.json"
    num_cuts = 0
    if storyboard_file.exists():
        with open(storyboard_file, 'r', encoding='utf-8') as f:
            sb = json.load(f)
        num_cuts = len(sb.get("cuts", []))

    if num_cuts > 0 and len(files) < num_cuts:
        print(f"Warning: Found {len(files)} image files in {source_dir}, but episode expects {num_cuts} slide images.")
    
    count_to_take = num_cuts if (num_cuts > 0 and len(files) >= num_cuts) else len(files)
    selected = files[:count_to_take]
    selected.reverse()  # Chronological order

    print(f"\nIngesting {len(selected)} comic slide images into {target_dir}:")
    for idx, src_file in enumerate(selected, start=1):
        target_name = f"slide_{idx:02d}.png"
        target_path = target_dir / target_name
        shutil.copy2(src_file, target_path)
        print(f"  [{idx}/{len(selected)}] {src_file.name} -> {target_name}")

    print(f"\n[INGESTION_COMPLETE] Ingested {len(selected)} slides into: {target_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Comic Studio Pipeline Automator")
    parser.add_argument("project_dir", help="Path to project episode directory")
    parser.add_argument("--init-status", action="store_true", help="Initialize status tracker")
    parser.add_argument("--ingest-master-assets", action="store_true", help="Auto-ingest downloaded master references into master_assets/")
    parser.add_argument("--ingest-slides", action="store_true", help="Auto-ingest downloaded scene slides into slides/")
    parser.add_argument("--source-dir", default=None, help="Custom folder for ingestion (defaults to Downloads)")
    args = parser.parse_args()

    if args.init_status or not (Path(args.project_dir) / "status.json").exists():
        init_episode_status(args.project_dir)
        
    if args.ingest_master_assets:
        ingest_master_assets(args.project_dir, args.source_dir)

    if args.ingest_slides:
        ingest_slides(args.project_dir, args.source_dir)
