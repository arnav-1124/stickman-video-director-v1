import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import json
import subprocess
import shutil
from pathlib import Path

def escape_ffmpeg_path(path):
    p_str = str(Path(path).resolve()).replace('\\', '/')
    return p_str.replace(':', r'\:')

def build_english_final():
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

    print("=======================================================")
    print("  BUILDING ENGLISH FINAL: Ep04 Why Girls Like Silent Boy")
    print("  Voice: Christopher (-2Hz, +2%) | Mastered -14 LUFS")
    print("=======================================================\n")

    manifest = json.load(open(manifest_path, encoding="utf-8"))
    words = json.load(open(words_path, encoding="utf-8"))

    # Map all 42 cuts to exact word timestamps
    cut_starts = []
    w_idx = 0
    for cut in manifest["clips"]:
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

    last_word_end = words[-1]["end_sec"] + 0.60
    exact_clips = []
    for i in range(len(cut_starts)):
        cid, start_t, text = cut_starts[i]
        actual_start = 0.0 if i == 0 else start_t
        next_t = cut_starts[i+1][1] if i < len(cut_starts) - 1 else last_word_end
        dur = round(next_t - actual_start, 3)
        exact_clips.append({
            "cut_id": cid,
            "start": actual_start,
            "end": next_t,
            "duration": dur,
            "text": text,
            "slide_file": slides_dir / f"slide_{cid:02d}.jpg"
        })

    total_dur = exact_clips[-1]["end"]
    print(f"✓ Total Duration: {total_dur:.2f}s across 42 slides")

    # Build concat file
    concat_txt_path = project_dir / "concat_en_42.txt"
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for c in exact_clips:
            resolved_p = str(c["slide_file"].resolve()).replace("\\", "/")
            f.write(f"file '{resolved_p}'\n")
            f.write(f"duration {c['duration']:.3f}\n")
        last_p = str(exact_clips[-1]["slide_file"].resolve()).replace("\\", "/")
        f.write(f"file '{last_p}'\n")

    out_project_file = project_dir / "ep04_why_girls_like_silent_boy_final_en.mp4"
    out_render_file = renders_dir / "ep04_why_girls_like_silent_boy_final_en.mp4"

    escaped_sub = escape_ffmpeg_path(subtitles_path)
    fade_start = total_dur - 0.40

    video_filter = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,ass='{escaped_sub}'[v_out]"
    audio_filter = (
        f"[1:a]atrim=0:{total_dur},afade=t=out:st={fade_start:.2f}:d=0.40[vo];"
        f"[vo]asplit=2[vo_main][vo_trigger];"
        f"[2:a]atrim=0:{total_dur},volume=0.20,afade=t=out:st={fade_start:.2f}:d=0.40[bgm];"
        f"[bgm][vo_trigger]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=400[ducked_bgm];"
        f"[vo_main][ducked_bgm]amix=inputs=2:duration=first:normalize=0[mixed];"
        f"[mixed]loudnorm=I=-14:LRA=7:tp=-1[a_out]"
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
        "-t", f"{total_dur:.2f}",
        str(out_project_file)
    ]

    print("[Rendering English Final Video...]")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FFmpeg Error]:\n{res.stderr}")
        raise RuntimeError("English build failed")

    shutil.copy2(out_project_file, out_render_file)
    print(f"✓ English Final Video Built: {out_render_file}")
    return out_render_file

if __name__ == "__main__":
    build_english_final()
