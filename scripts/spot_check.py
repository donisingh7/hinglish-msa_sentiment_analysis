# spot_check.py — isko scripts/ mein banao
import pandas as pd
import random

df = pd.read_csv("data/video_list.csv")
sample = df.sample(n=30, random_state=42)

print("=" * 60)
print("  SPOT CHECK — 30 RANDOM VIDEOS")
print("  In kholo aur confirm karo Hinglish hai")
print("=" * 60)

for i, (_, row) in enumerate(sample.iterrows(), 1):
    print(f"\n[{i:02d}] {row['title'][:55]}")
    print(f"      Channel : {row['channel']}")
    print(f"      URL     : {row['url']}")