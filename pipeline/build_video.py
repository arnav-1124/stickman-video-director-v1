import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

def get_media_info(file_path):
    """Probes media file with ffprobe to extract width, height, duration, and audio presence."""
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'stream=width,height,codec_type,duration:format=duration',
        '-of', 'json',
        str(file_path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    data = json.loads(result.stdout)
    
    width = 1080
    height = 1920
    has_audio = False
    duration = float(data.get('format', {}).get('duration', 0.0))
    
    for s in data.get('streams', []):
        if s.get('codec_type') == 'video':
            width = int(s.get('width', width))
            height = int(s.get('height', height))
            if 'duration' in s:
                try:
                    duration = max(duration, float(s['duration']))
                except ValueError:
                    pass
        elif s.get('codec_type') == 'audio':
            has_audio = True
            
    return width, height, duration, has_audio

def run_ffmpeg(command):
    """Executes FFmpeg command and handles errors with clear diagnostic output."""
    cmd_str = ' '.join(command)
    print(f"[FFmpeg] Executing: {cmd_str[:120]}...")
    try:
        proc = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return proc
    except subprocess.CalledProcessError as e:
        print(f"\n[FFmpeg Error]:\n{e.stderr.decode('utf-8', errors='ignore')}")
        sys.exit(1)

def escape_ffmpeg_path(path):
    """Escapes Windows path for FFmpeg filter syntax."""
    p_str = str(Path(path).resolve()).replace('\\', '/')
    return p_str.replace(':', r'\:')

def build_video(manifest_path, burn_subtitles=True, clean_cache=True, target_aspect=None):
    """
    Studio-Grade FFmpeg Assembler:
    - Normalizes AI video clips to 30fps, 1080p, yuv420p
    - Smart aspect ratio handling (9:16 Shorts or 16:9 Widescreen)
    - Concat demuxer assembly
    - Voiceover + BGM ducking (-14 LUFS loudness standard)
    - Burns kinetic word-level highlighted ASS subtitles
    - Saves final production copy into renders/
    """
    manifest_path = Path(manifest_path).resolve()
    if not manifest_path.exists():
        print(f"[Error] Manifest not found: {manifest_path}")
        sys.exit(1)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    project_dir = manifest_path.parent
    root_dir = project_dir.parent.parent
    project_id = manifest.get('project_id', project_dir.name)

    # Determine target resolution
    aspect = target_aspect or manifest.get('aspect_ratio', '9:16')
    is_vertical = (aspect == "9:16")
    target_w = 1080 if is_vertical else 1920
    target_h = 1920 if is_vertical else 1080
    
    output_file = project_dir / f"{project_id}_final.mp4"
    renders_dir = root_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)
    render_copy_file = renders_dir / f"{project_id}_final.mp4"

    temp_dir = root_dir / ".build_cache" / project_id
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=======================================================")
    print(f"  STICKMAN STUDIO VIDEO BUILDER: {project_id}")
    print(f"  Target Format: {aspect} ({target_w}x{target_h} @ 30fps)")
    print(f"=======================================================\n")

    # Step 1: Pre-process each raw clip
    print("--- Step 1: Pre-processing & Framing Clips ---")
    clips = manifest.get('clips', [])
    if not clips:
        # Auto-discover raw clips if none listed in manifest
        raw_dir = project_dir / "raw"
        raw_files = sorted(raw_dir.glob("shot_*.mp4"))
        if not raw_files:
            print(f"[Error] No clips specified in manifest and no shot_*.mp4 files found in {raw_dir}")
            sys.exit(1)
        clips = [{'file_path': str(f)} for f in raw_files]

    processed_clips = []
    for i, clip in enumerate(clips):
        raw_p = Path(clip['file_path'])
        input_path = raw_p if raw_p.is_absolute() else (project_dir / raw_p).resolve()

        if not input_path.exists():
            print(f"[Error] Clip {i+1} not found: {input_path}")
            sys.exit(1)

        is_image = input_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']
        if is_image:
            duration = float(clip.get('duration', 1.5))
            has_audio = False
            width, height, _, _ = get_media_info(input_path)
        else:
            width, height, duration, has_audio = get_media_info(input_path)
            
        processed_path = temp_dir / f"clip_{i:02d}.mp4"

        # Duration trimming / looping
        trim_args = []
        image_input_args = []
        if is_image:
            image_input_args = ['-loop', '1']
            trim_args = ['-t', str(duration)]
        elif 'duration' in clip and float(clip['duration']) > 0:
            trim_args = ['-t', str(clip['duration'])]

        # Audio strategy
        extra_inputs = []
        audio_args = ['-c:a', 'aac', '-b:a', '192k', '-ar', '44100'] if has_audio else []
        if not has_audio:
            extra_inputs = ['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100']
            audio_args = ['-c:a', 'aac', '-b:a', '192k', '-shortest']

        # Framing filter
        if is_vertical:
            if height >= width:
                # Vertical clip scaling cleanly into 1080x1920
                vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30"
                cmd = [
                    'ffmpeg', '-y', *image_input_args, '-i', str(input_path), *extra_inputs, *trim_args,
                    '-vf', vf,
                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
                    *audio_args, str(processed_path)
                ]
            else:
                # Widescreen clip into vertical -> blurred studio backdrop
                complex_filter = (
                    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5,eq=brightness=-0.15[bg];"
                    "[0:v]scale=1080:-1[fg];"
                    "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=30[v_out]"
                )
                cmd = [
                    'ffmpeg', '-y', *image_input_args, '-i', str(input_path), *extra_inputs, *trim_args,
                    '-filter_complex', complex_filter,
                    '-map', '[v_out]', '-map', '0:a' if has_audio else '1:a',
                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
                    *audio_args, str(processed_path)
                ]
        else:
            if width >= height:
                # Widescreen clip scaling cleanly into 1920x1080
                vf = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=30"
                cmd = [
                    'ffmpeg', '-y', *image_input_args, '-i', str(input_path), *extra_inputs, *trim_args,
                    '-vf', vf,
                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
                    *audio_args, str(processed_path)
                ]
            else:
                # Vertical clip into widescreen -> blurred backdrop
                complex_filter = (
                    "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=25:5,eq=brightness=-0.15[bg];"
                    "[0:v]scale=-1:1080[fg];"
                    "[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=30[v_out]"
                )
                cmd = [
                    'ffmpeg', '-y', *image_input_args, '-i', str(input_path), *extra_inputs, *trim_args,
                    '-filter_complex', complex_filter,
                    '-map', '[v_out]', '-map', '0:a' if has_audio else '1:a',
                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
                    *audio_args, str(processed_path)
                ]

        run_ffmpeg(cmd)
        processed_clips.append(processed_path)
        print(f"  ✓ Processed clip {i+1}/{len(clips)}: {input_path.name}")

    # Step 2: Concatenate processed clips
    print("\n--- Step 2: Concatenating Processed Clips ---")
    concat_list_file = temp_dir / "concat_list.txt"
    with open(concat_list_file, 'w', encoding='utf-8') as f:
        for p in processed_clips:
            f.write(f"file '{p.resolve()}'\n")

    concat_video_path = temp_dir / "concatenated.mp4"
    run_ffmpeg([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', str(concat_list_file),
        '-c', 'copy',
        str(concat_video_path)
    ])
    print(f"  ✓ Concatenated sequence built: {concat_video_path.name}")

    # Step 3: Compositing & Audio Mixing & Subtitle Burning
    print("\n--- Step 3: Audio Mastering & Subtitle Burning ---")
    voiceover_path = manifest.get('voiceover_track') or manifest.get('audio_track')
    if voiceover_path:
        vo_p = Path(voiceover_path)
        voiceover_path = vo_p if vo_p.is_absolute() else (project_dir / vo_p).resolve()

    bgm_path = manifest.get('bgm_track')
    if bgm_path:
        bg_p = Path(bgm_path)
        bgm_path = bg_p if bg_p.is_absolute() else (project_dir / bg_p).resolve()

    # Subtitles
    subtitles_path = project_dir / ("subtitles.ass" if is_vertical else "subtitles_16x9.ass")
    if not subtitles_path.exists() and (project_dir / "subtitles.ass").exists():
        subtitles_path = project_dir / "subtitles.ass"

    filter_chains = []
    if burn_subtitles and subtitles_path.exists():
        escaped_sub = escape_ffmpeg_path(subtitles_path)
        filter_chains.append(f"ass='{escaped_sub}'")
        print(f"  ✓ Burning kinetic subtitles: {subtitles_path.name}")

    # Determine audio routing
    inputs = ['-i', str(concat_video_path)]
    filter_complex_parts = []
    
    if filter_chains:
        filter_complex_parts.append(f"[0:v]{','.join(filter_chains)}[v_out]")

    if voiceover_path and voiceover_path.exists():
        inputs.extend(['-i', str(voiceover_path)])
        vo_idx = len(inputs) // 2 - 1  # 1

        if bgm_path and bgm_path.exists():
            inputs.extend(['-i', str(bgm_path)])
            bgm_idx = len(inputs) // 2 - 1  # 2
            # Studio sidechain ducking: BGM ducks when voiceover speaks + loudnorm -14 LUFS
            audio_filter = (
                f"[{vo_idx}:a]asplit=2[vo_main][vo_trigger];"
                f"[{bgm_idx}:a]volume=0.18[bgm];"
                f"[bgm][vo_trigger]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=400[ducked_bgm];"
                f"[vo_main][ducked_bgm]amix=inputs=2:duration=first:normalize=0[mixed_a];"
                f"[mixed_a]loudnorm=I=-14:LRA=7:tp=-1[a_out]"
            )
            filter_complex_parts.append(audio_filter)
        else:
            # Voiceover only + loudnorm
            filter_complex_parts.append(f"[{vo_idx}:a]loudnorm=I=-14:LRA=7:tp=-1[a_out]")
    elif bgm_path and bgm_path.exists():
        inputs.extend(['-i', str(bgm_path)])
        bgm_idx = len(inputs) // 2 - 1
        # Studio sidechain ducking: BGM ducks when native speech in [0:a] speaks + loudnorm -14 LUFS
        audio_filter = (
            f"[0:a]asplit=2[vo_main][vo_trigger];"
            f"[{bgm_idx}:a]volume=0.12[bgm];"
            f"[bgm][vo_trigger]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=400[ducked_bgm];"
            f"[vo_main][ducked_bgm]amix=inputs=2:duration=first:normalize=0[mixed_a];"
            f"[mixed_a]loudnorm=I=-14:LRA=7:tp=-1[a_out]"
        )
        filter_complex_parts.append(audio_filter)
    else:
        # Normalize native concat audio
        filter_complex_parts.append("[0:a]loudnorm=I=-14:LRA=7:tp=-1[a_out]")

    final_cmd = ['ffmpeg', '-y', *inputs]
    if filter_complex_parts:
        final_cmd.extend(['-filter_complex', ';'.join(filter_complex_parts)])
        final_cmd.extend(['-map', '[v_out]' if filter_chains else '0:v'])
        final_cmd.extend(['-map', '[a_out]'])
    else:
        final_cmd.extend(['-c:v', 'copy', '-c:a', 'copy'])

    final_cmd.extend([
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '192k',
        str(output_file)
    ])

    run_ffmpeg(final_cmd)

    # Copy to renders
    shutil.copy2(output_file, render_copy_file)

    if clean_cache and temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"[Cleanup] Removed intermediate build cache: {temp_dir}")

    print(f"\n=======================================================")
    print(f"✓ Production Build Complete!")
    print(f"   Episode File: {output_file}")
    print(f"   Render Vault: {render_copy_file}")
    print(f"=======================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Studio-Grade Stickman / Ink Explainer Video Builder")
    parser.add_argument("manifest", help="Path to build_manifest.json")
    parser.add_argument("--aspect", choices=["9:16", "16:9"], default=None, help="Force aspect ratio")
    parser.add_argument("--no-subs", action="store_true", help="Skip burning subtitles")
    parser.add_argument("--keep-cache", action="store_true", help="Keep intermediate build cache")
    args = parser.parse_args()

    build_video(
        args.manifest, 
        burn_subtitles=not args.no_subs, 
        clean_cache=not args.keep_cache,
        target_aspect=args.aspect
    )
