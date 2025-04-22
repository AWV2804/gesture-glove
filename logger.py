#!/usr/bin/env python3
import os
from typing import List, Tuple, Optional

def get_next_run_dir(base: str = './Runs') -> str:
    """
    Find the next “Run N” folder (N=max+1, or 1 if none), create it, and return its path.
    """
    # Ensure the base directory (Runs/) exists
    os.makedirs(base, exist_ok=True)

    existing = []
    for name in os.listdir(base):
        if name.startswith("Run "):
            try:
                n = int(name.split(" ", 1)[1])
                existing.append(n)
            except ValueError:
                pass
    nxt = max(existing) + 1 if existing else 1
    path = os.path.join(base, f"Run {nxt}")
    os.makedirs(path, exist_ok=False)
    return path

def write_sensor_log(
    sensor_id: int,
    accel_data: List[Tuple[float, float, float]],
    gyro_data:  List[Tuple[float, float, float]],
    output_prefix: str,
    run_dir: Optional[str] = None,
    dt: float = 0.1
) -> Tuple[str, str]:
    """
    Write one logfile for sensor `sensor_id` containing accel+gyro samples in this form:

      0.0 acceleration: (ax, ay, az)
      0.0 gyro:         (gx, gy, gz)
      0.1 acceleration: (…)
      0.1 gyro:         (…)
      …

    - accel_data & gyro_data must be the same length.
    - Lines alternate accel then gyro, each with the same timestamp.
    - Timestamp starts at 0.0 and increments by `dt` per pair.
    - Filename is `<output_prefix><sensor_id>.log` inside a `Run X` folder.

    Returns (run_dir, logfile_path).
    """
    if len(accel_data) != len(gyro_data):
        raise ValueError("accel_data and gyro_data must have the same length")

    # 1) Create or reuse the Run folder
    if run_dir is None:
        run_dir = get_next_run_dir()

    # 2) Open the logfile
    fname = f"{output_prefix}{sensor_id}.log"
    out_path = os.path.join(run_dir, fname)
    with open(out_path, 'w', encoding='utf-8') as out:
        for idx, (a, g) in enumerate(zip(accel_data, gyro_data)):
            timestamp = idx * dt
            # acceleration line
            out.write(
                f"{timestamp:.1f} acceleration: "
                f"({a[0]}, {a[1]}, {a[2]})\n"
            )
            # gyro line (aligned under "acceleration")
            out.write(
                f"{timestamp:.1f} gyro:         "
                f"({g[0]}, {g[1]}, {g[2]})\n"
            )

    return run_dir, out_path

# Example usage
if __name__ == "__main__":
    example_accel = [
        (-0.000482784, 0.000122703, 0.0003662109),
        (0.001708987, -0.001342773, 0.001098633),
        # …
    ]
    example_gyro = [
        (-0.03053403, -0.1145039, 0.08778628),
        (-0.0381672, 0.01526713, -0.03435111),
        # …
    ]

    run_folder, logfile = write_sensor_log(
        sensor_id=2,
        accel_data=example_accel,
        gyro_data=example_gyro,
        output_prefix="MySensor"
    )
    print(f"Wrote sensor 2 data to {logfile} (in {run_folder}/)")