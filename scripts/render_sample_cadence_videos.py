import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CH1_DIR = ROOT_DIR / "projects" / "long" / "ep01_why_people_fall_for_who_ignores_them" / "chapter_01_the_pedestal_paradox"
SLIDES_DIR = CH1_DIR / "slides"
BGM_PATH = ROOT_DIR / "assets" / "bgm" / "dark_contemplation.mp3"
SCRATCH_DIR = ROOT_DIR / "scratch" / "cadence_test"

def make_sample_video(rate_label):
    concat_txt = SCRATCH_DIR / f"video_concat_{rate_label}.txt"
    durations = []
    
    for sid in range(1, 7):
        audio_file = SCRATCH_DIR / f"shot_{sid:02d}_{rate_label}.mp3"
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_file)]).decode().strip())
        img_name = f"slide_{sid:02d}.jpg"
        durations.append((img_name, dur))
        
    with open(concat_txt, "w") as f:
        for img, dur in durations:
            f.write(f"file '../../projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/slides/{img}'\n")
            f.write(f"duration {dur:.4f}\n")
        f.write(f"file '../../projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_01_the_pedestal_paradox/slides/{durations[-1][0]}'\n")
        
    master_audio = SCRATCH_DIR / f"sample_{rate_label}_master.mp3"
    out_video = SCRATCH_DIR / f"test_preview_shots_1_6_{rate_label}.mp4"
    total_dur = sum(d for _, d in durations)
    
    filter_complex = (
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#FAF9F6,setsar=1,fps=30[v];"
        f"[2:a]volume=0.10,afade=t=in:st=0:d=0.5,afade=t=out:st={total_dur-1.5:.2f}:d=1.5[bgm];"
        f"[1:a]volume=1.0[vo];"
        f"[vo][bgm]amix=inputs=2:duration=first:normalize=0[aout]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-i", str(master_audio),
        "-stream_loop", "-1", "-i", str(BGM_PATH),
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(out_video)
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated sample video: {out_video} ({total_dur:.2f}s)")

make_sample_video("12pct")
make_sample_video("15pct")
