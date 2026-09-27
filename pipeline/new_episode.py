import argparse
import json
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def scaffold_episode(episode_name):
    root_dir = Path(__file__).resolve().parent.parent
    template_dir = root_dir / "projects" / "templates" / "canonical_episode"
    target_dir = root_dir / "projects" / episode_name

    if not template_dir.exists():
        print(f"[Error] Canonical template not found at: {template_dir}")
        sys.exit(1)

    if target_dir.exists():
        print(f"[Warning] Project '{episode_name}' already exists at: {target_dir}")
        return target_dir

    print(f"[Scaffolding] Creating new episode: {episode_name}")
    shutil.copytree(template_dir, target_dir)

    # Ensure required directories exist
    (target_dir / "raw").mkdir(parents=True, exist_ok=True)
    (target_dir / "anchors").mkdir(parents=True, exist_ok=True)
    (target_dir / "audio").mkdir(parents=True, exist_ok=True)

    # Update project_id in JSON template files
    for json_file in target_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict) and "project_id" in data:
                data["project_id"] = episode_name
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
        except Exception:
            pass

    print(f"[SUCCESS] Episode workspace initialized at: {target_dir}")
    print(f"[INFO] Downloaded AI video clips should be placed in: {target_dir / 'raw'}")
    return target_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new stickman/ink-explainer episode.")
    parser.add_argument("--name", type=str, required=True, help="Episode folder name (e.g. ep02_the_silent_killer)")
    args = parser.parse_args()
    scaffold_episode(args.name)
