import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import os
import math
import json
import shutil
import subprocess
from pathlib import Path

pipeline_dir = Path(__file__).resolve().parent
if str(pipeline_dir) not in sys.path:
    sys.path.insert(0, str(pipeline_dir))

from calculate_exact_timeline import get_exact_slide_cuts
from generate_exact_subtitles import build_subtitles

def escape_ffmpeg_path(path):
    p_str = str(Path(path).resolve()).replace('\\', '/')
    return p_str.replace(':', r'\:')

def main():
    root_dir = Path(".").resolve()
    ep_dir = root_dir / "projects/long/ep02_how_humans_invented_the_first_lie"
    slides_dir = ep_dir / "slides"
    storyboard_file = ep_dir / "storyboard.json"
    audio_wav = ep_dir / "audio/voiceover_038s_calibrated.wav"
    words_file = ep_dir / "audio/exact_word_timestamps.json"
    bgm_file = root_dir / "assets/bgm/dark_contemplation.mp3"
    logo_file = root_dir / "assets/branding/channel_logo.png"

    project_renders = ep_dir / "renders"
    central_renders = root_dir / "renders/long/ep02_how_humans_invented_the_first_lie"
    project_renders.mkdir(parents=True, exist_ok=True)
    central_renders.mkdir(parents=True, exist_ok=True)

    out_mp4 = project_renders / "HOW_HUMANS_INVENTED_THE_FIRST_LIE_MASTER.mp4"
    central_mp4 = central_renders / "HOW_HUMANS_INVENTED_THE_FIRST_LIE_MASTER.mp4"

    temp_dir = root_dir / "temp/ep02_assembly"
    temp_dir.mkdir(parents=True, exist_ok=True)

    print("==================================================================")
    print("  EXACT STUDIO MASTER ASSEMBLY: Ep02 How Humans Invented the First Lie")
    print("  62 Slides | 16:9 (1920x1080) | 100% Math & Code Audio Synced   ")
    print("==================================================================\n")

    # 1. Load exact slide timeline
    cuts = get_exact_slide_cuts()
    print(f"Loaded {len(cuts)} exact mathematical slide cuts.")

    for filename, st, en, note in cuts:
        slide_p = slides_dir / filename
        if not slide_p.exists():
            print(f"[Error] Missing slide: {slide_p}")
            sys.exit(1)
    print(f"✓ Verified: All {len(cuts)} slides exist 1:1.\n")

    # 2. Probe audio duration
    audio_dur = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_wav)
    ]).decode().strip())
    print(f"Calibrated Voiceover Audio Duration: {audio_dur:.3f}s")

    # 3. Build Concat Manifest for FFmpeg using exact calculated durations
    concat_txt = temp_dir / "video_concat_62.txt"
    total_calculated_dur = 0.0
    with open(concat_txt, "w", encoding="utf-8") as f:
        for filename, st, en, note in cuts:
            dur = en - st
            total_calculated_dur += dur
            slide_p = slides_dir / filename
            f.write(f"file '{slide_p.resolve().as_posix()}'\n")
            f.write(f"duration {dur:.3f}\n")
        # Final image repeat for ffmpeg concat demuxer bug prevention
        last_slide = slides_dir / cuts[-1][0]
        f.write(f"file '{last_slide.resolve().as_posix()}'\n")

    print(f"✓ Video Concat Manifest generated ({total_calculated_dur:.3f}s total across {len(cuts)} visual cuts).")

    # 4. Generate Exact Kinetic ASS Subtitles from Whisper Word Timestamps
    print("\nGenerating Kinetic ASS Subtitles from exact millisecond word timestamps...")
    with open(words_file, "r", encoding="utf-8") as f:
        words = json.load(f)

    sub_file = ep_dir / "subtitles_16_9.ass"
    ass_content = build_subtitles(words, cuts, show_on_markers=False)
    with open(sub_file, "w", encoding="utf-8") as f:
        f.write(ass_content)
    print(f"✓ Generated exact kinetic subtitles: {sub_file.name}")

    # 5. Master Narration Audio (EQ + Compand + Loudnorm to -11.9 LUFS)
    mastered_wav = temp_dir / "ep02_narration_mastered.wav"
    print("\nMastering narration with Studio EQ, Compand & Loudnorm (-11.9 LUFS)...")
    dsp = (
        "equalizer=f=115:width_type=o:w=1.2:g=3.5,"
        "equalizer=f=250:width_type=o:w=1.0:g=1.8,"
        "equalizer=f=3500:width_type=o:w=1.2:g=2.2,"
        "compand=attacks=0.01:decays=0.08:points=-80/-80|-30/-14|-10/-5|0/-1:soft-knee=6,"
        "loudnorm=I=-11.9:TP=-1.0:LRA=6.0,"
        "aresample=48000"
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(audio_wav),
        "-af", dsp, str(mastered_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✓ Audio mastering complete (-11.9 LUFS).")

    # 6. Compose Video Filter Complex
    print("\nBuilding FFmpeg Filter Complex (1920x1080 30fps + Subtitles + Logo + BGM Bed)...")
    escaped_sub = escape_ffmpeg_path(sub_file)

    filter_complex = (
        "[0:v]fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[v_scaled];"
        "[1:v]scale=110:110[logo];"
        "[v_scaled][logo]overlay=1800:960[v_branded];"
        f"[v_branded]ass='{escaped_sub}'[v_out];"
        "[2:a]aresample=48000,aformat=channel_layouts=stereo[voice];"
        f"[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.07,afade=t=in:st=0:d=1.5,afade=t=out:st={audio_dur-2.5:.2f}:d=2.5[bgm_bed];"
        "[voice][bgm_bed]amix=inputs=2:duration=first:weights=1.0 1.0[a_out]"
    )

    # Detect encoder (prefer NVENC)
    encoder = "h264_nvenc"
    enc_args = ["-c:v", encoder, "-preset", "p5", "-cq", "19", "-pix_fmt", "yuv420p"]

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-i", str(logo_file.resolve()),
        "-i", str(mastered_wav.resolve()),
        "-stream_loop", "-1", "-i", str(bgm_file.resolve()),
        "-filter_complex", filter_complex,
        "-map", "[v_out]",
        "-map", "[a_out]",
        *enc_args,
        "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
        "-t", f"{audio_dur:.3f}",
        str(out_mp4)
    ]

    print(f"Executing FFmpeg render using {encoder}...")
    try:
        proc = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("\n[NVENC fallback] Trying CPU libx264...")
        enc_args = ["-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p"]
        idx = cmd.index("-c:v")
        cmd[idx:idx + 6] = enc_args
        subprocess.run(cmd, check=True)

    # 7. Copy to central render vault
    shutil.copyfile(out_mp4, central_mp4)

    file_size_mb = out_mp4.stat().st_size / (1024 * 1024)
    print("\n==================================================================")
    print("✓ PRODUCTION MASTER FILM RENDER COMPLETE!")
    print(f"  Episode Render: {out_mp4} ({file_size_mb:.2f} MB)")
    print(f"  Central Vault:  {central_mp4} ({file_size_mb:.2f} MB)")
    print(f"  Total Duration: {audio_dur:.2f}s | Resolution: 1920x1080 @ 30fps")
    print("==================================================================\n")

if __name__ == "__main__":
    main()
