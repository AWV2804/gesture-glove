import torch
from torch.utils.data import DataLoader
from dataset import LogGestureDataset
from model import GestureCNN

# Configuration
BATCH_SIZE = 2
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

# Label map for display
LABELS = {0: "clap", 1: "jazz", 2: "pinch"}

# Load model
model = GestureCNN(pooled_steps=25)
model.load_state_dict(torch.load("gesture_model.pth", map_location=DEVICE))
model.to(DEVICE)
model.eval()

# Load test data (augmented runs)
test_dataset = LogGestureDataset(mode="augmented")
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

# Evaluation
correct = 0
total = 0

with torch.no_grad():
    for X, y in test_loader:
        X, y = X.to(DEVICE), y.to(DEVICE)
        outputs = model(X)
        _, predicted = torch.max(outputs, 1)
        total += y.size(0)
        correct += (predicted == y).sum().item()

        for true, pred in zip(y.cpu(), predicted.cpu()):
            truth_label = LABELS[int(true.item())]
            predicted_label = LABELS[int(pred.item())]
            result = "✅" if truth_label == predicted_label else "❌"
            print(f"True: {truth_label}, Pred: {predicted_label} {result}")

print(f"\nTest Accuracy on Augmented Runs: {100 * correct / total:.2f}%")
