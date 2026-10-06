import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import asyncio
import subprocess
from pathlib import Path
import edge_tts

HINDI_SCRIPT_CONVERSATIONAL = (
    "हर कॉलेज के लेक्चर हॉल में, लास्ट बेंच पर एक ऐसा लड़का ज़रूर होता है जो कभी हाथ नहीं उठाता। "
    "वो अटेंशन पाने के लिए कभी नहीं लड़ता, और न ही बेकार के जोक्स पर हंसता है। "
    "वो बस अपना लैपटॉप बंद करता है, और शांति से सबको देखता है।"
)

HINDI_SCRIPT_DEEP = (
    "हर कॉलेज के लेक्चर हॉल में, आखिरी बेंच पर एक लड़का ऐसा होता है जो कभी हाथ नहीं उठाता। "
    "वो ध्यान खींचने की कोई कोशिश नहीं करता, न ही बेकार के चुटकुलों पर हंसता है। "
    "वो बस शांत रहता है, और सब कुछ चुपचाप देखता है।"
)

HINDI_VOICE_CONFIGS = [
    {
        "id": "hi_1_madhur_deep",
        "name": "Madhur - Deep Stoic Hindi",
        "voice": "hi-IN-MadhurNeural",
        "pitch": "-2Hz",
        "rate": "+2%",
        "text": HINDI_SCRIPT_DEEP,
        "style_desc": "Grounded, deep stoic psychological tone (Hindi Male)"
    },
    {
        "id": "hi_2_madhur_dynamic",
        "name": "Madhur - Dynamic YouTube Hindi",
        "voice": "hi-IN-MadhurNeural",
        "pitch": "+0Hz",
        "rate": "+5%",
        "text": HINDI_SCRIPT_CONVERSATIONAL,
        "style_desc": "Natural, energetic Indian YouTube storytelling pace (Hindi Male)"
    },
    {
        "id": "hi_3_madhur_college",
        "name": "Madhur - Modern College Hinglish",
        "voice": "hi-IN-MadhurNeural",
        "pitch": "-1Hz",
        "rate": "+3%",
        "text": HINDI_SCRIPT_CONVERSATIONAL,
        "style_desc": "Modern relatable Indian college campus cadence (Hindi Male)"
    },
    {
        "id": "hi_4_swara_clean",
        "name": "Swara - Crisp Hindi Female",
        "voice": "hi-IN-SwaraNeural",
        "pitch": "+0Hz",
        "rate": "+3%",
        "text": HINDI_SCRIPT_CONVERSATIONAL,
        "style_desc": "Clear, articulate Indian female explainer narration"
    }
]

async def generate_hindi_samples():
    root_dir = Path(".").resolve()
    project_dir = root_dir / "projects" / "ep04_why_girls_like_silent_boy"
    out_dir = project_dir / "voice_samples" / "hindi"
    out_dir.mkdir(parents=True, exist_ok=True)
    bgm_path = root_dir / "assets" / "bgm" / "dark_contemplation.mp3"
    
    results = []
    for cfg in HINDI_VOICE_CONFIGS:
        raw_path = out_dir / f"{cfg['id']}_dry.mp3"
        with_bgm_path = out_dir / f"{cfg['id']}_with_bgm.mp3"
        
        print(f"Generating [{cfg['name']}]...")
        comm = edge_tts.Communicate(cfg['text'], cfg['voice'], pitch=cfg['pitch'], rate=cfg['rate'])
        await comm.save(str(raw_path))
        
        # probe duration
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
        results.append({
            "cfg": cfg,
            "duration": duration,
            "raw_path": raw_path,
            "with_bgm_path": with_bgm_path
        })
        
    print("\n--- ALL HINDI SAMPLES READY ---")
    for r in results:
        print(f"{r['cfg']['name']} ({r['duration']:.1f}s)")
        print(f"  Dry:      {r['raw_path']}")
        print(f"  With BGM: {r['with_bgm_path']}")

if __name__ == "__main__":
    asyncio.run(generate_hindi_samples())
