# add the path into the system temporatory
import sys
sys.path.append(r"tsm\temporal-shift-module")
from torch import nn

# Defining architecture
from ops.temporal_shift import TemporalShift
from ops.models import TSN # Hai class trên sẽ import dc sau khi thêm tsm\temporal-shift-module vào hệ thống

# ... class TSM
class TSMFeatureModel(nn.Module):
    """
    Temporal Shift Module cho feature vector (2048-dim).
    Input: (batch_size, T, feature_dim)
    Output: logits cho 2 class (Violence / NonViolence)
    """
    def __init__(self, feature_dim=2048, num_classes=2, n_segment=32, shift_ratio=0.25):
        super(TSMFeatureModel, self).__init__()
        self.feature_dim = feature_dim
        self.num_classes = num_classes
        self.n_segment = n_segment
        self.shift_ratio = shift_ratio

        # Layer fc để map feature vector trước khi shift
        self.fc1 = nn.Linear(feature_dim, feature_dim)
        self.relu = nn.ReLU()

        # TSM + temporal conv (1D)
        self.temporal_conv = nn.Conv1d(
            in_channels=feature_dim,
            out_channels=feature_dim,
            kernel_size=3,
            padding=1,
            groups=1
        )

        self.fc_out = nn.Linear(feature_dim, num_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        """
        x: (batch_size, T, feature_dim)
        """
        # 1️⃣ FC + ReLU
        x = self.fc1(x)        # (B, T, F)
        x = self.relu(x)

        # 2️⃣ Temporal conv: cần (B, F, T) để conv1d theo trục temporal
        x = x.permute(0, 2, 1)  # (B, F, T)
        x = self.temporal_conv(x)
        x = x.permute(0, 2, 1)  # (B, T, F)

        # 3️⃣ Temporal pooling: mean over T frames
        x = x.mean(dim=1)       # (B, F)

        # 4️⃣ Output layer
        logits = self.fc_out(x)  # (B, num_classes)
        return logits