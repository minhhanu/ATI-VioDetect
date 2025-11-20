# backend/preprocessing/split_video.py
import time
from pathlib import Path
import os
import subprocess
import json

import os

os.environ["FFMPEG_BINARY"] = r"D:\ffmpeg lib\ffmpeg-2025-11-12-git-6cdd2cbe32-full_build\bin\ffmpeg.exe"
os.environ["FFPROBE_BINARY"] = r"D:\ffmpeg lib\ffmpeg-2025-11-12-git-6cdd2cbe32-full_build\bin\ffprobe.exe"

ffprobe_path = os.environ["FFPROBE_BINARY"]
    
def probe_video(video_path, ffprobe_path=ffprobe_path):
    """
    Probe video info safely on Windows
    Returns dictionary with video info
    """
    cmd = [
        ffprobe_path,
        "-v", "error",
        "-show_format",
        "-show_streams",
        "-print_format", "json",
        str(video_path)
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"[ERROR] ffprobe failed:\n{result.stderr}")
    return json.loads(result.stdout)

def split_video(video_path, ffprobe_path=ffprobe_path, duration=1):
    """
    Split a video into smaller clips of fixed duration (in seconds).
    Each clip is saved as {video_name}_{start}_{end}.mp4
    Example:
        fight.mp4  -->  fight_folder/fight_0_1.mp4, fight_1_2.mp4, ...
    """
    start_time = time.time()

    video_path = Path(video_path)
    output_dir = Path(f"{video_path.stem}_folder")
    os.makedirs(output_dir, exist_ok=True)

    # Get total duration using our safe probe
    probe = probe_video(video_path, ffprobe_path)
    total_duration = float(probe["format"]["duration"])

    start = 0
    while start < total_duration:
        end = min(start + duration, total_duration)

        # Clean filename: fight_0_1.mp4, not fight_0.00_1.00.mp4
        output_file = f"{video_path.stem}_{int(start)}_{int(end)}.mp4"
        output_path = output_dir / output_file

        cmd = [
            r"D:\ffmpeg lib\ffmpeg-2025-11-12-git-6cdd2cbe32-full_build\bin\ffmpeg.exe",
            "-y",                     # overwrite
            "-v", "error",            # suppress logs
            "-ss", str(start),
            "-to", str(end),
            "-i", str(video_path),
            "-c", "copy",
            str(output_path)
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"[ERROR] ffmpeg failed for scene {output_file}: {result.stderr}")
            raise RuntimeError(result.stderr)

        start += duration

    elapsed = time.time() - start_time
    num_files = len(list(output_dir.glob("*.mp4")))
    print(f"[INFO] Split complete → {num_files} scenes saved in '{output_dir}'")
    print(f"[TIME] Execution time: {elapsed:.2f} seconds")
    return output_dir
