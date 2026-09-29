import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import asyncio
import json
import math
import subprocess
import shutil
from pathlib import Path
import edge_tts

HINDI_CUTS = [
    {"cut_id": 1, "text": "हर कॉलेज के लेक्चर हॉल में,"},
    {"cut_id": 2, "text": "लास्ट रो में एक ऐसा लड़का होता है"},
    {"cut_id": 3, "text": "जो कभी हाथ नहीं उठाता।"},
    {"cut_id": 4, "text": "वो कभी नहीं लड़ता"},
    {"cut_id": 5, "text": "अटेंशन पाने के लिए।"},
    {"cut_id": 6, "text": "वो कभी नहीं हंसता"},
    {"cut_id": 7, "text": "खराब चुटकुलों पर।"},
    {"cut_id": 8, "text": "वो अपना लैपटॉप बंद करता है,"},
    {"cut_id": 9, "text": "पीछे आराम से बैठता है,"},
    {"cut_id": 10, "text": "और बस सबको देखता है।"},
    {"cut_id": 11, "text": "फिर भी, मिडल रो की लड़कियां"},
    {"cut_id": 12, "text": "बार-बार पीछे मुड़कर देखती हैं,"},
    {"cut_id": 13, "text": "कि वो आखिर क्या सोच रहा है।"},
    {"cut_id": 14, "text": "आखिर क्यों?"},
    {"cut_id": 15, "text": "क्योंकि इंसान का दिमाग"},
    {"cut_id": 16, "text": "भीख में मांगी गई अटेंशन को इग्नोर करता है।"},
    {"cut_id": 17, "text": "उतावला फ्रंटबेंचर"},
    {"cut_id": 18, "text": "वैलिडेशन टैक्स के जाल में फंसा होता है।"},
    {"cut_id": 19, "text": "वो ज़ोर-ज़ोर से बोलता है,"},
    {"cut_id": 20, "text": "हर बात पर हां में हां मिलाता है,"},
    {"cut_id": 21, "text": "और तालियों के लिए नाटक करता है।"},
    {"cut_id": 22, "text": "दिमाग के लिए,"},
    {"cut_id": 23, "text": "ज़्यादा मेहनत लो-स्टेटस का संकेत है।"},
    {"cut_id": 24, "text": "ये शांत लड़का"},
    {"cut_id": 25, "text": "इसके बिल्कुल उलट नियम पर चलता है।"},
    {"cut_id": 26, "text": "वो लोगों से दूर नहीं भागता"},
    {"cut_id": 27, "text": "किसी डर की वजह से।"},
    {"cut_id": 28, "text": "वो बस पूरी तरह बेअसर है"},
    {"cut_id": 29, "text": "दूसरों की मंज़ूरी से।"},
    {"cut_id": 30, "text": "जब प्रोफेसर उसका नाम पुकारते हैं,"},
    {"cut_id": 31, "text": "तो वो घबराता नहीं।"},
    {"cut_id": 32, "text": "वो शांत नज़रों से ऊपर देखता है,"},
    {"cut_id": 33, "text": "साफ़ तीन शब्दों में जवाब देता है,"},
    {"cut_id": 34, "text": "और वापस अपनी ख़ामोशी में लौट जाता है।"},
    {"cut_id": 35, "text": "न कोई नर्वस हंसी।"},
    {"cut_id": 36, "text": "न कोई घबराहट।"},
    {"cut_id": 37, "text": "न कोई ज़रूरत"},
    {"cut_id": 38, "text": "खुद को साबित करने की।"},
    {"cut_id": 39, "text": "सोशल साइकोलॉजी में,"},
    {"cut_id": 40, "text": "मिस्ट्री छुपने से नहीं बनती।"},
    {"cut_id": 41, "text": "ये बनती है खुद में पूरी तरह सहज रहने से,"},
    {"cut_id": 42, "text": "जब आपको किसी को कुछ साबित नहीं करना होता।"}
]

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - math.floor(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def escape_ffmpeg_path(path):
    p_str = str(Path(path).resolve()).replace('\\', '/')
    return p_str.replace(':', r'\:')

async def main():
    root_dir = Path(".").resolve()
    project_dir = root_dir / "projects" / "ep04_why_girls_like_silent_boy"
    hi_dir = project_dir / "audio_hindi"
    hi_dir.mkdir(parents=True, exist_ok=True)
    slides_dir = project_dir / "slides"
    renders_dir = root_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)
    bgm_path = root_dir / "assets" / "bgm" / "dark_contemplation.mp3"

    print("=======================================================")
    print("  BUILDING HINDI FINAL: Ep04 Why Girls Like Silent Boy")
    print("  Voice: Madhur (-2Hz, +2%) | Mastered -14 LUFS")
    print("=======================================================\n")

    # Generate full Hindi text
    full_text = " ".join(c["text"] for c in HINDI_CUTS)
    vo_hindi_path = hi_dir / "voiceover_hindi.mp3"
    words_hindi_path = hi_dir / "word_timestamps_hindi.json"

    print("[1/4] Generating Madhur Neural Speech & Word Boundaries...")
    comm = edge_tts.Communicate(
        full_text,
        voice="hi-IN-MadhurNeural",
        pitch="-2Hz",
        rate="+2%",
        boundary="WordBoundary"
    )

    words = []
    with open(vo_hindi_path, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                start_sec = (chunk["offset"] / 10000) / 1000.0
                end_sec = ((chunk["offset"] + chunk["duration"]) / 10000) / 1000.0
                words.append({
                    "word": chunk["text"],
                    "start_sec": round(start_sec, 3),
                    "end_sec": round(end_sec, 3),
                    "duration_sec": round(end_sec - start_sec, 3)
                })

    with open(words_hindi_path, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2, ensure_ascii=False)
    print(f"✓ Hindi voiceover generated: {len(words)} words ({words[-1]['end_sec']:.2f}s)")

    # Map each cut to first word of cut
    print("[2/4] Mapping Hindi cut boundaries to visual slides...")
    w_idx = 0
    cut_starts = []
    for cut in HINDI_CUTS:
        cut_words = cut["text"].replace(",", "").replace("।", "").replace("?", "").strip().split()
        first_w = cut_words[0] if cut_words else ""
        matched_time = None
        for j in range(w_idx, len(words)):
            clean_text_w = cut_words[0].strip()
            clean_audio_w = words[j]["word"].strip()
            if clean_text_w == clean_audio_w or clean_text_w in clean_audio_w:
                matched_time = words[j]["start_sec"]
                w_idx = j + len(cut_words)
                break
        cut_starts.append((cut["cut_id"], matched_time, cut["text"]))

    total_hi_dur = words[-1]["end_sec"] + 0.65
    exact_hi_clips = []
    for i in range(len(cut_starts)):
        cid, start_t, text = cut_starts[i]
        actual_start = 0.0 if i == 0 else (start_t if start_t is not None else exact_hi_clips[-1]["end"])
        if i < len(cut_starts) - 1:
            next_t = cut_starts[i+1][1] if cut_starts[i+1][1] is not None else actual_start + 1.5
        else:
            next_t = total_hi_dur
        dur = max(0.5, round(next_t - actual_start, 3))
        exact_hi_clips.append({
            "cut_id": cid,
            "start": actual_start,
            "end": next_t,
            "duration": dur,
            "text": text,
            "slide_file": slides_dir / f"slide_{cid:02d}.jpg"
        })

    print(f"✓ Total Hindi Duration: {total_hi_dur:.2f}s across 42 slides")

    # Build concat file for Hindi
    concat_hi_txt = project_dir / "concat_hi_42.txt"
    with open(concat_hi_txt, "w", encoding="utf-8") as f:
        for c in exact_hi_clips:
            resolved_p = str(c["slide_file"].resolve()).replace("\\", "/")
            f.write(f"file '{resolved_p}'\n")
            f.write(f"duration {c['duration']:.3f}\n")
        last_p = str(exact_hi_clips[-1]["slide_file"].resolve()).replace("\\", "/")
        f.write(f"file '{last_p}'\n")

    # Build Hindi ASS Subtitles
    print("[3/4] Generating Hindi Kinetic Subtitles (.ass)...")
    sub_events = []
    chunk_size = 3
    for i in range(0, len(words), chunk_size):
        chunk = words[i:i + chunk_size]
        chunk_start = chunk[0]["start_sec"]
        chunk_end = chunk[-1]["end_sec"]
        if i + chunk_size < len(words):
            chunk_end = min(chunk_end, words[i + chunk_size]["start_sec"])
            
        for active_idx, target_word in enumerate(chunk):
            w_start = target_word["start_sec"]
            w_end = chunk[active_idx + 1]["start_sec"] if active_idx < len(chunk) - 1 else chunk_end
            w_end = min(w_end, chunk_end)
            if w_end <= w_start:
                w_end = w_start + 0.10
                
            start_str = format_ass_time(w_start)
            end_str = format_ass_time(w_end)
            
            parts = []
            for idx, w in enumerate(chunk):
                raw_word = w["word"]
                if idx == active_idx:
                    parts.append(f"{{\\c&H0000D7FF&\\3c&H000A0D14&\\t(0,70,\\fscx108\\fscy108)\\t(70,140,\\fscx100\\fscy100)}}{raw_word}{{\\c&H00FFFFFF&\\3c&H000A0D14&}}")
                else:
                    parts.append(raw_word)
            line_text = " ".join(parts)
            sub_events.append(f"Dialogue: 0,{start_str},{end_str},ExplainerWordSub,,0,0,0,,{line_text}")

    ass_header = f"""[Script Info]
Title: Hindi Kinetic Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ExplainerWordSub,Nirmala UI,56,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.0,2.0,2,60,60,350,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ass_hindi_path = project_dir / "subtitles_hindi.ass"
    with open(ass_hindi_path, "w", encoding="utf-8") as f:
        f.write(ass_header)
        for ev in sub_events:
            f.write(f"{ev}\n")
    print(f"✓ Hindi subtitles written: {ass_hindi_path.name} ({len(sub_events)} events)")

    # Build Video
    print("[4/4] Rendering Hindi Final Video...")
    out_project_file = project_dir / "ep04_why_girls_like_silent_boy_final_hi.mp4"
    out_render_file = renders_dir / "ep04_why_girls_like_silent_boy_final_hi.mp4"
    escaped_sub = escape_ffmpeg_path(ass_hindi_path)
    fade_start = total_hi_dur - 0.40

    video_filter = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,ass='{escaped_sub}'[v_out]"
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
        "-f", "concat", "-safe", "0", "-i", str(concat_hi_txt),
        "-i", str(vo_hindi_path),
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
        raise RuntimeError("Hindi build failed")

    shutil.copy2(out_project_file, out_render_file)
    print(f"✓ Hindi Final Video Built: {out_render_file}")
    return out_render_file

if __name__ == "__main__":
    asyncio.run(main())
