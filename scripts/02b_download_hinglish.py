import os
import subprocess
import pandas as pd
from tqdm import tqdm
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
from pytubefix import YouTube

# ============================================
# CONFIG
# ============================================
VIDEO_LIST_PATH = "data/video_list_hinglish.csv"
AUDIO_DIR   = "data/hinglish_audio"
FRAMES_DIR  = "data/hinglish_frames"
TEMP_DIR    = "data/hinglish_temp"
LOG_DIR     = "data/hinglish_logs"
MAX_WORKERS     = 3

os.makedirs(AUDIO_DIR,  exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(LOG_DIR,    exist_ok=True)
os.makedirs(TEMP_DIR,   exist_ok=True)

# ============================================
# SPEED TRACKER
# ============================================
speed_lock    = threading.Lock()
recent_speeds = deque(maxlen=10)
total_bytes   = [0]

def update_speed(bytes_dl, elapsed):
    if elapsed > 0:
        mbps = (bytes_dl / (1024 * 1024)) / elapsed
        with speed_lock:
            recent_speeds.append(mbps)
            total_bytes[0] += bytes_dl

def avg_speed():
    with speed_lock:
        return sum(recent_speeds) / len(recent_speeds) if recent_speeds else 0.0

# ============================================
# LOAD VIDEO LIST + SKIP PROCESSED
# ============================================
df = pd.read_csv(VIDEO_LIST_PATH)
processed_log = os.path.join(LOG_DIR, "processed.txt")
failed_log    = os.path.join(LOG_DIR, "failed.txt")

processed_ids = set()
if os.path.exists(processed_log):
    with open(processed_log, 'r') as f:
        processed_ids = set(f.read().splitlines())

remaining_df = df[~df['video_id'].isin(processed_ids)]

print("=" * 62)
print("   PHASE 2 — BATCH DOWNLOAD (pytubefix | 720p)")
print("=" * 62)
print(f"  Total videos   : {len(df)}")
print(f"  Already done   : {len(processed_ids)}")
print(f"  Remaining      : {len(remaining_df)}")
print(f"  Parallel workers: {MAX_WORKERS}")
print(f"  Quality        : 720p adaptive (video) + best audio")
print("=" * 62 + "\n")

# ============================================
# PROCESS ONE VIDEO
# ============================================
def process_video(row):
    video_id = row['video_id']
    url      = row['url']
    start    = time.time()

    video_temp = os.path.join(TEMP_DIR, f"{video_id}_video.mp4")
    audio_temp = os.path.join(TEMP_DIR, f"{video_id}_audio")
    audio_wav  = os.path.join(AUDIO_DIR, f"{video_id}.wav")
    frames_dir = os.path.join(FRAMES_DIR, video_id)

    try:
        # ─────────────────────────────────────────
        # STEP 1: YouTube object banao
        # ─────────────────────────────────────────
        yt = YouTube(
            url,
            use_oauth=True,
            allow_oauth_cache=True
        )

        # ─────────────────────────────────────────
        # STEP 2: Video stream select karo (720p)
        # ─────────────────────────────────────────
        video_stream = yt.streams.filter(
            adaptive=True,
            file_extension='mp4',
            resolution='720p'
        ).first()

        # Fallback 1: highest available adaptive
        if not video_stream:
            video_stream = yt.streams.filter(
                adaptive=True,
                file_extension='mp4'
            ).order_by('resolution').last()

        # Fallback 2: progressive (video+audio)
        if not video_stream:
            video_stream = yt.streams.filter(
                progressive=True,
                file_extension='mp4'
            ).order_by('resolution').last()

        if not video_stream:
            return video_id, False, "No video stream", 0

        # ─────────────────────────────────────────
        # STEP 3: Audio stream select karo
        # ─────────────────────────────────────────
        audio_stream = yt.streams.filter(
            only_audio=True
        ).order_by('abr').last()

        if not audio_stream:
            # Progressive stream se hi audio nikalenge
            audio_stream = None

        # ─────────────────────────────────────────
        # STEP 4: Download karo
        # ─────────────────────────────────────────
        video_stream.download(
            output_path=TEMP_DIR,
            filename=f"{video_id}_video.mp4"
        )

        if audio_stream:
            audio_stream.download(
                output_path=TEMP_DIR,
                filename=f"{video_id}_audio"
            )
            # Actual downloaded file dhundho
            audio_temp_actual = None
            for f in os.listdir(TEMP_DIR):
                if f.startswith(f"{video_id}_audio"):
                    audio_temp_actual = os.path.join(TEMP_DIR, f)
                    break
        else:
            audio_temp_actual = video_temp  # progressive case

        # File size + speed track
        video_size = os.path.getsize(video_temp) if os.path.exists(video_temp) else 0
        audio_size = os.path.getsize(audio_temp_actual) if audio_temp_actual and os.path.exists(audio_temp_actual) else 0
        total_size = video_size + audio_size
        elapsed    = time.time() - start
        update_speed(total_size, elapsed)

        # ─────────────────────────────────────────
        # STEP 5: Audio → 16kHz mono WAV
        # ─────────────────────────────────────────
        source_for_audio = audio_temp_actual if audio_temp_actual else video_temp

        subprocess.run([
            "ffmpeg",
            "-i", source_for_audio,
            "-ac", "1",
            "-ar", "16000",
            "-vn",
            audio_wav,
            "-y",
            "-loglevel", "quiet"
        ], capture_output=True, timeout=120)

        # ─────────────────────────────────────────
        # STEP 6: 5 frames evenly extract karo
        # ─────────────────────────────────────────
        os.makedirs(frames_dir, exist_ok=True)

        # Video duration nikalo
        dur_result = subprocess.run([
            "ffprobe",
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            video_temp
        ], capture_output=True, text=True, timeout=30)

        try:
            duration = float(dur_result.stdout.strip())
        except:
            duration = 300.0  # default 5 min

        # 5 evenly spaced timestamps
        timestamps = [duration * j / 6 for j in range(1, 6)]

        for i, ts in enumerate(timestamps):
            subprocess.run([
                "ffmpeg",
                "-ss", str(round(ts, 2)),
                "-i", video_temp,
                "-vframes", "1",
                "-q:v", "2",
                os.path.join(frames_dir, f"frame_{i+1:02d}.jpg"),
                "-y",
                "-loglevel", "quiet"
            ], capture_output=True, timeout=30)

        # ─────────────────────────────────────────
        # STEP 7: Temp files delete karo
        # ─────────────────────────────────────────
        for f in os.listdir(TEMP_DIR):
            if f.startswith(video_id):
                try:
                    os.remove(os.path.join(TEMP_DIR, f))
                except:
                    pass

        # ─────────────────────────────────────────
        # STEP 8: Verify outputs
        # ─────────────────────────────────────────
        audio_ok  = os.path.exists(audio_wav) and os.path.getsize(audio_wav) > 1000
        frame_cnt = len(os.listdir(frames_dir)) if os.path.exists(frames_dir) else 0
        size_mb   = total_size / (1024 * 1024)
        res       = getattr(video_stream, 'resolution', '?')

        if audio_ok and frame_cnt > 0:
            return video_id, True, f"{res} | {size_mb:.0f}MB | {frame_cnt}frames", total_size
        elif audio_ok:
            return video_id, True, f"{res} | {size_mb:.0f}MB | no frames", total_size
        else:
            return video_id, False, f"audio missing | frames={frame_cnt}", 0

    except Exception as e:
        # Cleanup
        for f in os.listdir(TEMP_DIR):
            if f.startswith(video_id):
                try:
                    os.remove(os.path.join(TEMP_DIR, f))
                except:
                    pass
        err_msg = str(e)[:35]
        return video_id, False, err_msg, 0

# ============================================
# PARALLEL PROCESSING LOOP
# ============================================
rows           = [row for _, row in remaining_df.iterrows()]
success_count  = len(processed_ids)
fail_count     = 0
pipeline_start = time.time()

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(process_video, row): row for row in rows}

    with tqdm(
        total=len(rows),
        desc="Downloading",
        unit="vid",
        ncols=90
    ) as pbar:

        for future in as_completed(futures):
            video_id, success, message, fbytes = future.result()

            if success:
                success_count += 1
                with open(processed_log, 'a') as f:
                    f.write(f"{video_id}\n")
            else:
                fail_count += 1
                with open(failed_log, 'a') as f:
                    f.write(f"{video_id}: {message}\n")

            # Stats calculate
            done     = success_count + fail_count - len(processed_ids)
            elapsed  = time.time() - pipeline_start
            eta_min  = ((len(rows) - done) * (elapsed / max(done, 1))) / 60
            spd      = avg_speed()
            total_gb = total_bytes[0] / (1024 ** 3)

            pbar.set_postfix({
                "✅" : success_count,
                "❌" : fail_count,
                "spd": f"{spd:.1f}MB/s",
                "GB" : f"{total_gb:.1f}",
                "eta": f"{eta_min:.0f}m"
            })
            pbar.update(1)

# ============================================
# FINAL SUMMARY
# ============================================
total_min    = (time.time() - pipeline_start) / 60
audio_count  = len([f for f in os.listdir(AUDIO_DIR) if f.endswith('.wav')])
frames_count = len([f for f in os.listdir(FRAMES_DIR) if os.path.isdir(os.path.join(FRAMES_DIR, f))])

print("\n" + "=" * 62)
print("   PHASE 2 COMPLETE")
print("=" * 62)
print(f"  ✅ Success       : {success_count}")
print(f"  ❌ Failed        : {fail_count}")
print(f"  ⚡ Avg speed     : {avg_speed():.1f} MB/s")
print(f"  📦 Total data    : {total_bytes[0]/(1024**3):.2f} GB")
print(f"  ⏱️  Total time    : {total_min:.0f} mins")
print(f"  🎵 Audio (WAV)   : {audio_count} files")
print(f"  🖼️  Frame folders : {frames_count} folders")
print("=" * 62)
print("\n✅ Phase 2 done! Agle step ke liye Phase 3 (segmentation) ready.")