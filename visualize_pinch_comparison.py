import os
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = "Runs"
TARGET_GESTURE = "pinch"
SENSOR_COUNT = 6

def parse_log(filepath):
    accel = []
    with open(filepath, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 2):
            acc_line = lines[i].split("acceleration:")[-1].strip()
            ax, ay, az = eval(acc_line)
            accel.append([ax, ay, az])
    return np.array(accel)

def find_gesture_runs(gesture, max_count=None, augmented=False):
    runs = []
    run_dirs = [d for d in os.listdir(BASE_DIR) if d.startswith("Run ") and os.path.isdir(os.path.join(BASE_DIR, d))]
    run_dirs_sorted = sorted(run_dirs, key=lambda x: int(x.split()[1]))

    for run_name in run_dirs_sorted:
        run_id = int(run_name.split(" ")[1])
        if augmented and run_id < 30:
            continue
        if not augmented and run_id >= 30:
            continue
        gesture_file = os.path.join(BASE_DIR, run_name, "gesture.txt")
        if os.path.exists(gesture_file):
            with open(gesture_file) as f:
                label = f.read().strip().lower()
            if label == gesture:
                runs.append(run_name)
                if max_count and len(runs) >= max_count:
                    break
    return runs

def plot_runs(runs, augmented=False):
    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    axes = axes.flatten()

    for idx, run_name in enumerate(runs):
        ax = axes[idx]
        for sensor_id in range(SENSOR_COUNT):
            file_path = os.path.join(BASE_DIR, run_name, f"MySensor{sensor_id}.log")
            acc_data = parse_log(file_path)
            z_acc = acc_data[:, 2]
            ax.plot(z_acc, label=f"Sensor {sensor_id}")
        ax.set_title(f"{'Augmented' if augmented else 'Original'} {run_name}")
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Z Acceleration")
        ax.legend(fontsize=6)

    plt.suptitle(f"{'Augmented' if augmented else 'Original'} Pinch Runs (Z-Accel from 6 Sensors)", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    real_pinch_runs = find_gesture_runs(TARGET_GESTURE, max_count=10, augmented=False)
    aug_pinch_runs = find_gesture_runs(TARGET_GESTURE, max_count=10, augmented=True)

    print("Showing original pinch runs...")
    plot_runs(real_pinch_runs, augmented=False)

    print("Showing augmented pinch runs...")
    plot_runs(aug_pinch_runs, augmented=True)