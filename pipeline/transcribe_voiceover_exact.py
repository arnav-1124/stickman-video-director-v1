import sys
import json
from pathlib import Path
from faster_whisper import WhisperModel

def main():
    root_dir = Path(".").resolve()
    ep_dir = root_dir / "projects/long/ep02_how_humans_invented_the_first_lie"
    audio_path = ep_dir / "audio/voiceover_038s_calibrated.wav"
    output_words_json = ep_dir / "audio/exact_word_timestamps.json"
    output_segments_json = ep_dir / "audio/exact_segment_timestamps.json"

    print("=" * 60)
    print("EXACT AUDIO ANALYSIS: Word & Letter Level Alignment")
    print(f"Target Audio: {audio_path.name}")
    print("=" * 60)

    # Use 'base.en' or 'small.en' on CPU with int8 compute for high speed & precision
    print("\nLoading WhisperModel ('base.en')...")
    model = WhisperModel("base.en", device="cpu", compute_type="int8")

    print("Running cross-attention DTW word-level alignment...")
    segments, info = model.transcribe(
        str(audio_path),
        beam_size=5,
        word_timestamps=True,
        vad_filter=False  # Keep all audio aligned
    )

    all_words = []
    all_segments = []

    for seg in segments:
        seg_data = {
            "id": seg.id,
            "start": round(seg.start, 3),
            "end": round(seg.end, 3),
            "text": seg.text.strip(),
            "words": []
        }
        for w in seg.words:
            w_data = {
                "word": w.word.strip(),
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "probability": round(w.probability, 3)
            }
            seg_data["words"].append(w_data)
            all_words.append(w_data)
        all_segments.append(seg_data)

    print(f"\nExtracted {len(all_segments)} segments and {len(all_words)} exact word timestamps.")

    with open(output_words_json, "w", encoding="utf-8") as f:
        json.dump(all_words, f, indent=2)

    with open(output_segments_json, "w", encoding="utf-8") as f:
        json.dump(all_segments, f, indent=2)

    print(f"Saved: {output_words_json.name}")
    print(f"Saved: {output_segments_json.name}")

if __name__ == "__main__":
    main()
