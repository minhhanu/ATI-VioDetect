import os
import json
import time
import torch
import cv2
import numpy as np
from torchvision import transforms
from tqdm import tqdm

def scene_to_tensor(scene_path, resnet50_model, T=1, device=None):
    """
    Convert 1 scene video → (T, feature_dim)
    """
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")

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

    indices = np.linspace(0, max(total_frames - 1, 0), T).astype(int)

    frames = []
    last_valid = None
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ret, frame = cap.read()
        if not ret or frame is None:
            frame = last_valid.copy() if last_valid is not None else np.zeros((224, 224, 3), np.uint8)
        else:
            last_valid = frame.copy()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(preprocess(frame_rgb))

    cap.release()

    if len(frames) == 0:
        return None

    frames_tensor = torch.stack(frames).to(device)

    with torch.no_grad():
        feats = resnet50_model(frames_tensor)

    feats = feats.reshape(feats.size(0), -1)

    # pad or trim to T
    if feats.size(0) < T:
        feats = torch.cat([feats, feats[-1:].repeat(T - feats.size(0), 1)], dim=0)
    elif feats.size(0) > T:
        feats = feats[:T]

    return feats.cpu()


def folder_to_tensor(folder_path, resnet50_model, T=1, device=None):
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")

    output_dir = f"{folder_path}_tensor"
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for filename in tqdm(os.listdir(folder_path)):
        if not filename.lower().endswith(".mp4"):
            continue

        scene_path = os.path.join(folder_path, filename)
        tensor = scene_to_tensor(scene_path, resnet50_model, T=T, device=device)
        if tensor is None:
            print(f"[WARN] Skipping: {scene_path}")
            continue

        tensor_name = os.path.splitext(filename)[0] + ".pt"
        tensor_path = os.path.join(output_dir, tensor_name)
        torch.save(tensor, tensor_path)

        results.append({
            "scene_path": scene_path,
            "tensor_path": tensor_path
        })

        # Optional: release GPU memory gradually
        if device == "cuda":
            torch.cuda.empty_cache()

    json_path = os.path.join(output_dir, "mapping.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"[INFO] Folder converted: {folder_path} → {output_dir}")
    return results
