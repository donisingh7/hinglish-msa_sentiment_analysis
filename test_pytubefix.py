# test_pytubefix.py — root folder mein banao
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

url = "https://www.youtube.com/watch?v=5h37gpEyem8"

print("Downloading test video...")
yt = YouTube(url, on_progress_callback=on_progress, use_oauth=True, allow_oauth_cache=True)

print(f"Title: {yt.title}")

# 720p stream
stream = yt.streams.filter(
    progressive=False,
    file_extension='mp4'
).filter(
    resolution='720p'
).first()

# Fallback — best available
if not stream:
    stream = yt.streams.filter(
        progressive=True,
        file_extension='mp4'
    ).order_by('resolution').last()

print(f"Selected: {stream.resolution} {stream.mime_type}")
stream.download(output_path=".", filename="test_video.mp4")
print("✅ Download complete!")