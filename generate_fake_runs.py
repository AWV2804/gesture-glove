import os
import random
import math

GESTURES = ["clap", "pinch", "snap"]
NUM_RUNS = 600  # Set a default value for NUM_RUNS
NUM_SENSORS = 6
NUM_SAMPLES = 100
DT = 0.01  # Smaller time step for quick motions

def add_noise(vec, std=0.05):
    return tuple(x + random.gauss(0, std) for x in vec)

def simulate_sample_data(t, gesture, sensor_id):
    if gesture == "clap":
        impact = 1.5 if 0.4 < t < 0.5 else random.gauss(0, 0.05)
        accel = (impact, 0, 0)
        gyro = (0, 0, 0)

    elif gesture == "pinch":
        base = -0.8 + t if sensor_id in [1, 2] else 0
        accel = (0, 0, base)
        gyro = (0, 0, 0)

    elif gesture == "snap":
        freq = 25
        flick = 1.0 * math.sin(2 * math.pi * freq * t) if sensor_id in [1, 3] else 0.0
        accel = (0, 0, 0)
        gyro = (flick, 0, 0)

    else:
        accel = (0, 0, 0)
        gyro = (0, 0, 0)

    # Apply Gaussian noise to both
    return add_noise(accel), add_noise(gyro)

def create_run(run_idx, gesture):
    # Ensure the Runs/ directory exists
    base_dir = "Runs"
    os.makedirs(base_dir, exist_ok=True)

    # Create the specific Run directory inside Runs/
    run_dir = os.path.join(base_dir, f"Run {run_idx}")
    os.makedirs(run_dir, exist_ok=True)

    # Write the gesture file
    # gesture = random.choice(GESTURES)
    with open(os.path.join(run_dir, "gesture.txt"), "w") as f:
        f.write(gesture)

    # Write sensor data files
    for sensor_id in range(NUM_SENSORS):
        sensor_file = os.path.join(run_dir, f"MySensor{sensor_id}.log")
        with open(sensor_file, "w") as f:
            for i in range(NUM_SAMPLES):
                t = i * DT
                accel, gyro = simulate_sample_data(t, gesture, sensor_id)
                f.write(f"acceleration: {accel}\n")
                f.write(f"gyro:         {gyro}\n")

if __name__ == "__main__":
    for run_id in range(1, NUM_RUNS + 1):
        if run_id <= 200:
            gesture = "clap"
        elif run_id <= 400:
            gesture = "pinch"
        else:
            gesture = "snap"
        create_run(run_id, gesture)

    print(f"Generated {NUM_RUNS} synthetic runs in the 'Runs/' directory.")