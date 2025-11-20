import os
import json
import time
import torch
import cv2
import numpy as np
import torch.nn.functional as F
from torchvision import transforms
from tqdm import tqdm


# =============================
# 🎥 Convert 1 scene -> tensor
# - Guaranteed output shape: (T, feature_dim) e.g. (T, 2048)
# - Uses seek to read exact frame indices; fallback if read fails
# =============================
def scene_to_tensor(scene_path, resnet50_model, T=1, device=None):
    device = "cuda"

    preprocess = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    cap = cv2.VideoCapture(scene_path)
    if not cap.isOpened():
        print(f"[WARN] Cannot open video: {scene_path}")
        return None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        cap.release()
        print(f"[WARN] Video has zero frames: {scene_path}")
        return None

    # compute indices (T indices uniformly spaced)
    indices = np.linspace(0, max(total_frames - 1, 0), T).astype(int)

    frames = []
    last_valid = None
    for idx in indices:
        # Seek to frame idx
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ret, frame = cap.read()
        if not ret or frame is None:
            # fallback: if we have a last valid frame, reuse it; else create black frame
            if last_valid is not None:
                frame = last_valid.copy()
            else:
                # create black RGB frame of reasonable size (use 224x224 after preprocess anyway)
                frame = np.zeros((224, 224, 3), dtype=np.uint8)
        else:
            last_valid = frame.copy()

        # convert and preprocess
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(preprocess(frame_rgb))

    cap.release()

    if len(frames) == 0:
        return None

    # Stack -> (T, 3, 224, 224)
    frames_tensor = torch.stack(frames).to(device)

    # Extract features from ResNet50 (assume resnet50_model returns [batch, 2048, 1, 1] or [batch, 2048])
    with torch.no_grad():
        feats = resnet50_model(frames_tensor)  # shape depends on model

    # Normalize/reshape features to (T, 2048)
    if feats.ndim == 4:
        # [T, 2048, 1, 1] -> (T, 2048)
        feats = feats.view(feats.size(0), -1)
    elif feats.ndim == 2:
        # [T, 2048] already
        pass
    else:
        # unexpected shape, try to flatten per time step
        feats = feats.view(feats.size(0), -1)

    # Ensure final shape is exactly (T, feature_dim)
    if feats.size(0) != T:
        # If something odd happened, pad/trim temporally to T
        if feats.size(0) < T:
            # pad by repeating last row
            last_row = feats[-1:].repeat(T - feats.size(0), 1)
            feats = torch.cat([feats, last_row], dim=0)
        else:
            feats = feats[:T]

    return feats.cpu()  # (T, D)


# =========================================
# 📁 Convert folder of scenes -> tensors (unchanged style)
# =========================================
def folder_to_tensor(folder_path, resnet50_model, T=1, device=None):
    device = "cuda"
    output_dir = f"{folder_path}_tensor"
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for filename in tqdm(os.listdir(folder_path)):
        if not filename.lower().endswith(".mp4"):
            continue

        scene_path = os.path.join(folder_path, filename)
        tensor = scene_to_tensor(scene_path, resnet50_model, T=T, device=device)
        if tensor is None:
            print(f"[WARN] Skipping (no tensor): {scene_path}")
            continue

        tensor_name = os.path.splitext(filename)[0] + ".pt"
        tensor_path = os.path.join(output_dir, tensor_name)
        torch.save(tensor, tensor_path)
        # Ensure data is flushed to disk
        with open(tensor_path, "wb") as f:
            torch.save(tensor, f)
            f.flush()
            os.fsync(f.fileno())

        results.append({
            "scene_path": scene_path,
            "tensor_path": tensor_path
        })

    json_path = os.path.join(output_dir, "mapping.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)

    return results