import torch
import torchvision.transforms as T
import cv2

def get_preprocess_transform():
    """
    Preprocessing pipeline for ResNet50:
        - BGR -> RGB
        - Resize to 224x224
        - Convert to Tensor
        - Normalize using ImageNet mean/std
    """
    return T.Compose([
        T.ToPILImage(),
        T.Resize((224, 224)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225])
    ])


def frames_to_vectors(lst_frames, resnet50_model, device='cuda', batch_size=None):
    """
    Convert a list of frames into feature vectors using a preloaded ResNet50.
    
    Args:
        lst_frames (list of np.ndarray): Video frames in BGR format.
        resnet50_model (nn.Module): Preloaded ResNet50 backbone (truncated)
        device (str or torch.device): 'cuda' or 'cpu'
        batch_size (int, optional): Split into mini-batches if GPU memory is limited.
        
    Returns:
        torch.Tensor: Feature vectors (N_frames, 2048)
    """
    if not lst_frames:
        return torch.empty(0, 2048, device=device)
    
    device = torch.device(device)
    resnet50_model.to(device).eval()
    
    preprocess = get_preprocess_transform()
    
    # Function to process a single batch
    def process_batch(frames):
        batch_tensor = torch.stack([
            preprocess(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)) for f in frames
        ]).to(device)
        
        with torch.no_grad():
            feats = resnet50_model(batch_tensor)
            feats = feats.view(feats.size(0), -1)
        return feats
    
    # Handle mini-batches if batch_size is specified
    if batch_size is None or batch_size >= len(lst_frames):
        return process_batch(lst_frames)
    
    all_feats = []
    for i in range(0, len(lst_frames), batch_size):
        batch = lst_frames[i:i+batch_size]
        all_feats.append(process_batch(batch))
    
    return torch.cat(all_feats, dim=0)