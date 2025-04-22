# tests/test_dataset.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib.pyplot as plt
from dataset import LogGestureDataset
from torch.utils.data import DataLoader

def main():
    # Adjust path if your Run folders are somewhere else
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    print("Base directory (absolute):", basedir)
    dataset = LogGestureDataset()
    print(f"Total samples: {len(dataset)}")

    loader = DataLoader(dataset, batch_size=2, shuffle=True)
    print(loader.batch_size)
    for X, y in loader:
        print("X shape:", X.shape)  # (batch_size, 36, T)
        print("y labels:", y)

        # Visualize the first sample in the batch
        sample = X[0].numpy()       # shape: [36, T]
        label = y[0].item()

        fig, axs = plt.subplots(6, 6, figsize=(15, 10))
        fig.suptitle(f"Gesture Label: {label} ({list(dataset.samples)[label][1]})")

        for i in range(36):
            row = i // 6
            col = i % 6
            axs[row][col].plot(sample[i])
            axs[row][col].set_title(f"S{i//6} {'ax ay az gx gy gz'.split()[i%6]}")
            axs[row][col].set_xticks([])
            axs[row][col].set_yticks([])

        plt.tight_layout()
        plt.show()
        break  # Stop after first batch is visualized

if __name__ == "__main__":
    main()