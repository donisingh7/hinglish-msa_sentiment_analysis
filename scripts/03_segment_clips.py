import os
import subprocess
import pandas as pd
from tqdm import tqdm
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================
# CONFIG
# ============================================
AUDIO_DIR    = "data/raw_audio"
CLIPS_DIR    = "data/clips"
FRAMES_DIR   = "data/raw_frames"
LOG_DIR      = "data/download_logs"
MIN_DURATION = 3.0    # minimum clip length (seconds)
MAX_DURATION = 15.0   # maximum clip length (seconds)
MAX_WORKERS  = 4

os.makedirs(CLIPS_DIR, exist_ok=True)

# ============================================
# SEGMENT ONE AUDIO FILE
# ============================================
def get_silence_timestamps(audio_path):
    """ffmpeg se silence detect karke speech segments nikalo"""
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-af", "silencedetect=noise=-35dB:d=0.4",
        "-f", "null", "-"
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=120
    )
    output = result.stderr

    # Silence timestamps parse karo
    silence_starts = []
    silence_ends   = []

    for line in output.split('\n'):
        if 'silence_start' in line:
            try:
                val = float(line.split('silence_start:')[1].strip())
                silence_starts.append(val)
            except:
                pass
        if 'silence_end' in line:
            try:
                val = float(line.split('silence_end:')[1].split('|')[0].strip())
                silence_ends.append(val)
            except:
                pass

    return silence_starts, silence_ends

def get_audio_duration(audio_path):
    """Audio duration nikalo"""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-show_entries", "format=duration",
        "-of", "csv=p=0", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        return float(result.stdout.strip())
    except:
        return 0.0

def cut_audio_clip(audio_path, start, end, output_path):
    """Ek clip cut karo"""
    cmd = [
        "ffmpeg",
        "-ss", str(round(start, 3)),
        "-to", str(round(end, 3)),
        "-i", audio_path,
        "-ac", "1", "-ar", "16000",
        output_path,
        "-y", "-loglevel", "quiet"
    ]
    subprocess.run(cmd, capture_output=True, timeout=30)
    return os.path.exists(output_path) and os.path.getsize(output_path) > 500

def process_audio(audio_file):
    """Ek video ki audio ko clips mein convert karo"""
    video_id   = audio_file.replace('.wav', '')
    audio_path = os.path.join(AUDIO_DIR, audio_file)
    clips_made = []

    try:
        # Total duration
        duration = get_audio_duration(audio_path)
        if duration < MIN_DURATION:
            return video_id, 0, "Too short"

        # Silence detect karo
        silence_starts, silence_ends = get_silence_timestamps(audio_path)

        # Speech segments banao (silence ke beech ka hissa)
        speech_segments = []

        # Pehle silence se pehle ka segment
        if silence_starts:
            if silence_starts[0] > MIN_DURATION:
                speech_segments.append((0.0, silence_starts[0]))
        else:
            # Koi silence nahi — poori audio ek segment
            speech_segments.append((0.0, duration))

        # Silences ke beech ke segments
        for i in range(len(silence_ends)):
            seg_start = silence_ends[i]
            seg_end   = silence_starts[i+1] if i+1 < len(silence_starts) else duration

            seg_duration = seg_end - seg_start
            if seg_duration >= MIN_DURATION:
                speech_segments.append((seg_start, seg_end))

        # Long segments ko MAX_DURATION mein toddo
        final_segments = []
        for seg_start, seg_end in speech_segments:
            seg_dur = seg_end - seg_start
            if seg_dur <= MAX_DURATION:
                final_segments.append((seg_start, seg_end))
            else:
                # Split into smaller pieces
                current = seg_start
                while current < seg_end:
                    chunk_end = min(current + MAX_DURATION, seg_end)
                    if chunk_end - current >= MIN_DURATION:
                        final_segments.append((current, chunk_end))
                    current = chunk_end

        # Clips cut karo
        for i, (seg_start, seg_end) in enumerate(final_segments):
            clip_id    = f"{video_id}_clip{i:04d}"
            clip_path  = os.path.join(CLIPS_DIR, f"{clip_id}.wav")

            success = cut_audio_clip(audio_path, seg_start, seg_end, clip_path)
            if success:
                clips_made.append({
                    "clip_id"  : clip_id,
                    "video_id" : video_id,
                    "start"    : round(seg_start, 3),
                    "end"      : round(seg_end, 3),
                    "duration" : round(seg_end - seg_start, 3),
                    "clip_path": clip_path
                })

        return video_id, len(clips_made), clips_made

    except Exception as e:
        return video_id, 0, str(e)[:40]

# ============================================
# MAIN LOOP
# ============================================
audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.wav')]

print("=" * 60)
print("  PHASE 3 — CLIP SEGMENTATION (ffmpeg)")
print("=" * 60)
print(f"  Audio files   : {len(audio_files)}")
print(f"  Clip duration : {MIN_DURATION}s – {MAX_DURATION}s")
print(f"  Workers       : {MAX_WORKERS}")
print(f"  Est. time     : ~{len(audio_files)//MAX_WORKERS//60 + 5} mins")
print("=" * 60 + "\n")

all_clips   = []
total_clips = 0
failed      = 0

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {
        executor.submit(process_audio, af): af
        for af in audio_files
    }

    with tqdm(total=len(audio_files), desc="Segmenting", unit="video", ncols=80) as pbar:
        for future in as_completed(futures):
            result = future.result()
            video_id = result[0]
            count    = result[1]
            clips    = result[2]

            if isinstance(clips, list):
                all_clips.extend(clips)
                total_clips += count
            else:
                failed += 1

            pbar.set_postfix({
                "clips": total_clips,
                "failed": failed
            })
            pbar.update(1)

# ============================================
# SAVE CLIPS LOG
# ============================================
df_clips = pd.DataFrame(all_clips)
df_clips.to_csv("data/clips_log.csv", index=False)

print("\n" + "=" * 60)
print("  PHASE 3 COMPLETE")
print("=" * 60)
print(f"  Videos processed : {len(audio_files) - failed}")
print(f"  Total clips made : {total_clips}")
print(f"  Failed videos    : {failed}")
print(f"  Avg clips/video  : {total_clips // max(len(audio_files)-failed, 1)}")
print(f"  Clips saved to   : data/clips/")
print(f"  Log saved to     : data/clips_log.csv")
print("=" * 60)
print("\n✅ Phase 3 done! Ab Phase 4 (transcription + filtering) ready.")