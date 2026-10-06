import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import argparse
import json
import os
import subprocess
from pathlib import Path

def find_repo_root(start_dir):
    curr = Path(start_dir).resolve()
    while curr.parent != curr:
        if (curr / ".git").exists() or (curr / "pipeline").exists():
            return curr
        curr = curr.parent
    return Path(start_dir).resolve()

def make_episode(project_dir, skip_tts=False, skip_subs=False, micro_motion=False, dry_run=False, aspect="16:9"):
    """
    Unified Master Pipeline Orchestrator:
    Chains audio verification -> subtitle generation -> manifest building -> FFmpeg assembly.
    """
    project_dir = Path(project_dir).resolve()
    if not project_dir.exists():
        print(f"[Error] Project directory not found: {project_dir}")
        sys.exit(1)

    repo_root = find_repo_root(project_dir)
    project_id = project_dir.name
    print(f"\n=======================================================")
    print(f"  🎬 MAKE EPISODE MASTER ORCHESTRATOR: {project_id}")
    print(f"  Target Aspect: {aspect} | Micro-motion: {micro_motion}")
    print(f"=======================================================\n")

    # Step 1: Verify / Generate Audio
    print("--- Step 1: Audio Check ---")
    audio_dir = project_dir / "audio"
    master_audio = None
    if audio_dir.exists():
        # Look for existing master audio
        masters = list(audio_dir.glob("*master*.wav")) + list(audio_dir.glob("*master*.mp3"))
        if masters:
            master_audio = masters[0]
            print(f"  ✓ Found master audio: {master_audio.name}")

    if not master_audio:
        print("  ℹ No master audio file detected in audio/. Checking for script...")
        script_file = project_dir / "script_upgraded.txt"
        if not script_file.exists():
            script_file = project_dir / "script.txt"
        
        if script_file.exists() and not skip_tts:
            print(f"  → Generating Gemini TTS voiceover from {script_file.name}...")
            if not dry_run:
                tts_script = repo_root / "pipeline" / "generate_gemini_tts.py"
                if tts_script.exists():
                    subprocess.run([sys.executable, str(tts_script), str(project_dir)], check=True)
                else:
                    print("  ⚠ TTS script pipeline/generate_gemini_tts.py not found.")
        else:
            print("  ⚠ Step 1 skipped (--skip-tts or no script found).")

    # Step 2: Verify / Generate Subtitles
    print("\n--- Step 2: Subtitles Check ---")
    sub_files = list(project_dir.glob("*.ass"))
    if sub_files:
        print(f"  ✓ Found kinetic subtitle file: {sub_files[0].name}")
    elif not skip_subs:
        print("  → Building subtitles from storyboard & audio...")
        if not dry_run:
            sub_script = repo_root / "pipeline" / "generate_subtitles.py"
            if sub_script.exists():
                subprocess.run([sys.executable, str(sub_script), str(project_dir)], check=False)
    else:
        print("  ⚠ Step 2 skipped (--skip-subs).")

    # Step 3: Build Manifest
    print("\n--- Step 3: Assembling Manifest ---")
    manifest_file = project_dir / "build_manifest.json"
    slides_dir = project_dir / "slides"
    storyboard_file = project_dir / "storyboard.json"

    slides = sorted(list(slides_dir.glob("slide_*.*"))) if slides_dir.exists() else []
    print(f"  ✓ Detected {len(slides)} slide image(s) in {slides_dir.name}/")

    cuts_data = []
    if storyboard_file.exists():
        try:
            with open(storyboard_file, 'r', encoding='utf-8') as f:
                sb = json.load(f)
            cuts_data = sb.get("cuts", [])
        except Exception:
            pass

    clips_list = []
    for i, slide in enumerate(slides):
        duration = 4.5  # default baseline
        if i < len(cuts_data):
            duration = float(cuts_data[i].get("duration", cuts_data[i].get("duration_sec", 4.5)))
        clips_list.append({
            "clip_id": i + 1,
            "file_path": str(slide.relative_to(project_dir)).replace("\\", "/"),
            "duration": duration
        })

    bgm_path = "assets/bgm/dark_contemplation.mp3"
    voice_path = None
    if master_audio:
        voice_path = str(master_audio.relative_to(project_dir)).replace("\\", "/")

    sub_path = str(sub_files[0].relative_to(project_dir)).replace("\\", "/") if sub_files else None

    manifest = {
        "project_id": project_id,
        "aspect_ratio": aspect,
        "voiceover": voice_path,
        "background_music": bgm_path if (repo_root / bgm_path).exists() else None,
        "bgm_volume": 0.08,
        "subtitles": sub_path,
        "clips": clips_list
    }

    if not dry_run:
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        print(f"  ✓ Manifest written to: {manifest_file.name}")
    else:
        print(f"  [DRY-RUN] Manifest preview: {len(clips_list)} clips mapped.")

    # Step 4: Run FFmpeg Assembly
    print("\n--- Step 4: Video Assembly via build_video.py ---")
    if not dry_run:
        build_script = repo_root / "pipeline" / "build_video.py"
        cmd = [sys.executable, str(build_script), str(manifest_file)]
        if aspect:
            cmd.extend(["--aspect", aspect])
        subprocess.run(cmd, check=True)
        print(f"\n[EPISODE BUILD COMPLETE] Deliverable saved for {project_id}.")
    else:
        print("  [DRY-RUN] Assembly command skipped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stickman Studio Episode Build Orchestrator")
    parser.add_argument("project_dir", help="Path to episode project directory")
    parser.add_argument("--skip-tts", action="store_true", help="Skip TTS generation")
    parser.add_argument("--skip-subs", action="store_true", help="Skip subtitle generation")
    parser.add_argument("--micro-motion", action="store_true", help="Enable subtle Ken Burns pan/zoom on slides")
    parser.add_argument("--dry-run", action="store_true", help="Preview pipeline steps without writing files")
    parser.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"], help="Target aspect ratio")
    args = parser.parse_args()

    make_episode(
        args.project_dir,
        skip_tts=args.skip_tts,
        skip_subs=args.skip_subs,
        micro_motion=args.micro_motion,
        dry_run=args.dry_run,
        aspect=args.aspect
    )
