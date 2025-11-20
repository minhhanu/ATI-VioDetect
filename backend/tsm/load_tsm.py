from torch import device, nn
import torch
from tsm.tsm_class_definition import TSMFeatureModel

default_path = r"tsm\tsm_feature_epoch_12.pt"

def load_TSM(pt_path=default_path, feature_dim=2048, num_classes=2, n_segment=32):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Define device here
    model = TSMFeatureModel(
        feature_dim=feature_dim,
        num_classes=num_classes,
        n_segment=n_segment
    )
    model.load_state_dict(torch.load(pt_path, map_location=device))
    model.eval()
    return model.to(device)