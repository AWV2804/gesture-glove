import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset import LogGestureDataset
from model import GestureCNN

# Configuration
BATCH_SIZE = 2
EPOCHS = 50
LEARNING_RATE = 0.0005
BASE_DIR = "."  # Root folder where Run X folders live
if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
# elif torch.backends.mps.is_available():
#     DEVICE = torch.device("mps")
else:
    DEVICE = torch.device("cpu")

print(f"Using device: {DEVICE}")

# Load dataset
train_dataset = LogGestureDataset(mode="real")
test_dataset = LogGestureDataset(mode="augmented")

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)


# Initialize model
model = GestureCNN(pooled_steps=25)
model.to(DEVICE)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Training loop
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for X, y in train_loader:
        X, y = X.to(DEVICE), y.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += y.size(0)
        correct += (predicted == y).sum().item()

    print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {running_loss:.4f} - Accuracy: {100 * correct / total:.2f}%")

# Save model
torch.save(model.state_dict(), "gesture_model.pth")
print("Model saved as gesture_model.pth")

# # Map index to gesture name
# LABELS = {0: "clap", 1: "jazz", 2: "pinch"}

# # Evaluate on augmented (test) dataset
# model.eval()
# correct = 0
# total = 0

# with torch.no_grad():
#     for X, y in test_loader:
#         X, y = X.to(DEVICE), y.to(DEVICE)
#         outputs = model(X)
#         _, predicted = torch.max(outputs, 1)
#         total += y.size(0)
#         correct += (predicted == y).sum().item()

#         for true, pred in zip(y.cpu(), predicted.cpu()):
#             truth_label = LABELS[int(true.item())]
#             predicted_label = LABELS[int(pred.item())]
#             result = "✅" if truth_label == predicted_label else "❌"
#             print(f"True: {truth_label}, Pred: {predicted_label} {result}")

# print(f"\nTest Accuracy on Augmented Runs: {100 * correct / total:.2f}%")