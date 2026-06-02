import os
import pandas as pd
from tqdm import tqdm
from faster_whisper import WhisperModel
import torch

# ============================================
# CONFIG
# ============================================
FACE_CSV     = "data/clips_with_face.csv"
PRESCREEN_CSV = "data/prescreen_results.csv"
CLIPS_DIR    = "data/clips"

# ============================================
# TINY MODEL — sirf language detect karo
# ============================================
print("Loading Whisper tiny (fast pre-screening)...")
model = WhisperModel(
    "tiny",
    device="cuda",
    compute_type="float16"
)
print("✅ Tiny model loaded\n")

df = pd.read_csv(FACE_CSV)
clip_ids = df[df['has_face'] == True]['clip_id'].tolist()

# Already screened skip karo
done_log = "data/download_logs/prescreened.txt"
done_ids = set()
if os.path.exists(done_log):
    with open(done_log) as f:
        done_ids = set(f.read().splitlines())

remaining = [c for c in clip_ids if c not in done_ids]

print(f"Total clips    : {len(clip_ids)}")
print(f"Already done   : {len(done_ids)}")
print(f"Remaining      : {len(remaining)}\n")

results = []

with tqdm(total=len(remaining), desc="Pre-screening", unit="clip", ncols=80) as pbar:
    for clip_id in remaining:
        clip_path = os.path.join(CLIPS_DIR, f"{clip_id}.wav")
        if not os.path.exists(clip_path):
            continue

        try:
            # Sirf language detect — no full transcription
            _, info = model.transcribe(
                clip_path,
                language=None,
                beam_size=1,
                without_timestamps=True,
                vad_filter=False,
                condition_on_previous_text=False
            )

            lang       = info.language
            lang_prob  = info.language_probability

            # Hinglish likely hone ke conditions:
            # 1. Hindi detect hua (Hindi speaker = potentially Hinglish)
            # 2. Ya English with low confidence (code-mixed confusion)
            likely_hinglish = (
                lang == 'hi' or
                (lang == 'en' and lang_prob < 0.85) or
                lang_prob < 0.80  # Model confused → mixed language
            )

            results.append({
                "clip_id"         : clip_id,
                "video_id"        : clip_id.rsplit('_clip', 1)[0],
                "detected_lang"   : lang,
                "lang_probability": round(lang_prob, 3),
                "likely_hinglish" : likely_hinglish
            })

            with open(done_log, 'a') as f:
                f.write(f"{clip_id}\n")

        except:
            results.append({
                "clip_id"         : clip_id,
                "video_id"        : clip_id.rsplit('_clip',1)[0],
                "detected_lang"   : "error",
                "lang_probability": 0.0,
                "likely_hinglish" : False
            })

        likely_count = sum(1 for r in results if r['likely_hinglish'])
        pbar.set_postfix({
            "likely": likely_count,
            "rate"  : f"{likely_count/max(len(results),1)*100:.0f}%"
        })
        pbar.update(1)

# ============================================
# SAVE
# ============================================
df_results  = pd.DataFrame(results)
df_likely   = df_results[df_results['likely_hinglish'] == True]

df_results.to_csv(PRESCREEN_CSV, index=False)

print("\n" + "=" * 55)
print("  PRE-SCREENING COMPLETE")
print("=" * 55)
print(f"  Total screened    : {len(df_results)}")
print(f"  Likely Hinglish   : {len(df_likely)} ({len(df_likely)/len(df_results)*100:.1f}%)")
print(f"  Skip karo         : {len(df_results)-len(df_likely)}")
print(f"\n  Time saved on Step 2: ~{(len(df_results)-len(df_likely))*2//3600:.0f} hrs")
print("=" * 55)