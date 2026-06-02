import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from googleapiclient.discovery import build
import pandas as pd
from tqdm import tqdm
import time
from config import YOUTUBE_API_KEY

# Specifically Hinglish creators aur content
HINGLISH_QUERIES = [
    # Specific well-known Hinglish creators
    "Mostly Sane vlog 2024",
    "Prajakta Koli video Hindi",
    "Ranveer Allahbadia podcast Hindi English",
    "Technical Guruji review 2024",
    "Niharika NM video Hindi English",
    "Mumbiker Nikhil vlog Hindi",
    "Ashish Chanchlani video 2024",
    "Triggered Insaan video Hindi English",
    "Round2Hell video 2024",
    "Sourav Joshi vlog Hindi English",
    "Bhuvan Bam video Hindi English",
    "CarryMinati video Hindi English",
    "Fukra Insaan Hindi English",
    "Elvish Yadav Hindi English vlog",

    # Content types known for Hinglish
    "honest product review Hindi English 2024",
    "unboxing Hindi English mix honest",
    "Hinglish podcast episode 2024",
    "India vlog Hindi English couple",
    "startup founder Hindi English talk",
    "college life vlog Hindi English",
    "Delhi vlog Hindi English 2024",
    "Mumbai vlog Hinglish 2024",
    "job interview prep Hindi English",
    "coding tutorial Hindi English 2024",
    "gym workout Hindi English motivation",
    "skin care routine Hindi English",
]

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def search_videos(query, max_results=50):
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            videoDuration="medium",
            videoDefinition="high",
            relevanceLanguage="hi",
            regionCode="IN",
            maxResults=max_results,
            fields="items(id/videoId,snippet/title,snippet/channelTitle,snippet/publishedAt)"
        )
        return request.execute().get("items", [])
    except Exception as e:
        print(f"Error: {e}")
        return []

all_videos = []
seen_ids   = set()

# Load old video IDs to avoid duplicates
old_df = pd.read_csv("data/video_list.csv")
seen_ids.update(old_df['video_id'].tolist())
print(f"Existing videos (skip): {len(seen_ids)}")

for query in tqdm(HINGLISH_QUERIES, desc="Searching"):
    results = search_videos(query)
    new = 0
    for item in results:
        vid = item['id']['videoId']
        if vid in seen_ids:
            continue
        seen_ids.add(vid)
        all_videos.append({
            "video_id" : vid,
            "title"    : item['snippet']['title'],
            "channel"  : item['snippet']['channelTitle'],
            "published": item['snippet']['publishedAt'],
            "url"      : f"https://www.youtube.com/watch?v={vid}",
            "query_used": query
        })
        new += 1
    print(f"  '{query[:40]}' → {new} new")
    time.sleep(0.5)

df_new = pd.DataFrame(all_videos)
df_new.to_csv("data/video_list_hinglish.csv", index=False)

print(f"\n✅ New Hinglish videos: {len(df_new)}")
print(f"   Saved: data/video_list_hinglish.csv")