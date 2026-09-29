import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import asyncio
import json
import subprocess
import shutil
from pathlib import Path
import edge_tts

# Natural conversational Hindi (No textbook Hindi, pure creator storytelling flow)
HINDI_CUTS_NATURAL = [
    {"cut_id": 1, "text": "कॉलेज के हर क्लासरूम में,"},
    {"cut_id": 2, "text": "लास्ट बेंच पर एक ऐसा लड़का ज़रूर होता है,"},
    {"cut_id": 3, "text": "जो कभी हाथ नहीं उठाता।"},
    {"cut_id": 4, "text": "उसे किसी की अटेंशन की"},
    {"cut_id": 5, "text": "भूख नहीं होती।"},
    {"cut_id": 6, "text": "न वो प्रोफेसर के"},
    {"cut_id": 7, "text": "फालतू जोक्स पर हंसता है।"},
    {"cut_id": 8, "text": "वो बस लैपटॉप बंद करता है,"},
    {"cut_id": 9, "text": "आराम से पीछे टिकता है,"},
    {"cut_id": 10, "text": "और चुपचाप सबको नोटिस करता है।"},
    {"cut_id": 11, "text": "फिर भी, आगे बैठी लड़कियां"},
    {"cut_id": 12, "text": "बार-बार मुड़कर देखती हैं,"},
    {"cut_id": 13, "text": "कि वो सोच क्या रहा है।"},
    {"cut_id": 14, "text": "जानते हो क्यों?"},
    {"cut_id": 15, "text": "क्योंकि इंसान का दिमाग"},
    {"cut_id": 16, "text": "अटेंशन के लिए मरे जा रहे लोगों को इग्नोर करता है।"},
    {"cut_id": 17, "text": "आगे बैठने वाला लड़का"},
    {"cut_id": 18, "text": "हमेशा वैलिडेशन के जाल में फंसा रहता है।"},
    {"cut_id": 19, "text": "वो लाउड बोलता है,"},
    {"cut_id": 20, "text": "हर बात में हां मिलाता है,"},
    {"cut_id": 21, "text": "और सिर्फ तालियों के लिए नाटक करता है।"},
    {"cut_id": 22, "text": "दिमाग की नज़र में,"},
    {"cut_id": 23, "text": "ज़रूरत से ज़्यादा कोशिश कमजोरी की निशानी है।"},
    {"cut_id": 24, "text": "लेकिन ये शांत लड़का,"},
    {"cut_id": 25, "text": "बिल्कुल अलग उसूलों पर चलता है।"},
    {"cut_id": 26, "text": "वो किसी डर से"},
    {"cut_id": 27, "text": "लोगों से नहीं बचता।"},
    {"cut_id": 28, "text": "उसे बस दूसरों के"},
    {"cut_id": 29, "text": "अप्रूवल की कोई परवाह नहीं है।"},
    {"cut_id": 30, "text": "जब प्रोफेसर अचानक उसका नाम लेते हैं,"},
    {"cut_id": 31, "text": "वो पैनिक नहीं करता।"},
    {"cut_id": 32, "text": "वो शांत नज़रों से देखता है,"},
    {"cut_id": 33, "text": "तीन नपे-तुले शब्दों में जवाब देता है,"},
    {"cut_id": 34, "text": "और वापस अपनी ख़ामोशी में लौट जाता है।"},
    {"cut_id": 35, "text": "न कोई नर्वस हंसी।"},
    {"cut_id": 36, "text": "न कोई बेचैनी।"},
    {"cut_id": 37, "text": "न खुद को"},
    {"cut_id": 38, "text": "सही साबित करने की कोई जल्दी।"},
    {"cut_id": 39, "text": "साइकोलॉजी कहती है,"},
    {"cut_id": 40, "text": "मिस्ट्री छुपने से नहीं बनती।"},
    {"cut_id": 41, "text": "ये बनती है खुद में इतना कम्फर्टेबल रहने से,"},
    {"cut_id": 42, "text": "कि आपको किसी को कुछ भी साबित न करना पड़े।"}
]

async def build_natural_hindi():
    root_dir = Path(".").resolve()
    project_dir = root_dir / "projects" / "ep04_why_girls_like_silent_boy"
    hi_dir = project_dir / "audio_hindi"
    hi_dir.mkdir(parents=True, exist_ok=True)
    slides_dir = project_dir / "slides"
    renders_dir = root_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)
    bgm_path = root_dir / "assets" / "bgm" / "dark_contemplation.mp3"

    print("=======================================================")
    print("  BUILDING NATURAL HINDI FINAL (NO CAPTIONS / NO SUBS)")
    print("  Voice: Madhur (+12% rate, natural conversational flow)")
    print("=======================================================\n")

    full_text = " ".join(c["text"] for c in HINDI_CUTS_NATURAL)
    vo_path = hi_dir / "voiceover_natural_hindi.mp3"
    words_path = hi_dir / "words_natural_hindi.json"

    print("[1/3] Generating Natural Conversational Hindi Voiceover (Faster Pacing +20%)...")
    comm = edge_tts.Communicate(
        full_text,
        voice="hi-IN-MadhurNeural",
        pitch="+0Hz",
        rate="+20%",
        boundary="WordBoundary"
    )

    words = []
    with open(vo_path, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = (chunk["offset"] / 10000) / 1000.0
                end_sec = ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                words.append({
                    "word": chunk["text"],
                    "start_sec": round(start_sec, 3),
                    "end_sec": round(end_sec, 3)
                })

    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2, ensure_ascii=False)

    print(f"✓ Natural speech generated: {len(words)} words ({words[-1]['end_sec']:.2f}s)")

    # Map each cut to first word of cut
    print("[2/3] Mapping cuts to exact Hindi word boundaries...")
    w_idx = 0
    cut_starts = []
    for cut in HINDI_CUTS_NATURAL:
        clean_c_words = cut["text"].replace(",", "").replace("।", "").replace("?", "").strip().split()
        matched_time = None
        for j in range(w_idx, len(words)):
            clean_text_w = clean_c_words[0].strip()
            clean_audio_w = words[j]["word"].strip()
            if clean_text_w == clean_audio_w or clean_text_w in clean_audio_w:
                matched_time = words[j]["start_sec"]
                w_idx = j + len(clean_c_words)
                break
        cut_starts.append((cut["cut_id"], matched_time, cut["text"]))

    total_hi_dur = words[-1]["end_sec"] + 0.60
    exact_clips = []
    for i in range(len(cut_starts)):
        cid, start_t, text = cut_starts[i]
        actual_start = 0.0 if i == 0 else (start_t if start_t is not None else exact_clips[-1]["end"])
        if i < len(cut_starts) - 1:
            next_t = cut_starts[i+1][1] if cut_starts[i+1][1] is not None else actual_start + 1.5
        else:
            next_t = total_hi_dur
        dur = max(0.4, round(next_t - actual_start, 3))
        exact_clips.append({
            "cut_id": cid,
            "start": actual_start,
            "end": next_t,
            "duration": dur,
            "text": text,
            "slide_file": slides_dir / f"slide_{cid:02d}.jpg"
        })

    print(f"✓ Total Natural Hindi Duration: {total_hi_dur:.2f}s across 42 slides")

    # Build concat file
    concat_txt_path = project_dir / "concat_hi_natural_42.txt"
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for c in exact_clips:
            resolved_p = str(c["slide_file"].resolve()).replace("\\", "/")
            f.write(f"file '{resolved_p}'\n")
            f.write(f"duration {c['duration']:.3f}\n")
        last_p = str(exact_clips[-1]["slide_file"].resolve()).replace("\\", "/")
        f.write(f"file '{last_p}'\n")

    # Render video with ZERO CAPTIONS (pure visuals)
    print("[3/3] Rendering Hindi Video with ZERO CAPTIONS and ducked BGM...")
    out_project_file = project_dir / "ep04_why_girls_like_silent_boy_final_hi.mp4"
    out_render_file = renders_dir / "ep04_why_girls_like_silent_boy_final_hi.mp4"

    fade_start = total_hi_dur - 0.40
    # Notice: NO ass filter! Pure scaling, cropping, 30fps
    video_filter = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v_out]"
    
    audio_filter = (
        f"[1:a]atrim=0:{total_hi_dur},afade=t=out:st={fade_start:.2f}:d=0.40[vo];"
        f"[vo]asplit=2[vo_main][vo_trigger];"
        f"[2:a]atrim=0:{total_hi_dur},volume=0.20,afade=t=out:st={fade_start:.2f}:d=0.40[bgm];"
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
        "-t", f"{total_hi_dur:.2f}",
        str(out_project_file)
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[FFmpeg Error]:\n{res.stderr}")
        raise RuntimeError("Hindi rendering failed")

    shutil.copy2(out_project_file, out_render_file)
    print(f"\n=======================================================")
    print(f"🎉 NATURAL HINDI FINAL VIDEO BUILT SUCCESSFULLY!")
    print(f"   Project File: {out_project_file}")
    print(f"   Render Vault: {out_render_file}")
    print(f"   Duration:     {total_hi_dur:.2f}s")
    print(f"   Captions:     NONE (Clean Full-Bleed 2D Visuals)")
    print(f"   Audio:        Natural Conversational Madhur + Ducked BGM (-14 LUFS)")
    print("=======================================================\n")
    return out_render_file

if __name__ == "__main__":
    asyncio.run(build_natural_hindi())
