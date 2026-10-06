import os
import time
from pathlib import Path
import subprocess
from google import genai
from google.genai import types

def main():
    # Load .env
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k] = v

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env")

    client = genai.Client(api_key=api_key)

    script_path = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/script_upgraded.txt")
    with open(script_path, "r", encoding="utf-8") as f:
        full_text = f.read().strip()

    lines = [l.strip() for l in full_text.split("\n") if l.strip()]

    # 3 natural acts
    act1 = "\n".join(lines[0:15])
    act2 = "\n".join(lines[15:26])
    act3 = "\n".join(lines[26:])

    acts = [("act1", act1), ("act2", act2), ("act3", act3)]
    out_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/audio/google_tts")
    out_dir.mkdir(parents=True, exist_ok=True)

    act_files = []
    for name, act_text in acts:
        print(f"Generating {name} ({len(act_text.split())} words) with Ludo...")
        prompt = f"Read with calm, conversational, natural storytelling cadence, like an older brother sharing quiet wisdom with natural pauses:\n\n{act_text}"
        
        res = client.models.generate_content(
            model="gemini-3.8-flash-tts",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Ludo")
                    )
                )
            )
        )
        data = res.candidates[0].content.parts[0].inline_data.data
        out_file = out_dir / f"{name}_ludo.wav"
        with open(out_file, "wb") as f:
            f.write(data)
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(out_file)]).decode().strip())
        print(f"  Done {name}: {dur:.2f}s ({len(data)} bytes)")
        act_files.append(out_file)
        print("  Sleeping 5s to strictly respect Google rate limits...")
        time.sleep(5)

    # Concatenate all 3 acts
    concat_list = out_dir / "concat_acts.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for af in act_files:
            f.write(f"file '{af.name}'\n")

    master_out = out_dir / "master_narration_ludo.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(master_out)], check=True)
    master_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(master_out)]).decode().strip())
    print(f"\n=== SUCCESS! Master audio created: {master_out} ({master_dur:.2f}s) ===")

if __name__ == "__main__":
    main()
