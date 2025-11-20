import os
import json
import time
import torch
import cv2
import numpy as np
import torch.nn.functional as F
from torchvision import transforms
from tqdm import tqdm

# =========================================
# ⚡ Faster predict_folder with temporal interpolation support
# - expected_T: the temporal length T that TSM expects (e.g. n_segmentation)
# - if a loaded tensor has different temporal length, we interpolate temporally
# =========================================
def predict_folder(json_tensor_list, tsm_model, expected_T=32, device=None, batch_size=16):
    device = "cuda"
    tsm_model = tsm_model.to(device).eval()
    results = []

    print("[INFO] 🚀 Fast predict_folder() started...")

    # --- Preload all valid tensors ---
    valid_items = []
    for obj in json_tensor_list:
        tensor_path = os.path.abspath(obj["tensor_path"])
        if not os.path.exists(tensor_path):
            print(f"[WARN] Missing tensor file: {tensor_path}")
            continue
        valid_items.append(obj)

    all_tensors = []
    for obj in valid_items:
        tensor = torch.load(obj["tensor_path"], map_location="cpu")  # load on cpu first
        # Accept shape (T, D) or (1, T, D) or (T, D, 1, 1)
        # Normalize to (T, D)
        if tensor.ndim == 4:
            tensor = tensor.view(tensor.size(0), -1)
        elif tensor.ndim == 3 and tensor.size(0) == 1:
            # maybe saved as [1, T, D], convert to (T, D)
            tensor = tensor.squeeze(0)
        elif tensor.ndim == 2:
            pass
        else:
            print(f"[WARN] Unexpected tensor shape {tensor.shape} for {obj['tensor_path']} — attempting to reshape")
            try:
                tensor = tensor.view(tensor.size(0), -1)
            except Exception as e:
                print(f"[ERROR] Cannot reshape tensor {obj['tensor_path']}: {e}")
                continue

        T_loaded, D = tensor.shape

        # If temporal length differs from expected_T, interpolate along time
        if T_loaded != expected_T:
            # Convert to [1, D, T] for interpolate, use linear mode
            t = tensor.transpose(0, 1).unsqueeze(0)  # [1, D, T_loaded]
            t = F.interpolate(t, size=expected_T, mode='linear', align_corners=False)  # [1, D, expected_T]
            tensor = t.squeeze(0).transpose(0, 1)  # [expected_T, D]

        # Finally ensure shape (T_expected, D)
        if tensor.size(0) != expected_T:
            print(f"[WARN] After interpolation still wrong T for {obj['tensor_path']}, got {tensor.shape}")
            continue

        all_tensors.append(tensor.unsqueeze(0))  # [1, T, D]

    if not all_tensors:
        print("[ERROR] No valid tensors found.")
        return []

    # concat -> [N, T, D]
    all_tensors = torch.cat(all_tensors, dim=0).to(device)
    print(f"[INFO] Loaded {len(valid_items)} tensors → shape {tuple(all_tensors.shape)} (expected_T={expected_T})")

    # --- Run in batches ---
    num_samples = all_tensors.shape[0]
    start_time = time.time()

    all_probs = []
    with torch.no_grad():
        for i in range(0, num_samples, batch_size):
            batch = all_tensors[i:i + batch_size].to(device)  # [B, T, D]
            preds = torch.softmax(tsm_model(batch), dim=1)
            probs = preds[:, 1].cpu().numpy().tolist()
            all_probs.extend(probs)

    elapsed = time.time() - start_time
    print(f"[TIME] Inference finished in {elapsed:.2f}s (batch_size={batch_size})")

    # --- Collect results ---
    for obj, prob in zip(valid_items, all_probs):
        results.append({
            "scene_path": obj["scene_path"],
            "tensor_path": obj["tensor_path"],
            "violence_probability": float(prob)
        })

    print(f"[INFO] ✅ Done — {len(results)} predictions completed.")
    return results