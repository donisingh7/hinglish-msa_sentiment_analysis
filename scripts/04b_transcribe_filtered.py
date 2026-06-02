import os
import json
import pandas as pd
from tqdm import tqdm
from faster_whisper import WhisperModel
from langdetect import detect_langs, LangDetectException
import re

# ============================================
# CONFIG
# ============================================
PRESCREEN_CSV = "data/prescreen_results.csv"
CLIPS_DIR     = "data/clips"
OUTPUT_ALL    = "data/transcriptions_all.csv"
OUTPUT_HINDI  = "data/transcriptions_hinglish.csv"
DONE_LOG      = "data/download_logs/transcribed_v2.txt"
CHECKPOINT    = "data/transcriptions_checkpoint_v2.csv"

# ============================================
# LOAD ONLY LIKELY HINGLISH CLIPS
# ============================================
df_screen = pd.read_csv(PRESCREEN_CSV)
df_likely = df_screen[df_screen['likely_hinglish'] == True]
clip_ids  = df_likely['clip_id'].tolist()

print(f"Pre-screened clips  : {len(clip_ids)}")

# Resume support
done_ids = set()
if os.path.exists(DONE_LOG):
    with open(DONE_LOG) as f:
        done_ids = set(f.read().splitlines())

remaining = [c for c in clip_ids if c not in done_ids]
print(f"Remaining           : {len(remaining)}\n")

# ============================================
# LARGE-V3 MODEL LOAD
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
def is_hinglish(text_devanagari, text_roman=""):
    if not text_devanagari or len(text_devanagari.strip()) < 5:
        return False, 0.0, 0.0

    has_devanagari = bool(re.search(r'[\u0900-\u097F]', text_devanagari))
    has_latin      = bool(re.search(r'[a-zA-Z]{2,}', text_devanagari))

    # Roman text mein check
    if text_roman:
        english_words = len(re.findall(r'\b[a-zA-Z]{3,}\b', text_roman))
        total_words   = len(text_roman.split())
        en_ratio      = english_words / max(total_words, 1)
        if has_devanagari and en_ratio > 0.10:
            return True, 0.5, round(en_ratio, 3)

    # Devanagari + Latin dono present
    if has_devanagari and has_latin:
        return True, 0.5, 0.5

    # langdetect
    try:
        langs = detect_langs(text_devanagari)
        ld    = {l.lang: l.prob for l in langs}
        hi    = ld.get('hi', 0.0)
        en    = ld.get('en', 0.0)
        if hi > 0.05 and en > 0.05:
            return True, round(hi,3), round(en,3)
    except:
        pass

    return False, 0.0, 0.0

# ============================================
# TRANSCRIBE + DETECT
# ============================================
results = []
if os.path.exists(CHECKPOINT):
    results = pd.read_csv(CHECKPOINT).to_dict('records')

with tqdm(total=len(remaining), desc="Transcribing", unit="clip", ncols=80) as pbar:
    for i, clip_id in enumerate(remaining):
        clip_path = os.path.join(CLIPS_DIR, f"{clip_id}.wav")
        if not os.path.exists(clip_path):
            continue

        try:
            # Pass 1: Auto language
            segs1, info = model.transcribe(
                clip_path,
                language=None,
                beam_size=1,
                vad_filter=False,
                without_timestamps=True,
                condition_on_previous_text=False
            )
            text1 = " ".join([s.text for s in segs1]).strip()
            lang  = info.language

            # Pass 2: Agar Hindi → Roman mein bhi transcribe
            text2 = ""
            if lang == 'hi':
                segs2, _ = model.transcribe(
                    clip_path,
                    language="en",
                    beam_size=1,
                    vad_filter=False,
                    without_timestamps=True,
                    condition_on_previous_text=False
                )
                text2 = " ".join([s.text for s in segs2]).strip()

            mixed, hi, en = is_hinglish(text1, text2)

            results.append({
                "clip_id"      : clip_id,
                "video_id"     : clip_id.rsplit('_clip',1)[0],
                "text"         : text1,
                "text_roman"   : text2,
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
                "text_roman"   : "",
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

# ============================================
# SAVE
# ============================================
df_all      = pd.DataFrame(results)
df_hinglish = df_all[df_all['is_hinglish'] == True]

df_all.to_csv(OUTPUT_ALL, index=False)
df_hinglish.to_csv(OUTPUT_HINDI, index=False)

print("\n" + "=" * 55)
print("  PHASE 4 COMPLETE")
print("=" * 55)
print(f"  Clips transcribed : {len(df_all)}")
print(f"  Hinglish clips    : {len(df_hinglish)}")
print(f"  Rate              : {len(df_hinglish)/max(len(df_all),1)*100:.1f}%")
print("=" * 55)