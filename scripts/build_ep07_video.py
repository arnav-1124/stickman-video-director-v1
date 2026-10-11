import os
import subprocess
import shutil
from pathlib import Path

def main():
    base_dir = Path("f:/Arnav - YT/stickman-video-director").resolve()
    ep_dir = base_dir / "projects" / "sticky_in_dark" / "shorts" / "ep07_dopamine_is_not_what_you_think"
    raw_video = base_dir / "remotion" / "out_ep07_raw.mp4"
    vo_file = ep_dir / "audio" / "master_voiceover.wav"
    bgm_file = base_dir / "assets" / "bgm" / "dark_contemplation.mp3"
    ass_file = ep_dir / "subtitles.ass"
    out_master = ep_dir / "DOPAMINE_IS_NOT_WHAT_YOU_THINK_MASTER.mp4"
    renders_dir = base_dir / "renders" / "shorts" / "ep07_dopamine_is_not_what_you_think"
    renders_dir.mkdir(parents=True, exist_ok=True)
    out_render = renders_dir / "DOPAMINE_IS_NOT_WHAT_YOU_THINK_MASTER.mp4"

    if not raw_video.exists():
        raise FileNotFoundError(f"Raw Remotion render not found: {raw_video}")

    print("[1/3] Preparing exact FFmpeg mastering pipeline for Ep 07...")

    # Complex filter for video + audio:
    # Video: burn ASS kinetic subtitles cleanly with libass filter
    # Audio: master voiceover at full clarity, BGM at -22dB (volume 0.08), amix, loudnorm -11.9 LUFS
    filter_complex = (
        "[0:v]ass=subtitles.ass[v];"
        "[2:a]volume=0.08,aloop=loop=-1:size=2e+09[bgm];"
        "[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2,"
        "loudnorm=I=-11.9:TP=-1.5:LRA=7.0[a]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(vo_file),
        "-i", str(bgm_file),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[a]",
        "-t", "52.50",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-movflags", "+faststart",
        str(out_master)
    ]

    print("[2/3] Rendering Master Short with Subtitles & Sound Design...")
    # Run with Cwd set to ep_dir so libass can locate subtitles.ass cleanly
    res = subprocess.run(cmd, cwd=str(ep_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if res.returncode != 0:
        print("FFmpeg Error:\n", res.stderr[-2000:])
        raise RuntimeError("FFmpeg rendering failed!")

    print("[3/3] Copying to master renders directory...")
    shutil.copy2(str(out_master), str(out_render))

    # Verify duration and integrity
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size",
        "-of", "default=noprint_wrappers=1",
        str(out_master)
    ]
    probe_res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, text=True).stdout.strip()
    print("\n[SUCCESS] Render Complete!")
    print(f"Master Output: {out_master}")
    print(f"Render Output: {out_render}")
    print(probe_res)

if __name__ == "__main__":
    main()
