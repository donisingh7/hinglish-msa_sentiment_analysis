import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from googleapiclient.discovery import build
import pandas as pd
from tqdm import tqdm
import time

# Config
from config import YOUTUBE_API_KEY

# ============================================
# 25 SEARCH QUERIES — 10 CATEGORIES
# ============================================
SEARCH_QUERIES = [
    # Tech Reviews (3)
    "tech review Hindi English 2024",
    "smartphone review Hinglish honest",
    "laptop review Hindi English mix",

    # Food Reviews (2)
    "food review Hindi English vlog 2024",
    "restaurant review Hinglish",

    # Movie/Web Series Reviews (3)
    "movie review Hindi English mix 2024",
    "web series review Hinglish honest",
    "OTT review Hindi English opinion",

    # Daily Vlogs (3)
    "daily vlog Hinglish 2024",
    "day in my life Hindi English",
    "college vlog Hinglish India",

    # Reaction Videos (2)
    "reaction video Hinglish 2024",
    "reacting Hindi English mix",

    # Opinion/Rant (3)
    "honest opinion Hindi English",
    "rant video Hinglish India",
    "controversial topic Hindi English opinion",

    # Podcast Clips (3)
    "podcast Hindi English mix 2024",
    "interview Hindi English mix India",
    "conversation Hinglish podcast clips",

    # Unboxing (2)
    "unboxing video Hinglish 2024",
    "unboxing review Hindi English honest",

    # Travel Vlogs (2)
    "travel vlog Hindi English mix India",
    "trip vlog Hinglish 2024",

    # Comedy/Roast (2)
    "comedy video Hinglish India",
    "roast video Hindi English mix",
]

MAX_RESULTS_PER_QUERY = 50  # YouTube API max per call

# ============================================
# YOUTUBE API SETUP
# ============================================
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# ============================================
# SEARCH FUNCTION
# ============================================
def search_videos(query, max_results=50):
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            videoDuration="medium",        # 4-20 minutes
            videoDefinition="high",        # HD only
            relevanceLanguage="hi",        # Hindi relevance
            regionCode="IN",               # India region
            maxResults=max_results,
            fields="items(id/videoId,snippet/title,snippet/channelTitle,snippet/publishedAt)"
        )
        response = request.execute()
        return response.get("items", [])
    except Exception as e:
        print(f"  ⚠️  Error for query '{query}': {e}")
        return []

# ============================================
# MAIN COLLECTION LOOP
# ============================================
print("=" * 60)
print("  PHASE 1 — HINGLISH VIDEO DISCOVERY")
print("=" * 60)
print(f"  Total queries: {len(SEARCH_QUERIES)}")
print(f"  Max results per query: {MAX_RESULTS_PER_QUERY}")
print(f"  Expected total: ~{len(SEARCH_QUERIES) * MAX_RESULTS_PER_QUERY} videos")
print("=" * 60 + "\n")

all_videos = []
seen_ids = set()

for i, query in enumerate(tqdm(SEARCH_QUERIES, desc="Searching")):
    results = search_videos(query, MAX_RESULTS_PER_QUERY)
    new_count = 0

    for item in results:
        video_id = item['id']['videoId']

        # Duplicate check
        if video_id in seen_ids:
            continue

        seen_ids.add(video_id)
        snippet = item['snippet']

        all_videos.append({
            "video_id": video_id,
            "title": snippet.get('title', ''),
            "channel": snippet.get('channelTitle', ''),
            "published": snippet.get('publishedAt', ''),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "query_used": query
        })
        new_count += 1

    print(f"  Query {i+1:02d}: '{query[:45]}...' → {new_count} new videos")

    # Rate limit avoid karne ke liye
    time.sleep(0.5)

# ============================================
# SAVE RESULTS
# ============================================
df = pd.DataFrame(all_videos)
output_path = "data/video_list.csv"
df.to_csv(output_path, index=False)

print("\n" + "=" * 60)
print("  RESULTS SUMMARY")
print("=" * 60)
print(f"  Total unique videos found : {len(df)}")
print(f"  Total queries used        : {len(SEARCH_QUERIES)}")
print(f"  Duplicates removed        : {len(SEARCH_QUERIES)*50 - len(df)}")
print(f"  Saved to                  : {output_path}")
print("=" * 60)
print("\n✅ Phase 1 Complete — video_list.csv ready!")
print("📋 Next: Spot check 30 random URLs before Phase 2")