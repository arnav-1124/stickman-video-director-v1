import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import math
import wave
import struct
import shutil
import subprocess
from pathlib import Path
import numpy as np

def format_ass(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def extract_pure_pcm(wav_path):
    raw = wav_path.read_bytes()
    idx = raw.find(b'C2PA')
    if idx != -1:
        pcm_bytes = raw[44:idx]
    else:
        pcm_bytes = raw[44:]
    if len(pcm_bytes) % 2 != 0:
        pcm_bytes = pcm_bytes[:-1]
    return np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0

# 31 Shots with verified narration texts and relative speech boundaries in raw acts
RAW_SHOTS_DATA = [
    # Act 1 (13 shots)
    (37, "act1", "slide_37.jpg", "Chapter Two: The Casino Effect. The Dopamine of Uncertainty.", 0.08, 3.89),
    (38, "act1", "slide_38.jpg", "To see this principle in action, we have to look inside a psychology laboratory from the nineteen fifties.", 4.72, 9.55),
    (39, "act1", "slide_39.jpg", "The behavioral scientist B.F. Skinner conducted a famous series of experiments with animals.", 9.87, 14.43),
    (40, "act1", "slide_40.jpg", "In the first setup, a pigeon was placed inside a box with a lever.", 14.94, 18.23),
    (41, "act1", "slide_41.jpg", "Every single time the pigeon pressed the lever, a food pellet dropped into the bowl. Press the lever, get food. Press the lever, get food.", 18.77, 25.09),
    (42, "act1", "slide_42.jpg", "What happened? The pigeon pressed the lever when it was hungry, ate its food, and then completely ignored the lever. The food was completely predictable.", 25.64, 34.20),
    (43, "act1", "slide_43.jpg", "It was reliable, safe, and boring.", 34.73, 36.53),
    (44, "act1", "slide_44.jpg", "Then, Skinner changed the rules. He introduced what psychologists call a variable-ratio schedule of reinforcement.", 36.94, 45.56),
    (45, "act1", "slide_45.jpg", "Now, when the pigeon pressed the lever, food only dropped out sometimes.", 46.07, 51.02),
    (46, "act1", "slide_46.jpg", "Sometimes it took one press. Sometimes it took five presses. Sometimes it took twelve presses with nothing, and then suddenly two pellets dropped at once. The reward was completely unpredictable.", 51.34, 55.43),
    (47, "act1", "slide_47.jpg", "What did the pigeon do? It became completely obsessed.", 55.89, 59.12),
    (48, "act1", "slide_48.jpg", "It stood in front of the lever for hours, pressing it frantically, ignoring its sleep, and ignoring other birds.", 59.54, 64.61),
    (49, "act1", "slide_49.jpg", "The unpredictability hijacked the animal's neurological reward circuitry.", 65.08, 68.83),

    # Act 2 (7 shots)
    (50, "act2", "slide_50.jpg", "Modern neuroscientists now know why this happens.", 0.08, 3.55),
    (51, "act2", "slide_51.jpg", "Dopamine is not the chemical of pleasure.", 3.55, 6.09),
    (52, "act2", "slide_52.jpg", "Dopamine is the chemical of anticipation.", 6.59, 9.02),
    (53, "act2", "slide_53.jpg", "Your brain does not release its biggest spike of dopamine when you receive a prize. It releases its biggest spike of dopamine when it does not know whether a prize is coming or not.", 9.91, 19.39),
    (54, "act2", "slide_54.jpg", "This is the exact psychological mechanism behind slot machines, lottery tickets, and social media notifications.", 20.25, 26.59),
    (55, "act2", "slide_55.jpg", "When you pull the lever on a slot machine, the thrilling tension is in the spinning reels. Will three cherries align, or will you lose everything?", 27.27, 35.02),
    (56, "act2", "slide_56.jpg", "That unresolved gap between hope and fear floods your brain with dopamine.", 35.53, 39.40),

    # Act 3 (10 shots)
    (57, "act3", "slide_57.jpg", "Now, bring this back to human interaction. The person who is always available operates like the first lever.", 0.00, 5.68),
    (58, "act3", "slide_58.jpg", "Text them, and they reply within thirty seconds. Compliment them, and they shower you with praise. Ask them to meet, and they immediately say yes.", 6.18, 13.56),
    (59, "act3", "slide_59.jpg", "Their behavior is a hundred percent predictable. There is no mystery. There is no tension.", 14.17, 18.64),
    (60, "act3", "slide_60.jpg", "And because there is no anticipation, there is no dopamine.", 19.04, 22.08),
    (61, "act3", "slide_61.jpg", "Their attention is comfortable, but it creates zero gravitational pull.", 22.75, 26.85),
    (62, "act3", "slide_62.jpg", "The person who is slightly aloof, however, operates like the slot machine.", 27.70, 35.34),
    (63, "act3", "slide_63.jpg", "When they look at you, it feels meaningful because they rarely look around.", 36.12, 42.47),
    (64, "act3", "slide_64.jpg", "When they pay you a compliment, it sticks in your memory for three weeks because compliments from them are virtually impossible to get.", 43.08, 51.34),
    (65, "act3", "slide_65.jpg", "When they text you back, your phone lights up and your heart skips a beat—not because the text is poetic, but because you genuinely didn't know if they would reply at all.", 51.81, 54.46),
    (66, "act3", "slide_66.jpg", "You are not necessarily falling in love with the person. You are falling in love with the chemical cocktail created by their unpredictability.", 54.67, 58.80),

    # Outro (1 shot)
    (67, "outro", "slide_67.jpg", "In Chapter Three, we reveal why the most powerful move in any room is having somewhere else to be: The Economy of Availability. Subscribe to Sticky in Dark.", 0.10, 9.20)
]

def main():
    print("=" * 80)
    print("  🎬 BUILDING CONTINUOUS V2 CALIBRATED CHAPTER 02 (ALL GAPS AT 0.35s)")
    print("=" * 80)

    ch02_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_02_the_casino_effect")
    ch03_dir = Path("projects/long/ep01_why_people_fall_for_who_ignores_them/chapter_03_the_economy_of_availability")
    slides_dir = ch02_dir / "slides"
    tts_dir = ch02_dir / "audio" / "google_tts"
    logo = Path("assets/branding/channel_logo.png")
    bgm = Path("assets/bgm/dark_contemplation.mp3")

    temp_dir = Path("temp/ch02_v2_continuous_build")
    temp_dir.mkdir(parents=True, exist_ok=True)

    master_v2_mp4 = ch02_dir / "renders" / "WHY_UNPREDICTABLE_PEOPLE_ARE_ADDICTIVE_Chapter_02_V2_CALIBRATED.mp4"
    central_v2_mp4 = Path("renders/long/ep01_why_people_fall_for_who_ignores_them/WHY_UNPREDICTABLE_PEOPLE_ARE_ADDICTIVE_Chapter_02_V2_CALIBRATED.mp4")
    master_v2_mp4.parent.mkdir(parents=True, exist_ok=True)
    central_v2_mp4.parent.mkdir(parents=True, exist_ok=True)

    sr = 24000

    # 1. Load pure audio PCM without C2PA watermark metadata
    pcm_a1 = extract_pure_pcm(tts_dir / "act1_ludo.wav")
    pcm_a2 = extract_pure_pcm(tts_dir / "act2_ludo.wav")
    pcm_a3 = extract_pure_pcm(tts_dir / "act3_ludo.wav")
    pcm_outro = extract_pure_pcm(tts_dir / "outro_ludo.wav")

    # Trim leading & trailing silence on each act before joining with exactly 0.35s junction
    # Act 1 ends at 68.85s
    pcm_a1 = pcm_a1[:int(68.85 * sr)]
    # Act 2 ends at 39.45s
    pcm_a2 = pcm_a2[:int(39.45 * sr)]
    # Act 3 ends at 58.85s
    pcm_a3 = pcm_a3[:int(58.85 * sr)]
    # Outro ends at 9.25s
    pcm_outro = pcm_outro[:int(9.25 * sr)]

    # Inter-act breathing silence buffer (0.35s)
    sil_35 = np.zeros(int(0.35 * sr), dtype=np.float32)

    # Offsets in raw stitched audio
    off_a1 = 0.0
    off_a2 = (len(pcm_a1) + len(sil_35)) / sr
    off_a3 = (len(pcm_a1) + len(sil_35) + len(pcm_a2) + len(sil_35)) / sr
    off_outro = (len(pcm_a1) + len(sil_35) + len(pcm_a2) + len(sil_35) + len(pcm_a3) + len(sil_35)) / sr

    # Combine into single continuous audio track
    raw_continuous = np.concatenate([
        pcm_a1, sil_35,
        pcm_a2, sil_35,
        pcm_a3, sil_35,
        pcm_outro
    ])
    print(f"Stitched Pure Continuous Audio: {len(raw_continuous)/sr:.3f}s (Zero C2PA screech artifacts)")

    # 2. Calibrate All Gaps >= 0.38s down to 0.35s across the whole continuous track
    win_len = int(0.02 * sr)
    hop = int(0.005 * sr)
    rms = np.array([np.sqrt(np.mean(raw_continuous[i:i+win_len]**2)) for i in range(0, len(raw_continuous) - win_len, hop)])
    times = np.array([i / sr for i in range(0, len(raw_continuous) - win_len, hop)])

    thresh = 0.012
    is_silent = rms < thresh

    silence_blocks = []
    in_sil = False
    s_start = 0
    for t, sil in zip(times, is_silent):
        if sil and not in_sil:
            in_sil = True
            s_start = t
        elif not sil and in_sil:
            in_sil = False
            dur = t - s_start
            if dur > 0.38:
                silence_blocks.append((s_start, t, dur))
    if in_sil:
        dur = times[-1] - s_start
        if dur > 0.38:
            silence_blocks.append((s_start, times[-1], dur))

    print(f"Detected {len(silence_blocks)} pauses to calibrate to 0.35s across episode.")

    calibrated_chunks = []
    curr_samp = 0
    target_sil = 0.35
    time_pairs = [] # (orig_continuous_time, calibrated_time)
    curr_cal_time = 0.0

    for s_start, s_end, dur in silence_blocks:
        st_samp = int(s_start * sr)
        en_samp = int(s_end * sr)

        pre = raw_continuous[curr_samp:st_samp]
        calibrated_chunks.append(pre)
        time_pairs.append((curr_samp / sr, curr_cal_time))
        curr_cal_time += len(pre) / sr
        time_pairs.append((s_start, curr_cal_time))

        keep_samp = int(target_sil * sr)
        h_keep = keep_samp // 2
        head = raw_continuous[st_samp : st_samp + h_keep]
        tail = raw_continuous[en_samp - h_keep : en_samp]

        xf_len = int(0.015 * sr)
        xf_in = np.linspace(0, 1, xf_len)
        xf_out = np.linspace(1, 0, xf_len)

        sil_c = np.concatenate([head[:-xf_len], head[-xf_len:]*xf_out + tail[:xf_len]*xf_in, tail[xf_len:]])
        calibrated_chunks.append(sil_c)
        curr_cal_time += len(sil_c) / sr
        time_pairs.append((s_end, curr_cal_time))

        curr_samp = en_samp

    rem = raw_continuous[curr_samp:]
    calibrated_chunks.append(rem)
    time_pairs.append((len(raw_continuous)/sr, curr_cal_time + len(rem)/sr))

    final_calibrated_audio = np.concatenate(calibrated_chunks)
    cal_dur = len(final_calibrated_audio) / sr
    print(f"Calibrated Full Audio Duration: {cal_dur:.3f}s (Saved {len(raw_continuous)/sr - cal_dur:.2f}s of dead silence)")

    def map_to_calibrated(act_name, rel_time):
        if act_name == "act1":
            t_orig = off_a1 + rel_time
        elif act_name == "act2":
            t_orig = off_a2 + rel_time
        elif act_name == "act3":
            t_orig = off_a3 + rel_time
        else:
            t_orig = off_outro + rel_time
        return float(np.interp(t_orig, [p[0] for p in time_pairs], [p[1] for p in time_pairs]))

    # Save calibrated clean PCM audio
    raw_calibrated_wav = temp_dir / "ch02_v2_voice_calibrated_raw.wav"
    final_int16 = (np.clip(final_calibrated_audio, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(str(raw_calibrated_wav), "wb") as ow:
        ow.setnchannels(1)
        ow.setsampwidth(2)
        ow.setframerate(sr)
        ow.writeframes(final_int16.tobytes())

    # 3. Master through Studio DSP Chain (-11.9 LUFS)
    mastered_voice_wav = temp_dir / "ch02_v2_voice_mastered.wav"
    dsp_filter = (
        "highpass=f=80,"
        "equalizer=f=115:t=q:w=1.2:g=4.2,"
        "equalizer=f=250:t=q:w=1.5:g=2.0,"
        "equalizer=f=3500:t=q:w=1.0:g=2.5,"
        "acompressor=threshold=-18dB:ratio=2.5:attack=15:release=120,"
        "loudnorm=I=-11.9:TP=-1.5:LRA=7.0"
    )
    subprocess.run([
        "ffmpeg", "-y", "-i", str(raw_calibrated_wav),
        "-af", dsp_filter,
        "-ar", "48000", str(mastered_voice_wav)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Mastered voice track with Deep Masculine Broadcast DSP (-11.9 LUFS)")

    # 4. Build Verified Shot Timeline for All 31 Shots
    timeline = []
    for sid, act_name, slide, text, s_rel, e_rel in RAW_SHOTS_DATA:
        cal_s = map_to_calibrated(act_name, s_rel)
        cal_e = map_to_calibrated(act_name, e_rel)
        slide_file = (ch03_dir / "slides" / slide) if sid == 67 else (slides_dir / slide)
        timeline.append({
            "shot_id": sid,
            "slide_path": slide_file,
            "text": text,
            "speech_start": cal_s,
            "speech_end": cal_e
        })

    # Cut boundaries exactly halfway between sentences for seamless continuous flow
    for i in range(len(timeline)):
        if i == 0:
            c_start = 0.0
        else:
            prev_end = timeline[i-1]["speech_end"]
            curr_start = timeline[i]["speech_start"]
            c_start = (prev_end + curr_start) / 2.0

        if i == len(timeline) - 1:
            c_end = timeline[i]["speech_end"] + 1.50 # 1.5s visual hold at end
        else:
            curr_end = timeline[i]["speech_end"]
            next_start = timeline[i+1]["speech_start"]
            c_end = (curr_end + next_start) / 2.0

        timeline[i]["cut_start"] = c_start
        timeline[i]["cut_end"] = c_end
        timeline[i]["cut_dur"] = c_end - c_start

    total_video_dur = timeline[-1]["cut_end"]
    print(f"Continuous Timeline Assembled: 31 shots across {total_video_dur:.3f}s ({int(total_video_dur//60):02d}:{total_video_dur%60:05.2f})")

    # 5. Build Concat Script for Video Slides
    video_concat_txt = temp_dir / "video_concat_ch02_v2.txt"
    with open(video_concat_txt, "w", encoding="utf-8") as f:
        for t in timeline:
            sp = t["slide_path"].resolve().as_posix()
            f.write(f"file '{sp}'\n")
            f.write(f"duration {t['cut_dur']:.3f}\n")
        # Final repeat for concat demuxer boundary
        f.write(f"file '{timeline[-1]['slide_path'].resolve().as_posix()}'\n")

    # 6. Generate Kinetic Highlighted ASS Subtitles
    sub_file = ch02_dir / "subtitles_ch02_v2_calibrated.ass"
    header = """[Script Info]
Title: Sticky in Dark 16:9 Kinetic Subtitles - Chapter 02 (V2 Calibrated)
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ExplainerWordSub,Arial Black,50,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.0,2.0,2,80,80,110,1
Style: OutroWordSub,Arial Black,46,&H00FFFFFF&,&H0000D7FF&,&H000A0D14&,&HA0000000&,-1,0,0,0,100,100,1.2,0,1,5.0,2.0,2,80,80,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    chunk_size = 4
    for t in timeline:
        sp_start = t["speech_start"]
        sp_end = t["speech_end"]
        sp_dur = sp_end - sp_start
        words = t["text"].split()
        if not words: continue

        sub_style = "OutroWordSub" if t["shot_id"] == 67 else "ExplainerWordSub"
        w_dur = sp_dur / len(words)

        for i in range(0, len(words), chunk_size):
            chunk = words[i:i+chunk_size]
            c_start = sp_start + (i * w_dur)
            c_end = min(sp_end, sp_start + ((i + len(chunk)) * w_dur))
            for j in range(len(chunk)):
                w_start = c_start + (j * w_dur)
                w_end = min(sp_end, w_start + w_dur)
                if w_end <= w_start: continue

                line_parts = []
                for k, w in enumerate(chunk):
                    clean_w = w.upper().replace('"', '').replace('—', ' - ')
                    if k == j:
                        # Golden yellow highlight with subtle scale pop
                        line_parts.append(r"{\c&H0000D7FF&\3c&H000A0D14&\t(0,70,\fscx108\fscy108)\t(70,140,\fscx100\fscy100)}" + clean_w + r"{\c&H00FFFFFF&\3c&H000A0D14&}")
                    else:
                        line_parts.append(clean_w)
                display_text = " ".join(line_parts)
                events.append(f"Dialogue: 0,{format_ass(w_start)},{format_ass(w_end)},{sub_style},,0,0,0,,{display_text}")

    with open(sub_file, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
    print(f"Generated {len(events)} calibrated kinetic highlighted subtitle events.")

    # 7. Render V2 Master Video with BGM ducking and subtle branding
    print("\nRendering Master V2 Calibrated Video via FFmpeg...")
    sub_ass_escaped = sub_file.resolve().as_posix().replace(":", "\\:").replace("'", "\\'")
    logo_escaped = logo.resolve().as_posix().replace(":", "\\:").replace("'", "\\'")

    filter_complex = (
        f"[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[bg];"
        f"[bg][2:v]overlay=W-w-50:50:format=auto[vbranded];"
        f"[vbranded]subtitles='{sub_ass_escaped}'[vfinal];"
        f"[3:a]volume=0.08,afade=t=in:st=0:d=2.0,afade=t=out:st={total_video_dur-3.0:.2f}:d=3.0[bgm];"
        f"[1:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[afinal]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(video_concat_txt),
        "-i", str(mastered_voice_wav),
        "-loop", "1", "-i", str(logo.resolve()),
        "-stream_loop", "-1", "-i", str(bgm.resolve()),
        "-filter_complex", filter_complex,
        "-map", "[vfinal]",
        "-map", "[afinal]",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "320k",
        "-ar", "48000",
        "-t", f"{total_video_dur:.3f}",
        "-movflags", "+faststart",
        str(master_v2_mp4)
    ]

    subprocess.run(cmd, check=True)
    shutil.copy2(master_v2_mp4, central_v2_mp4)
    print(f"\n✅ Chapter 02 V2 Calibrated Film rendered successfully!")
    print(f"Local:   {master_v2_mp4.resolve().as_posix()}")
    print(f"Central: {central_v2_mp4.resolve().as_posix()}")

if __name__ == "__main__":
    main()
