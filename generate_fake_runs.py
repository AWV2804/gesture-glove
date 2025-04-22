import os
import random

GESTURES = ["clap", "pinch", "snap"]
NUM_RUNS = 10
NUM_SENSORS = 6
NUM_SAMPLES = 50
DT = 0.1

def simulate_sample_data(t):
    ax = round(random.uniform(-1, 1), 6)
    ay = round(random.uniform(-1, 1), 6)
    az = round(random.uniform(-1, 1), 6)
    gx = round(random.uniform(-0.5, 0.5), 6)
    gy = round(random.uniform(-0.5, 0.5), 6)
    gz = round(random.uniform(-0.5, 0.5), 6)
    return (ax, ay, az), (gx, gy, gz)

def create_run(run_idx):
    run_dir = f"Run {run_idx}"
    os.makedirs(run_dir, exist_ok=True)
    gesture = random.choice(GESTURES)
    with open(os.path.join(run_dir, "gesture.txt"), "w") as f:
        f.write(gesture)

    for sensor_id in range(NUM_SENSORS):
        sensor_file = os.path.join(run_dir, f"MySensor{sensor_id}.log")
        with open(sensor_file, "w") as f:
            for i in range(NUM_SAMPLES):
                t = round(i * DT, 1)
                accel, gyro = simulate_sample_data(t)
                f.write(f"{t:.1f} acceleration: {accel}\n")
                f.write(f"{t:.1f} gyro:         {gyro}\n")

if __name__ == "__main__":
    for run_id in range(1, NUM_RUNS + 1):
        create_run(run_id)
    print(f"Generated {NUM_RUNS} synthetic runs.")