# scripts/07_sample_test_set.py
import pandas as pd, os

# Use auto_labeled if train_set not ready yet
src = "data/train_set.csv" if os.path.exists("data/train_set.csv") else "data/auto_labeled.csv"
df  = pd.read_csv(src)
df  = df[df['confidence'].isin(['high', 'medium'])]

n   = min(150, len(df))
test = df.sample(n=n, random_state=42)
test = test[['clip_id', 'video_id', 'text', 'score', 'whisper_lang']]
test.to_csv("data/test_set_to_annotate.csv", index=False)
print(f"Source     : {src}")
print(f"Test clips : {len(test)}")
print(f"Saved      : data/test_set_to_annotate.csv")
print("Next: add 'score' column manually (-3 to +3) -> save as test_set_gold.csv")