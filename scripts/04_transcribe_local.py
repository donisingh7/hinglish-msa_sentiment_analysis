import os
import pandas as pd
from tqdm import tqdm
from faster_whisper import WhisperModel
from langdetect import detect_langs, LangDetectException

# ============================================
# CONFIG
# ============================================
CLIPS_DIR    = "data/clips"
FACE_CSV     = "data/clips_with_face.csv"
OUTPUT_ALL   = "data/transcriptions_all.csv"
OUTPUT_HINDI = "data/transcriptions_hinglish.csv"
DONE_LOG     = "data/download_logs/transcribed.txt"
CHECKPOINT   = "data/transcriptions_checkpoint.csv"

# ============================================
# LOAD MODEL
# ============================================
print("=" * 55)
print("  PHASE 4 — WHISPER TRANSCRIPTION (faster-whisper)")
print("=" * 55)
print("  Model  : large-v3")
print("  Device : CUDA (RTX 4050)")
print("=" * 55 + "\n")

print("Loading faster-whisper large-v3...")
model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16",
    cpu_threads=4,
    num_workers=2
)
print("✅ Model loaded\n")

# ============================================
# SIRF FACE WALE CLIPS LO
# ============================================
df_face  = pd.read_csv(FACE_CSV)
df_clips = df_face[df_face['has_face'] == True]
clip_ids = df_clips['clip_id'].tolist()

print(f"Total clips (with face) : {len(clip_ids)}")

# Resume support
os.makedirs("data/download_logs", exist_ok=True)
done_ids = set()
if os.path.exists(DONE_LOG):
    with open(DONE_LOG) as f:
        done_ids = set(f.read().splitlines())
    print(f"Already done           : {len(done_ids)}")

remaining = [c for c in clip_ids if c not in done_ids]
print(f"Remaining              : {len(remaining)}\n")

# Load checkpoint
results = []
if os.path.exists(CHECKPOINT):
    results = pd.read_csv(CHECKPOINT).to_dict('records')
    print(f"Checkpoint loaded: {len(results)} results")

# ============================================
# HINGLISH DETECTION
# ============================================
def is_hinglish(text):
    if not text or len(text.strip()) < 5:
        return False, 0.0, 0.0
    try:
        langs = detect_langs(text)
        ld    = {l.lang: l.prob for l in langs}
        hi    = ld.get('hi', 0.0)
        en    = ld.get('en', 0.0)
        return hi > 0.05 and en > 0.05, round(hi,3), round(en,3)
    except:
        return False, 0.0, 0.0

# ============================================
# MAIN LOOP
# ============================================
print("Starting — raat ko chalao, subah done!\n")

with tqdm(total=len(remaining), desc="Transcribing", unit="clip", ncols=80) as pbar:
    for i, clip_id in enumerate(remaining):
        clip_path = os.path.join(CLIPS_DIR, f"{clip_id}.wav")

        if not os.path.exists(clip_path):
            continue

        try:
            segments, info = model.transcribe(
                clip_path,
                language=None,
                beam_size=1,
                vad_filter=False,
                without_timestamps=True,
                condition_on_previous_text=False
            )

            text = " ".join([s.text for s in segments]).strip()
            lang = info.language
            mixed, hi, en = is_hinglish(text)

            results.append({
                "clip_id"      : clip_id,
                "video_id"     : clip_id.rsplit('_clip', 1)[0],
                "text"         : text,
                "whisper_lang" : lang,
                "hindi_score"  : hi,
                "english_score": en,
                "is_hinglish"  : mixed
            })

            with open(DONE_LOG, 'a') as f:
                f.write(f"{clip_id}\n")

        except Exception as e:
            results.append({
                "clip_id"      : clip_id,
                "video_id"     : clip_id.rsplit('_clip',1)[0],
                "text"         : "",
                "whisper_lang" : "error",
                "hindi_score"  : 0.0,
                "english_score": 0.0,
                "is_hinglish"  : False
            })

        hinglish_count = sum(1 for r in results if r['is_hinglish'])
        pbar.set_postfix({
            "hinglish": hinglish_count,
            "rate"    : f"{hinglish_count/max(len(results),1)*100:.1f}%",
            "lang"    : lang if 'lang' in dir() else "?"
        })
        pbar.update(1)

        if (i+1) % 500 == 0:
            pd.DataFrame(results).to_csv(CHECKPOINT, index=False)
            print(f"\n  Checkpoint saved [{i+1}] — Hinglish: {hinglish_count}")

# ============================================
# FINAL SAVE
# ============================================
df_all      = pd.DataFrame(results)
df_hinglish = df_all[df_all['is_hinglish'] == True]

df_all.to_csv(OUTPUT_ALL, index=False)
df_hinglish.to_csv(OUTPUT_HINDI, index=False)

print("\n" + "=" * 55)
print("  PHASE 4 COMPLETE")
print("=" * 55)
print(f"  Total transcribed : {len(df_all)}")
print(f"  Hinglish clips    : {len(df_hinglish)}")
print(f"  Filter rate       : {len(df_hinglish)/max(len(df_all),1)*100:.1f}%")
print(f"\n  Language breakdown:")
print(df_all['whisper_lang'].value_counts().head(8).to_string())
print("=" * 55)