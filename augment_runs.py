import os
import random
import shutil

AUGMENTATIONS_PER_RUN = 20
INPUT_RUNS = list(range(30))  # Original runs Run 0 to Run 29
BASE_DIR = "Runs"
SENSOR_COUNT = 6

def add_noise_to_line(line, std=0.02):
    prefix, rest = line.split(":", 1)
    values = eval(rest.strip())
    noisy = tuple(round(v + random.gauss(0, std), 6) for v in values)
    return "{}: {}\n".format(prefix, noisy)

def augment_run(original_run_id, output_run_id):
    src_dir = "{}/Run {}".format(BASE_DIR, original_run_id)
    dst_dir = "{}/Run {}".format(BASE_DIR, output_run_id)

    try:
        os.mkdir(dst_dir)
    except OSError:
        pass  # Directory already exists

    # Copy gesture.txt
    shutil.copy("{}/gesture.txt".format(src_dir), "{}/gesture.txt".format(dst_dir))

    # Process each sensor file
    for sensor_id in range(SENSOR_COUNT):
        src_file = "{}/MySensor{}.log".format(src_dir, sensor_id)
        dst_file = "{}/MySensor{}.log".format(dst_dir, sensor_id)

        with open(src_file, "r") as fin, open(dst_file, "w") as fout:
            lines = fin.readlines()
            for line in lines:
                fout.write(add_noise_to_line(line))

if __name__ == "__main__":
    existing = [int(d.split()[1]) for d in os.listdir(BASE_DIR) if d.startswith("Run ")]
    next_run_id = max(existing) + 1 if existing else 30

    for original_id in INPUT_RUNS:
        for _ in range(AUGMENTATIONS_PER_RUN):
            augment_run(original_id, next_run_id)
            next_run_id += 1

    print("Generated {} augmented runs in '{}'.".format(next_run_id - max(INPUT_RUNS) - 1, BASE_DIR))