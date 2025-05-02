import os
import torch
from torch.utils.data import Dataset
import numpy as np
from log_info import log_info

GESTURE_LABELS = {'clap': 0, 'pinch': 1, 'snap': 2}

class LogGestureDataset(Dataset):
    def __init__(self, base_dir="Runs"):
        """
        Initialize the dataset by loading all runs from the specified base directory.
        Defaults to the 'Runs/' folder.
        """
        self.samples = []
        self.base_dir = base_dir
        self._load_all_runs()

    def _load_all_runs(self):
        log_info(f"Loading data from: {self.base_dir}")
        for run_name in sorted(os.listdir(self.base_dir)):
            run_path = os.path.join(self.base_dir, run_name)
            if not os.path.isdir(run_path) or not run_name.startswith("Run "):
                continue
            label_path = os.path.join(run_path, "gesture.txt")
            if not os.path.exists(label_path):
                continue
            with open(label_path, "r") as f:
                gesture = f.read().strip().lower()
            if gesture not in GESTURE_LABELS:
                continue
            y = GESTURE_LABELS[gesture]

            log_info(f"Checking folder: {run_path}")
            log_info(f"Found label: {gesture}")

            sensor_data = []
            for i in range(6):
                log_path = os.path.join(run_path, f"MySensor{i}.log")
                if not os.path.exists(log_path):
                    continue
                sensor_data.append(self._parse_log_file(log_path))
            if len(sensor_data) == 6:
                X = np.concatenate(sensor_data, axis=0)  # shape: [6*6, T]
                self.samples.append((torch.tensor(X, dtype=torch.float32), y))

    def _parse_log_file(self, filepath):
        accel, gyro = [], []
        with open(filepath, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                acc_line = lines[i].split("acceleration:")[-1].strip()
                gyr_line = lines[i+1].split("gyro:")[-1].strip()
                ax, ay, az = eval(acc_line)
                gx, gy, gz = eval(gyr_line)
                accel.append([ax, ay, az])
                gyro.append([gx, gy, gz])
        features = np.hstack([accel, gyro])  # shape: [T, 6]
        return features.T  # shape: [6, T]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]