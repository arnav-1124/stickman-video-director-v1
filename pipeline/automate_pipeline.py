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

def ingest_slides(project_dir, source_dir=None, dry_run=False, ext=None, delete_source=False, count=None):
    """
    Ingests downloaded scene slides from Downloads folder, sorts them cleanly,
    and places them into slides/slide_01.jpg, slide_02.jpg, etc.
    """
    project_dir = Path(project_dir).resolve()
    if not source_dir:
        source_dir = Path.home() / "Downloads"
    else:
        source_dir = Path(source_dir).resolve()

    if not source_dir.exists():
        print(f"[Error] Source directory {source_dir} not found.")
        return

    supported_exts = ['.png', '.jpg', '.jpeg', '.webp']
    target_dir = project_dir / "slides"
    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    # Detect existing slide extension in project if not specified
    if not ext:
        existing_slides = list(target_dir.glob("slide_01.*")) if target_dir.exists() else []
        if existing_slides:
            ext = existing_slides[0].suffix.lower()
        else:
            ext = ".jpg"  # Default project standard for long-form
    if not ext.startswith('.'):
        ext = '.' + ext

    # Find matching files in source
    files = [f for f in source_dir.iterdir() if f.is_file() and f.suffix.lower() in supported_exts]
    
    # Sort by creation time on Windows, fallback to mtime
    def file_sort_key(p):
        stat = p.stat()
        return getattr(stat, 'st_ctime', stat.st_mtime)

    files.sort(key=file_sort_key, reverse=True)

    storyboard_file = project_dir / "storyboard.json"
    num_cuts = 0
    if storyboard_file.exists():
        try:
            with open(storyboard_file, 'r', encoding='utf-8') as f:
                sb = json.load(f)
            num_cuts = len(sb.get("cuts", []))
        except Exception:
            pass

    if count is not None:
        count_to_take = count
    elif num_cuts > 0 and len(files) >= num_cuts:
        count_to_take = num_cuts
    else:
        count_to_take = len(files)

    selected = files[:count_to_take]
    selected.reverse()  # Chronological order: oldest downloaded first -> slide_01

    prefix = "[DRY-RUN] " if dry_run else ""
    print(f"\n{prefix}Ingesting {len(selected)} slide images into {target_dir} (target extension: {ext}):")
    print(f"{'#':<4} {'Source File':<40} -> {'Target File':<20}")
    print("-" * 68)

    for idx, src_file in enumerate(selected, start=1):
        target_name = f"slide_{idx:02d}{ext}"
        target_path = target_dir / target_name
        print(f"{idx:<4} {src_file.name[:38]:<40} -> {target_name:<20}")
        if not dry_run:
            shutil.copy2(src_file, target_path)
            if delete_source:
                src_file.unlink()

    if dry_run:
        print(f"\n[DRY-RUN COMPLETE] Plan verified for {len(selected)} slides. Run without --dry-run to execute.")
    else:
        print(f"\n[INGESTION_COMPLETE] Ingested {len(selected)} slides into: {target_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Comic Studio Pipeline Automator")
    parser.add_argument("project_dir", help="Path to project episode directory")
    parser.add_argument("--init-status", action="store_true", help="Initialize status tracker")
    parser.add_argument("--ingest-master-assets", action="store_true", help="Auto-ingest downloaded master references into master_assets/")
    parser.add_argument("--ingest-slides", action="store_true", help="Auto-ingest downloaded scene slides into slides/")
    parser.add_argument("--source-dir", default=None, help="Custom folder for ingestion (defaults to Downloads)")
    parser.add_argument("--dry-run", action="store_true", help="Preview renaming without copying files")
    parser.add_argument("--ext", default=None, help="Force target extension (.jpg, .png, .webp)")
    parser.add_argument("--count", type=int, default=None, help="Number of newest images to ingest")
    parser.add_argument("--delete-source", action="store_true", help="Delete source files after successful copy")
    args = parser.parse_args()

    if args.init_status or not (Path(args.project_dir) / "status.json").exists():
        init_episode_status(args.project_dir)
        
    if args.ingest_master_assets:
        ingest_master_assets(args.project_dir, args.source_dir)

    if args.ingest_slides:
        ingest_slides(
            args.project_dir,
            source_dir=args.source_dir,
            dry_run=args.dry_run,
            ext=args.ext,
            delete_source=args.delete_source,
            count=args.count
        )
