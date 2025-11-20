import os
import time
import ffmpeg
from pathlib import Path

def split_video(video_path, duration=1):
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

    # Get total duration
    probe = ffmpeg.probe(str(video_path))
    total_duration = float(probe["format"]["duration"])

    start = 0
    while start < total_duration:
        end = min(start + duration, total_duration)

        # Clean filename: fight_0_1.mp4, not fight_0.00_1.00.mp4
        output_file = f"{video_path.stem}_{int(start)}_{int(end)}.mp4"
        output_path = output_dir / output_file

        (
            ffmpeg
            .input(str(video_path), ss=start, to=end)
            .output(str(output_path), c="copy", loglevel="error")
            .run(quiet=True)
        )

        start += duration

    elapsed = time.time() - start_time
    num_files = len(list(output_dir.glob("*.mp4")))
    print(f"[INFO] Split complete → {num_files} scenes saved in '{output_dir}'")
    print(f"[TIME] Execution time: {elapsed:.2f} seconds")