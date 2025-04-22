import torch.nn as nn

class GestureCNN(nn.Module):
    def __init__(self, input_channels=36, pooled_steps=25, num_classes=3):
        super(GestureCNN, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=input_channels, out_channels=64, kernel_size=5, padding=2)
        self.relu = nn.ReLU()
        self.pool = nn.AdaptiveAvgPool1d(pooled_steps)  # <- Fixed output size
        self.conv2 = nn.Conv1d(64, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * pooled_steps, 128)
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(128, num_classes)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))  # (B, 64, pooled_steps)
        x = self.relu(self.conv2(x))             # (B, 128, pooled_steps)
        x = x.view(x.size(0), -1)                # Flatten
        x = self.dropout(self.relu(self.fc1(x)))
        return self.fc2(x)