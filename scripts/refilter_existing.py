# scripts/refilter_strict.py
import pandas as pd
import re

def is_genuinely_hinglish(text):
    """
    Sirf tabhi Hinglish maan lo jab:
    - Devanagari (Hindi) words bhi hain
    - AND actual Roman/Latin English words bhi hain (3+ characters)
    """
    if not isinstance(text, str) or len(text.strip()) < 5:
        return False

    has_devanagari = bool(re.search(r'[\u0900-\u097F]{2,}', text))
    has_latin      = bool(re.search(r'[a-zA-Z]{3,}', text))

    # Dono present tabhi genuine Hinglish
    return has_devanagari and has_latin

df = pd.read_csv("data/transcriptions_checkpoint.csv")
print(f"Total transcribed : {len(df)}")

df['is_hinglish'] = df['text'].apply(is_genuinely_hinglish)
df_hinglish = df[df['is_hinglish'] == True]

df.to_csv("data/transcriptions_all.csv", index=False)
df_hinglish.to_csv("data/transcriptions_hinglish.csv", index=False)

print(f"Genuine Hinglish  : {len(df_hinglish)}")
print(f"\nSample clips:")
print(df_hinglish[['clip_id','text']].head(10).to_string())