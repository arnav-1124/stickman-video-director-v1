# Headless Automation & Preview Flag Rule

## 1. Mandatory `--preview` Flag
Every production run must support a fast dry-run inspection mode:
```bash
python pipeline/run_short.py --topic "The Paradox of Choice" --preview
```

## 2. Dry-Run Output
- Prints full 5-beat script with word counts.
- Displays estimated duration and beat breakdown.
- Previews visual stickman choreography cues.
- Executes in under 5 seconds with zero GPU/render compute cost.
