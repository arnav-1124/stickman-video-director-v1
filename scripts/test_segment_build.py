import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CH1_DIR = ROOT_DIR / "projects" / "long" / "ep01_why_people_fall_for_who_ignores_them" / "chapter_01_the_pedestal_paradox"
SLIDES_DIR = CH1_DIR / "slides"
SCRATCH_DIR = ROOT_DIR / "scratch" / "natural_pacing_test"

def test_segment_build():
    segments = []
    for sid in range(1, 5):
        img = SLIDES_DIR / f"slide_{sid:02d}.jpg"
        audio = SCRATCH_DIR / f"shot_{sid:02d}_clean.mp3"
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio)]).decode().strip())
        
        seg_out = SCRATCH_DIR / f"seg_{sid:02d}.mp4"
        vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#FAF9F6,setsar=1,fps=30"
        
        # Build individual shot segment: image loops for exact audio duration
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(img),
            "-i", str(audio),
            "-vf", vf,
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
            "-t", f"{dur:.3f}",
            "-shortest",
            str(seg_out)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        segments.append(seg_out)
        print(f"Segment {sid:02d} rendered: {dur:.3f}s")
        
    # Concat segments
    concat_list = SCRATCH_DIR / "segments_list.txt"
    with open(concat_list, "w") as f:
        for seg in segments:
            f.write(f"file '{seg.as_posix()}'\n")
            
    final_test_video = SCRATCH_DIR / "test_shots_1_to_4_natural.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(final_test_video)
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Inspect final test video
    v_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(final_test_video)]).decode().strip())
    a_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(final_test_video)]).decode().strip())
    print(f"\nFinal Test Video: {final_test_video}")
    print(f"Video Stream Duration: {v_dur:.3f}s")
    print(f"Audio Stream Duration: {a_dur:.3f}s")
    print(f"Sync Difference:       {abs(v_dur - a_dur)*1000:.2f}ms")

if __name__ == "__main__":
    test_segment_build()
