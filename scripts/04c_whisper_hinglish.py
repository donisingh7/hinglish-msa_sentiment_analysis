import os
import pandas as pd
from tqdm import tqdm
from faster_whisper import WhisperModel
from langdetect import detect_langs, LangDetectException
import re

# ============================================
# CONFIG
# ============================================
CLIPS_LOG    = "data/clips_log.csv"
FACE_CSV     = "data/hinglish_face_results.csv"
CLIPS_DIR    = "data/hinglish_clips"
OUTPUT_ALL   = "data/hinglish_transcriptions_all.csv"
OUTPUT_HINDI = "data/hinglish_transcriptions_hinglish.csv"
DONE_LOG     = "data/hinglish_logs/transcribed.txt"
CHECKPOINT   = "data/hinglish_transcriptions_checkpoint.csv"

os.makedirs("data/hinglish_logs", exist_ok=True)

# ============================================
# LOAD + MERGE — clip level data banana
# ============================================
df_clips = pd.read_csv(CLIPS_LOG)
df_face  = pd.read_csv(FACE_CSV)

print("Clips log columns :", df_clips.columns.tolist())
print("Face CSV columns  :", df_face.columns.tolist())

# Video level face results ko clip level pe merge karo
df_merged = df_clips.merge(
    df_face[['video_id', 'has_face']],
    on='video_id',
    how='left'
)

# Sirf face wale clips lo
df_face_clips = df_merged[df_merged['has_face'] == True]
clip_ids      = df_face_clips['clip_id'].tolist()

print(f"\nTotal clips        : {len(df_clips)}")
print(f"With face          : {len(clip_ids)}")

# ============================================
# RESUME SUPPORT
# ============================================
done_ids = set()
if os.path.exists(DONE_LOG):
    with open(DONE_LOG) as f:
        done_ids = set(f.read().splitlines())
    print(f"Already done       : {len(done_ids)}")

remaining = [c for c in clip_ids if c not in done_ids]
print(f"Remaining          : {len(remaining)}\n")

# Load checkpoint
results = []
if os.path.exists(CHECKPOINT):
    results = pd.read_csv(CHECKPOINT).to_dict('records')
    print(f"Checkpoint loaded  : {len(results)} results")

# ============================================
# LOAD WHISPER
# ============================================
print("Loading Whisper large-v3...")
model = WhisperModel(
    "large-v3",
    device="cuda",
    compute_type="float16",
    cpu_threads=4,
    num_workers=2
)
print("✅ Model loaded\n")

# ============================================
# IMPROVED HINGLISH DETECTION
# ============================================
def is_hinglish_improved(text):
    if text is None or not isinstance(text, str):
        return False, 0.0, 0.0
    text = text.strip()
    if len(text) < 5:
        return False, 0.0, 0.0

    has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
    has_latin      = bool(re.search(r'[a-zA-Z]{2,}', text))

    if has_devanagari and has_latin:
        return True, 0.5, 0.5

    loanwords = [
        r'ओके', r'कूल', r'नाइस', r'बेस्ट', r'ग्रेट', r'परफेक्ट',
        r'टोटली', r'एक्चुअली', r'बेसिकली', r'लिटरली', r'सीरियसली',
        r'वर्थ', r'वाइब्स', r'वाओ', r'सॉरी', r'थैंक', r'हेलो',
    ]
    if has_devanagari and any(re.search(w, text) for w in loanwords):
        return True, 0.5, 0.3

    try:
        langs = detect_langs(text)
        ld    = {l.lang: l.prob for l in langs}
        hi    = ld.get('hi', 0.0)
        en    = ld.get('en', 0.0)
        if hi > 0.05 and en > 0.05:
            return True, round(hi,3), round(en,3)
    except:
        pass

    return False, 0.0, 0.0

# ============================================
# MAIN LOOP
# ============================================
print("=" * 55)
print("  PHASE 4C — WHISPER (New Hinglish Videos)")
print("=" * 55)

with tqdm(total=len(remaining), desc="Transcribing", unit="clip", ncols=80) as pbar:
    for i, clip_id in enumerate(remaining):
        clip_path = os.path.join(CLIPS_DIR, f"{clip_id}.wav")

        if not os.path.exists(clip_path):
            pbar.update(1)
            continue

        try:
            segs, info = model.transcribe(
                clip_path,
                language=None,
                beam_size=1,
                vad_filter=False,
                without_timestamps=True,
                condition_on_previous_text=False
            )
            text = " ".join([s.text for s in segs]).strip()
            lang = info.language

            mixed, hi, en = is_hinglish_improved(text)

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
            "rate"    : f"{hinglish_count/max(len(results),1)*100:.1f}%"
        })
        pbar.update(1)

        if (i+1) % 500 == 0:
            pd.DataFrame(results).to_csv(CHECKPOINT, index=False)
            print(f"\n  [{i+1}] Hinglish: {hinglish_count}")

# ============================================
# SAVE
# ============================================
df_all      = pd.DataFrame(results)
df_hinglish = df_all[df_all['is_hinglish'] == True]

df_all.to_csv(OUTPUT_ALL, index=False)
df_hinglish.to_csv(OUTPUT_HINDI, index=False)

print("\n" + "=" * 55)
print("  PHASE 4C COMPLETE")
print("=" * 55)
print(f"  Transcribed   : {len(df_all)}")
print(f"  Hinglish      : {len(df_hinglish)}")
print(f"  Rate          : {len(df_hinglish)/max(len(df_all),1)*100:.1f}%")
print("=" * 55)