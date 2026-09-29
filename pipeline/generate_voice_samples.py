import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import asyncio
import subprocess
from pathlib import Path
import edge_tts

SAMPLE_TEXT = (
    "In every college lecture hall, there is one boy in the last row who never raises his hand. "
    "He doesn't fight for attention. He doesn't laugh at bad jokes. "
    "He shuts his laptop, leans back, and simply observes."
)

VOICE_CONFIGS = [
    {
        "id": "1_christopher",
        "name": "Christopher (Current Baseline)",
        "voice": "en-US-ChristopherNeural",
        "pitch": "-2Hz",
        "rate": "+2%",
        "style_desc": "Deep, authoritative, calm psychological explainer (American)"
    },
    {
        "id": "2_guy",
        "name": "Guy (Punchy & Energetic)",
        "voice": "en-US-GuyNeural",
        "pitch": "+0Hz",
        "rate": "+4%",
        "style_desc": "Youthful, engaging, high-retention YouTube storytelling tone (American)"
    },
    {
        "id": "3_andrew",
        "name": "Andrew (Smooth & Conversational)",
        "voice": "en-US-AndrewMultilingualNeural",
        "pitch": "-1Hz",
        "rate": "+2%",
        "style_desc": "Smooth, modern video essay / podcast narrator (American)"
    },
    {
        "id": "4_eric",
        "name": "Eric (Grounded & Cinematic)",
        "voice": "en-US-EricNeural",
        "pitch": "-2Hz",
        "rate": "+1%",
        "style_desc": "Reflective, warm, understated cinematic presence (American)"
    },
    {
        "id": "5_ryan_british",
        "name": "Ryan (British Documentary)",
        "voice": "en-GB-RyanNeural",
        "pitch": "+0Hz",
        "rate": "+2%",
        "style_desc": "Articulate, sophisticated British documentary narrator"
    }
]

async def generate_voice(cfg, out_dir, bgm_path):
    raw_path = out_dir / f"{cfg['id']}_dry.mp3"
    with_bgm_path = out_dir / f"{cfg['id']}_with_bgm.mp3"
    
    print(f"Generating [{cfg['name']}]...")
    comm = edge_tts.Communicate(SAMPLE_TEXT, cfg['voice'], pitch=cfg['pitch'], rate=cfg['rate'])
    await comm.save(str(raw_path))
    
    # Probe duration
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(raw_path)]
    dur_res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    duration = float(dur_res.stdout.strip())
    
    # Mix with BGM ducked
    fade_start = max(0.0, duration - 0.4)
    audio_filter = (
        f"[0:a]afade=t=out:st={fade_start:.2f}:d=0.4[vo];"
        f"[vo]asplit=2[vo_main][vo_trigger];"
        f"[1:a]atrim=0:{duration:.2f},volume=0.20,afade=t=out:st={fade_start:.2f}:d=0.4[bgm];"
        f"[bgm][vo_trigger]sidechaincompress=threshold=0.08:ratio=4:attack=50:release=400[ducked_bgm];"
        f"[vo_main][ducked_bgm]amix=inputs=2:duration=first:normalize=0[mixed];"
        f"[mixed]loudnorm=I=-14:LRA=7:tp=-1[a_out]"
    )
    
    mix_cmd = [
        'ffmpeg', '-y',
        '-i', str(raw_path),
        '-stream_loop', '-1', '-i', str(bgm_path),
        '-filter_complex', audio_filter,
        '-map', '[a_out]',
        '-c:a', 'libmp3lame', '-b:a', '192k',
        str(with_bgm_path)
    ]
    subprocess.run(mix_cmd, capture_output=True, check=True)
    print(f"  ✓ Finished {cfg['name']} ({duration:.2f}s)")
    return {
        "cfg": cfg,
        "duration": duration,
        "raw_path": raw_path,
        "with_bgm_path": with_bgm_path
    }

async def main():
    root_dir = Path(".").resolve()
    project_dir = root_dir / "projects" / "ep04_why_girls_like_silent_boy"
    samples_dir = project_dir / "voice_samples"
    samples_dir.mkdir(parents=True, exist_ok=True)
    bgm_path = root_dir / "assets" / "bgm" / "dark_contemplation.mp3"
    
    results = []
    for cfg in VOICE_CONFIGS:
        res = await generate_voice(cfg, samples_dir, bgm_path)
        results.append(res)
        
    print("\n--- ALL SAMPLES READY ---")
    for r in results:
        print(f"{r['cfg']['name']} ({r['duration']:.1f}s)")
        print(f"  Dry:      {r['raw_path']}")
        print(f"  With BGM: {r['with_bgm_path']}")

if __name__ == "__main__":
    asyncio.run(main())
