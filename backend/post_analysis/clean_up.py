import shutil
from pathlib import Path

def delete_resource(video_path):
    video_path = Path(video_path)
    base_name = video_path.stem
    upload_dir = video_path.parent  # folder chứa video

    # 1️⃣ Xóa video gốc
    if video_path.exists():
        try:
            video_path.unlink()
            print(f"[INFO] Deleted video: {video_path}")
        except Exception as e:
            print(f"[ERROR] Could not delete video: {e}")

    # 2️⃣ Xóa folder scene/tensor liên quan (bên ngoài upload)
    parent_dir = upload_dir.parent  # folder chứa upload và các folder scene/tensor
    patterns = [
        f"*_{base_name}_folder",
        f"*_{base_name}_folder_tensor"
    ]
    for pattern in patterns:
        for folder in parent_dir.glob(pattern):
            if folder.is_dir():
                try:
                    shutil.rmtree(folder)
                    print(f"[INFO] Deleted folder: {folder}")
                except Exception as e:
                    print(f"[ERROR] Could not delete folder {folder}: {e}")

    print("[INFO] Cleanup complete.")