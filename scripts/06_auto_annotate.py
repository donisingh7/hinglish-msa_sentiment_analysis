import os
import json
import time
import re
import pandas as pd
from tqdm import tqdm
from groq import Groq
import sys
sys.path.insert(0, '.')
from config import GROQ_API_KEY

# ============================================
# CONFIG
# ============================================
HINGLISH_CSV = "data/transcriptions_hinglish.csv"
OUTPUT_CSV   = "data/auto_labeled.csv"
DONE_LOG     = "data/download_logs/annotated.txt"
client       = Groq(api_key=GROQ_API_KEY)

# Groq free tier: 30 req/min
# 2 second sleep = safe under limit
SLEEP_BETWEEN = 0.1

# Simple prompt — just asks for number, no JSON
PROMPT = """Rate this Hinglish text sentiment: -3 (very negative) to +3 (very positive).
Return ONLY a single number like: -2.5 or 1.0 or 0

Text: "{text}"

Number:"""

# ============================================
# LOAD DATA
# ============================================
df = pd.read_csv(HINGLISH_CSV)
print("=" * 55)
print("  PHASE 6 — GROQ AUTO ANNOTATION")
print("=" * 55)
print(f"  Total clips : {len(df)}")

# Resume support
os.makedirs("data/download_logs", exist_ok=True)
done_ids = set()
if os.path.exists(DONE_LOG):
    with open(DONE_LOG) as f:
        done_ids = set(f.read().splitlines())
    print(f"  Already done: {len(done_ids)}")

# Load existing results
results = []
if os.path.exists(OUTPUT_CSV):
    existing = pd.read_csv(OUTPUT_CSV)
    results  = existing.to_dict('records')
    print(f"  Loaded existing: {len(results)}")

remaining = df[~df['clip_id'].isin(done_ids)]
print(f"  Remaining   : {len(remaining)}")
print(f"  Est. time   : ~{len(remaining)*SLEEP_BETWEEN/3600:.1f} hrs")
print("=" * 55 + "\n")

# ============================================
# ANNOTATE — ONE BY ONE
# ============================================
def parse_score(raw_text):
    """Extract float score from model response."""
    raw = raw_text.strip()
    # Try direct float parse
    try:
        score = float(raw.split()[0])
        return max(-3.0, min(3.0, score))
    except:
        pass
    # Try regex
    match = re.search(r'[-+]?\d+\.?\d*', raw)
    if match:
        score = float(match.group())
        return max(-3.0, min(3.0, score))
    return 0.0  # default neutral

with tqdm(total=len(remaining), desc="Annotating", unit="clip", ncols=80) as pbar:
    for _, row in remaining.iterrows():
        clip_id = row['clip_id']
        text    = str(row['text'])[:300]  # truncate long texts

        score      = 0.0
        confidence = "medium"

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{
                    "role"   : "user",
                    "content": PROMPT.format(text=text)
                }],
                max_tokens=10,
                temperature=0.1
            )

            raw   = response.choices[0].message.content.strip()
            score = parse_score(raw)

            # Confidence based on how extreme the score is
            if abs(score) >= 1.5:
                confidence = "high"
            elif abs(score) >= 0.5:
                confidence = "medium"
            else:
                confidence = "low"

        except Exception as e:
            err = str(e)
            if "rate_limit" in err.lower() or "429" in err:
                time.sleep(60)  # Rate limit → wait 1 min
            elif "timeout" in err.lower() or "connection" in err.lower():
                time.sleep(10)  # Network error → wait 10 sec
            # score stays 0.0, confidence = medium

        results.append({
            "clip_id"      : clip_id,
            "video_id"     : row.get('video_id', ''),
            "text"         : text,
            "score"        : score,
            "confidence"   : confidence,
            "whisper_lang" : row.get('whisper_lang', ''),
            "hindi_score"  : row.get('hindi_score', 0),
            "english_score": row.get('english_score', 0)
        })

        with open(DONE_LOG, 'a') as f:
            f.write(f"{clip_id}\n")

        high_conf = sum(1 for r in results if r['confidence'] == 'high')
        pbar.set_postfix({
            "done"  : len(results),
            "high"  : high_conf
        })
        pbar.update(1)

        # Har 200 clips pe save karo
        if len(results) % 200 == 0:
            pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)

        time.sleep(SLEEP_BETWEEN)

# ============================================
# FINAL SAVE
# ============================================
df_out   = pd.DataFrame(results)
df_train = df_out[df_out['confidence'].isin(['high', 'medium'])]

df_out.to_csv(OUTPUT_CSV, index=False)
df_train.to_csv("data/train_set.csv", index=False)

print("\n" + "=" * 55)
print("  PHASE 6 COMPLETE")
print("=" * 55)
print(f"  Total        : {len(df_out)}")
print(f"  High conf    : {sum(df_out['confidence']=='high')}")
print(f"  Medium conf  : {sum(df_out['confidence']=='medium')}")
print(f"  Training set : {len(df_train)}")
print("=" * 55)