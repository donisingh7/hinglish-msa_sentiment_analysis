import os
import cv2
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================
# CONFIG
# ============================================
FRAMES_DIR  = "data/raw_frames"
CLIPS_LOG   = "data/clips_log.csv"
OUTPUT_CSV  = "data/face_detection_results.csv"
MAX_WORKERS = 4

# ============================================
# FACE DETECTION — OpenCV Haar Cascade
# ============================================
def check_face_in_video(video_id):
    frames_path = os.path.join(FRAMES_DIR, video_id)

    if not os.path.exists(frames_path):
        return video_id, False, 0, 0

    frame_files = [f for f in os.listdir(frames_path) if f.endswith('.jpg')]

    if not frame_files:
        return video_id, False, 0, 0

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    face_count    = 0
    total_checked = 0

    for frame_file in frame_files:
        frame_path = os.path.join(frames_path, frame_file)
        try:
            img = cv2.imread(frame_path)
            if img is None:
                continue
            gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=4,
                minSize=(30, 30)
            )
            total_checked += 1
            if len(faces) > 0:
                face_count += 1
        except:
            continue

    has_face = (total_checked > 0) and (face_count / total_checked >= 0.4)
    return video_id, has_face, face_count, total_checked

# ============================================
# MAIN
# ============================================
df_clips  = pd.read_csv(CLIPS_LOG)
video_ids = df_clips['video_id'].unique().tolist()

print("=" * 55)
print("  PHASE 5 — FACE DETECTION (OpenCV)")
print("=" * 55)
print(f"  Videos to check : {len(video_ids)}")
print(f"  Workers         : {MAX_WORKERS}")
print("=" * 55 + "\n")

results = []

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {
        executor.submit(check_face_in_video, vid): vid
        for vid in video_ids
    }

    with tqdm(total=len(video_ids), desc="Face Detection", unit="video", ncols=75) as pbar:
        for future in as_completed(futures):
            video_id, has_face, face_cnt, total = future.result()
            results.append({
                "video_id"    : video_id,
                "has_face"    : has_face,
                "face_frames" : face_cnt,
                "total_frames": total
            })
            pbar.set_postfix({
                "with_face": sum(1 for r in results if r['has_face'])
            })
            pbar.update(1)

# ============================================
# SAVE + SUMMARY
# ============================================
df_results   = pd.DataFrame(results)
df_with_face = df_results[df_results['has_face'] == True]
df_results.to_csv(OUTPUT_CSV, index=False)

# Clips mein face info merge karo
df_clips_face = df_clips.merge(
    df_results[['video_id', 'has_face']],
    on='video_id', how='left'
)
df_clips_face.to_csv("data/clips_with_face.csv", index=False)

print("\n" + "=" * 55)
print("  PHASE 5 COMPLETE")
print("=" * 55)
print(f"  Total videos     : {len(df_results)}")
print(f"  With face        : {len(df_with_face)} ({len(df_with_face)/len(df_results)*100:.1f}%)")
print(f"  Without face     : {len(df_results)-len(df_with_face)}")
print(f"  Clips with face  : {len(df_clips_face[df_clips_face['has_face']==True])}")
print("=" * 55)
print("\n✅ Phase 5 done!")
