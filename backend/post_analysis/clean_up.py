import shutil
from pathlib import Path

def delete_resource(video_path):
    """
    Delete resource folders generated from a given video.
    Specifically: {video_name}_folder and {video_name}_tensor

    Args:
        video_path (str or Path): Path to the original video file.
    """
    video_path = Path(video_path)
    base_name = video_path.stem  # e.g., "fight" from fight.mp4

    # Các thư mục cần xóa
    folders_to_delete = [
        Path(f"{base_name}_folder"),
        Path(f"{base_name}_folder_tensor")
    ]

    for folder in folders_to_delete:
        if folder.exists() and folder.is_dir():
            try:
                shutil.rmtree(folder)
                print(f"[INFO] Deleted folder: {folder}")
            except Exception as e:
                print(f"[ERROR] Could not delete {folder}: {e}")
        else:
            print(f"[WARN] Folder not found: {folder}")

    print("[INFO] Resource cleanup complete.")
