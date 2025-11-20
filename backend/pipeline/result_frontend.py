import re
import time
import json
from datetime import timedelta

def convert_scene_results(scene_data):
    """
    Convert scene-level predictions like:
      {'scene_path': '/content/.../video_16_17.mp4', 'tensor_path': '...', 'violence_probability': 0.2442}
    Into sorted frontend format:
      {
        "overallProbability": <avg of all vio_prob * 100>,
        "timestamps": [
          {"time": "00:00:01", "probability": 24.4},
          {"time": "00:00:02, "probability": 24.4}
          {"time": "00:00:03", "probability": 24.4}
          ...
        ],
        "message": "Video analysis complete."
      }
    """
    def seconds_to_timestamp(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    timestamps = []
    for item in scene_data:
        filename = item["scene_path"].split("/")[-1]
        parts = filename.split("_")
        try:
            start_sec = int(parts[-2])  # extract start second (e.g. 481 in _481_482.mp4)
        except ValueError:
            continue

        timestamps.append({
            "time": seconds_to_timestamp(start_sec),
            "probability": round(item["violence_probability"] * 100, 1),
            "_seconds": start_sec  # temporary field for sorting
        })

    # Sort by the start time
    timestamps.sort(key=lambda x: x["_seconds"])

    # Remove temporary field
    for t in timestamps:
        del t["_seconds"]

    # Compute overall average
    overall = (
        sum(t["probability"] for t in timestamps) / len(timestamps)
        if timestamps else 0
    )

    result = {
        "overallProbability": round(overall, 1),
        "timestamps": timestamps,
        "message": "Video analysis complete."
    }

    return result