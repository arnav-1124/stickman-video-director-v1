import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import json
import math
import subprocess
import shutil
from pathlib import Path

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - math.floor(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def parse_ass_time(time_str):
    parts = time_str.strip().split(':')
    h = int(parts[0])
    m = int(parts[1])
    s_parts = parts[2].split('.')
    s = int(s_parts[0])
    cs = int(s_parts[1])
    return h * 3600 + m * 60 + s + cs / 100.0

def escape_ffmpeg_path(path):
    p_str = str(Path(path).resolve()).replace('\\', '/')
    return p_str.replace(':', r'\:')

def main():
    root_dir = Path(".").resolve()
    project_dir = root_dir / "projects" / "ep04_why_girls_like_silent_boy"
    manifest_path = project_dir / "build_manifest.json"
    words_path = project_dir / "audio" / "word_timestamps.json"
    vo_path = project_dir / "audio" / "voiceover.mp3"
    bgm_path = root_dir / "assets" / "bgm" / "dark_contemplation.mp3"
    subtitles_path = project_dir / "subtitles.ass"
    slides_dir = project_dir / "slides"
    renders_dir = root_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)

    print("--- [1/5] Calculating frame-perfect cut timings for 36 slides ---")
    manifest = json.load(open(manifest_path, encoding="utf-8"))
    words = json.load(open(words_path, encoding="utf-8"))

    cut_starts = []
    w_idx = 0
    for cut in manifest["clips"][:37]:  # up to 37 so we know where 36 ends
        text_words = cut["text"].strip().split()
        first_w = text_words[0] if text_words else ""
        matched_time = None
        for j in range(w_idx, len(words)):
            clean_text_w = "".join(ch for ch in first_w.lower() if ch.isalnum())
            clean_audio_w = "".join(ch for ch in words[j]["word"].lower() if ch.isalnum())
            if clean_text_w and clean_text_w == clean_audio_w:
                matched_time = words[j]["start_sec"]
                w_idx = j + len(text_words)
                break
        cut_starts.append((cut["cut_id"], matched_time, cut["text"]))

    exact_clips = []
    for i in range(36):
        cid, start_t, text = cut_starts[i]
        next_cid, next_t, _ = cut_starts[i+1]
        actual_start = 0.0 if i == 0 else start_t
        dur = round(next_t - actual_start, 3)
        exact_clips.append({
            "cut_id": cid,
            "start": actual_start,
            "end": next_t,
            "duration": dur,
            "text": text,
            "slide_file": slides_dir / f"slide_{cid:02d}.jpg"
        })

    total_test_dur = exact_clips[-1]["end"]
    print(f"  ✓ Total Animation Test Duration: {total_test_dur:.2f}s across 36 slides")

    # Verify all 36 slides exist
    for c in exact_clips:
        if not c["slide_file"].exists():
            raise FileNotFoundError(f"Missing slide: {c['slide_file']}")

    print("--- [2/5] Creating image concat list ---")
    concat_txt_path = project_dir / "concat_test_36.txt"
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for c in exact_clips:
            resolved_p = str(c["slide_file"].resolve()).replace("\\", "/")
            f.write(f"file '{resolved_p}'\n")
            f.write(f"duration {c['duration']:.3f}\n")
        # Concat demuxer requirement: repeat last image without duration
        last_p = str(exact_clips[-1]["slide_file"].resolve()).replace("\\", "/")
        f.write(f"file '{last_p}'\n")
    print(f"  ✓ Wrote concat manifest: {concat_txt_path.name}")

    print("--- [3/5] Trimming kinetic ASS subtitles to 60.32s ---")
    sub_lines = subtitles_path.read_text(encoding="utf-8").splitlines()
    trimmed_subs = []
    for line in sub_lines:
        if line.startswith("Dialogue:"):
            # Dialogue: Layer, Start, End, Style...
            parts = line.split(",", 9)
            start_sec = parse_ass_time(parts[1])
            end_sec = parse_ass_time(parts[2])
            if start_sec >= total_test_dur:
                continue
            if end_sec > total_test_dur:
                parts[2] = format_ass_time(total_test_dur)
            trimmed_subs.append(",".join(parts))
        else:
            trimmed_subs.append(line)

    test_sub_path = project_dir / "subtitles_test_36.ass"
    test_sub_path.write_text("\n".join(trimmed_subs), encoding="utf-8")
    print(f"  ✓ Subtitles ready: {test_sub_path.name} ({len([l for l in trimmed_subs if l.startswith('Dialogue:')])} lines)")

    print("--- [4/5] Preparing Audio: Trimming VO & Sidechain Ducking BGM ---")
    out_test_mp4 = project_dir / "ep04_test_36_slides.mp4"
    render_test_mp4 = renders_dir / "ep04_test_36_slides.mp4"

    escaped_sub = escape_ffmpeg_path(test_sub_path)
    
    # Filter complex explanation:
    # 0:v - Image sequence via concat demuxer scaled & cropped to 1080x1920 @ 30fps
    # Burn ASS subtitles directly onto the video
    # 1:a - Voiceover trimmed to total_test_dur with fadeout
    # 2:a - BGM looped, ducked under VO when VO speaks, then mixed and normalized
    
    fade_start = total_test_dur - 0.35
    video_filter = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,ass='{escaped_sub}'[v_out]"
    
    audio_filter = (
        f"[1:a]atrim=0:{total_test_dur},afade=t=out:st={fade_start:.2f}:d=0.35[vo_trimmed];"
        f"[vo_trimmed]asplit=2[vo_main][vo_trigger];"
        f"[2:a]atrim=0:{total_test_dur},volume=0.20,afade=t=out:st={fade_start:.2f}:d=0.35[bgm_trimmed];"
        f"[bgm_trimmed][vo_trigger]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=400[ducked_bgm];"
        f"[vo_main][ducked_bgm]amix=inputs=2:duration=first:normalize=0[mixed_a];"
        f"[mixed_a]loudnorm=I=-14:LRA=7:tp=-1[a_out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt_path),
        "-i", str(vo_path),
        "-stream_loop", "-1", "-i", str(bgm_path),
        "-filter_complex", f"[0:v]{video_filter};{audio_filter}",
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{total_test_dur:.2f}",
        str(out_test_mp4)
    ]

    print(f"--- [5/5] Compiling final 1080x1920 animation preview with FFmpeg ---")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FFmpeg Error]:\n{res.stderr}")
        raise RuntimeError("FFmpeg rendering failed")

    # Copy to renders vault
    shutil.copy2(out_test_mp4, render_test_mp4)

    # Clean intermediate test files
    if (project_dir / "test_concat.txt").exists():
        (project_dir / "test_concat.txt").unlink()
    if (project_dir / "test_out.mp4").exists():
        (project_dir / "test_out.mp4").unlink()

    print("\n=======================================================")
    print(f"🎉 36-SLIDE TEST ANIMATION COMPILED SUCCESSFULLY!")
    print(f"   Project File: {out_test_mp4}")
    print(f"   Render Vault: {render_test_mp4}")
    print(f"   Duration:     {total_test_dur:.2f} seconds")
    print(f"   Resolution:   1080x1920 (9:16 Vertical)")
    print(f"   Audio:        -14 LUFS Mastered with BGM & Voiceover")
    print(f"   Subtitles:    Kinetic Gold Highlighted ASS burned in")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
