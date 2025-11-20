import time
import torch
import torch.nn as nn

def load_resnet50_model(device=None):
    """
    Load ResNet50 backbone for feature extraction (remove final FC).
    Returns a model that maps input (1, C, H, W) -> (1, 2048, 1, 1).
    """
    start_time = time.time()

    device = device or ("cuda" if torch.cuda.is_available() else "cpu")

    try:
        # Newer torchvision (preferred)
        from torchvision.models import resnet50, ResNet50_Weights
        weights = ResNet50_Weights.IMAGENET1K_V1
        backbone = resnet50(weights=weights)
    except Exception:
        # Fallback for older torchvision
        from torchvision import models
        backbone = models.resnet50(pretrained=True)

    # Remove the final fully-connected layer; keep avgpool
    backbone = nn.Sequential(*list(backbone.children())[:-1])

    backbone = backbone.to(device)
    backbone.eval()

    elapsed = time.time() - start_time
    print(f"[INFO] ResNet50 loaded on '{device}'")
    print(f"[TIME] Model load time: {elapsed:.2f} seconds")

    return backbone