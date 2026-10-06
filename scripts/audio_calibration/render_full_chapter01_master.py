import subprocess
import shutil
from pathlib import Path

def main():
    base_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox")
    renders_dir = base_dir / "renders"
    central_renders_dir = Path("renders/long/ep01_why_people_fall_for_who_ignores_them")
    renders_dir.mkdir(parents=True, exist_ok=True)
    central_renders_dir.mkdir(parents=True, exist_ok=True)

    concat_file = base_dir / "concat_master.txt"
    logo_file = Path("assets/branding/channel_logo.png")
    mastered_wav = base_dir / "audio" / "ch01_full_master_narration_mastered.wav"
    bgm_file = Path("assets/bgm/dark_contemplation.mp3")
    sub_file = base_dir / "subtitles_16_9.ass"

    # Destination master film
    out_master_mp4 = renders_dir / "YOU_REPLIED_INSTANTLY_Chapter_01_MASTER.mp4"
    central_master_mp4 = central_renders_dir / "YOU_REPLIED_INSTANTLY_Chapter_01_MASTER.mp4"

    # Export full MP3 for Chapter 1
    out_master_mp3 = base_dir / "audio" / "ch01_master_ludo_full.mp3"
    print("Exporting high-bitrate master MP3...")
    subprocess.run([
        "ffmpeg", "-y", "-i", str(mastered_wav),
        "-c:a", "libmp3lame", "-b:a", "320k", str(out_master_mp3)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Exported: {out_master_mp3}")

    total_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(mastered_wav)
    ]).decode().strip())
    print(f"Master Duration: {total_dur:.2f}s ({total_dur/60:.2f} minutes)")

    filter_complex = (
        "[0:v]fps=25,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_fps];"
        "[1:v]scale=110:110[logo];"
        "[v_fps][logo]overlay=1800:960[v_masked];"
        f"[v_masked]subtitles={sub_file.as_posix()}[v_out];"
        f"[3:a]volume=0.08,afade=t=in:st=0:d=2.0,afade=t=out:st={total_dur-3.0:.2f}:d=3.0[bgm_ducked];"
        "[2:a][bgm_ducked]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(logo_file.resolve()),
        "-i", str(mastered_wav.resolve()),
        "-stream_loop", "-1", "-i", str(bgm_file.resolve()),
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k",
        "-t", f"{total_dur:.3f}",
        str(out_master_mp4)
    ]

    print("Rendering FULL Chapter 1 Master Film (153.64s / 2.5 minutes)...")
    subprocess.run(cmd, check=True)
    
    # Copy to central renders
    shutil.copyfile(out_master_mp4, central_master_mp4)
    
    print(f"\n[DONE] Rendered Full Master Film:")
    print(f"  Chapter 1: {out_master_mp4} ({out_master_mp4.stat().st_size / (1024*1024):.2f} MB)")
    print(f"  Central:   {central_master_mp4} ({central_master_mp4.stat().st_size / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
