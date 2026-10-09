import os
import subprocess
import shutil
from pathlib import Path

def main():
    base_dir = Path("f:/Arnav - YT/stickman-video-director").resolve()
    ep_dir = base_dir / "projects" / "sticky_in_dark" / "shorts" / "ep06_when_you_make_eye_contact_in_public"
    concat_file = ep_dir / "concat_ep06.txt"
    vo_file = ep_dir / "audio" / "master_voiceover.wav"
    bgm_file = base_dir / "assets" / "bgm" / "dark_contemplation.mp3"
    ass_file = ep_dir / "subtitles.ass"
    out_master = ep_dir / "WHEN_YOU_MAKE_EYE_CONTACT_IN_PUBLIC_MASTER.mp4"
    renders_dir = base_dir / "renders" / "shorts" / "ep06_when_you_make_eye_contact_in_public"
    renders_dir.mkdir(parents=True, exist_ok=True)
    out_render = renders_dir / "WHEN_YOU_MAKE_EYE_CONTACT_IN_PUBLIC_MASTER.mp4"

    print("[1/3] Preparing exact FFmpeg command...")

    # Complex filter for video + audio
    # Video: scale to 1080x1920 on cream canvas (#FAF9F6), burn ASS subtitles, 30fps
    # Audio: Voiceover at full volume, BGM at -22dB (0.08 volume), amix, loudnorm to -11.9 LUFS
    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0xFAF9F6,"
        "fps=30,"
        "ass=subtitles.ass[v];"
        "[2:a]volume=0.08,aloop=loop=-1:size=2e+09[bgm];"
        "[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2,"
        "loudnorm=I=-11.9:TP=-1.5:LRA=7.0[a]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", "concat_ep06.txt",
        "-i", str(vo_file),
        "-i", str(bgm_file),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[a]",
        "-t", "49.54",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-movflags", "+faststart",
        str(out_master)
    ]

    print("[2/3] Rendering Master Short MP4...")
    # Run with Cwd set to ep_dir so libass can locate subtitles.ass cleanly
    res = subprocess.run(cmd, cwd=str(ep_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if res.returncode != 0:
        print("FFmpeg Error:\n", res.stderr[-2000:])
        raise RuntimeError("FFmpeg rendering failed!")

    print("[3/3] Copying to renders directory...")
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
