# scripts/combine_datasets.py
import pandas as pd

# Old Hinglish clips (already found)
df_old = pd.read_csv("data/transcriptions_hinglish.csv")

# New Hinglish clips
df_new = pd.read_csv("data/hinglish_transcriptions_hinglish.csv")

# Combine + deduplicate
df_combined = pd.concat([df_old, df_new]).drop_duplicates('clip_id')
df_combined.to_csv("data/final_hinglish_dataset.csv", index=False)

print(f"Old clips  : {len(df_old)}")
print(f"New clips  : {len(df_new)}")
print(f"Combined   : {len(df_combined)}")