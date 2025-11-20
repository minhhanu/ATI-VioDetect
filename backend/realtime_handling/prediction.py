from tsm.load_tsm import load_TSM
import torch
import torch.nn.functional as F
import cv2
from datetime import datetime, timedelta, timezone
from .frame_to_vector import frames_to_vectors
from resnet50.load_resnet50 import load_resnet50_model


# Global counter for prediction IDs
global_counter = 0
def predict_realtime(tsm_model, feature_stack, device='cuda'):
    """
    Run TSM model on feature stack and return structured dictionary with probabilities
    for each camera.
    
    Args:
        tsm_model (torch.nn.Module): Initialized TSM model
        feature_stack (torch.Tensor): Tensor of shape (num_cameras, feature_dim)
        device (str): 'cuda' or 'cpu'
        
    Returns:
        dict: Dictionary in JSON format with per-camera probabilities
    """
    global global_counter
    global_counter += 1

    vn_time = datetime.now(timezone(timedelta(hours=7)))

    # Move features to device
    feature_stack = feature_stack.to(device)


    # Ensure model is in eval mode
    tsm_model.eval()
    
    with torch.no_grad():
        # Forward pass through TSM

        # Each camera is treated independently, so we don't add extra batch dim
        if feature_stack.dim() == 2:  # (num_cameras, feature_dim)
            feature_stack = feature_stack.unsqueeze(1)  

        outputs = tsm_model(feature_stack)  # (num_cameras, num_classes) or (num_cameras, 1)

        # Convert logits to probabilities
        if outputs.shape[-1] == 1:
            probs = torch.sigmoid(outputs).squeeze() * 100  # probability in percentage
        else:
            probs = torch.softmax(outputs, dim=-1)[:, 1] * 100  # take class 1 prob

        # Convert to integer list
        probs = probs.cpu().int().tolist()

    # Build list of cameras
    cameras_list = [
        {"cameraId": i + 1, "probability": probs[i]}
        for i in range(len(probs))
    ]

    # Build result dictionary
    result = {
        "id": global_counter,
        "timestamp": vn_time.replace(microsecond=0).isoformat(),
        "cameras": cameras_list
    }

    return result