#!/usr/bin/env python3
import os
import time

def get_runs_base_dir(base='./Runs'):
    """
    Ensure the base 'Runs' directory exists, and return its path.
    """
    try:
        os.mkdir(base)
    except OSError:
        pass  # Directory already exists
    return base

def write_sensor_log(sensor_id, accel_data, gyro_data, output_prefix, base_dir='./Runs'):
    """
    Append to a logfile for the given sensor_id, storing accel+gyro data.

    File format:
      acceleration: (ax, ay, az)
      gyro:         (gx, gy, gz)
      ...
    """
    if len(accel_data) != len(gyro_data):
        raise ValueError("accel_data and gyro_data must have the same length")

    run_dir = get_runs_base_dir(base_dir)
    fname = output_prefix + str(sensor_id) + ".log"
    out_path = run_dir + "/" + fname

    with open(out_path, 'a') as out:
        out.write("acceleration: ({}, {}, {})\n".format(accel_data[0], accel_data[1], accel_data[2]))
        out.write("gyro:         ({}, {}, {})\n".format(gyro_data[0], gyro_data[1], gyro_data[2]))

    return run_dir, out_path

# Example usage
if __name__ == "__main__":
    example_accel = (-0.00048, 0.00012, 0.00036)

    example_gyro = (-0.0305, -0.1145, 0.0877)
    
    run_folder, logfile = write_sensor_log(
        sensor_id=2,
        accel_data=example_accel,
        gyro_data=example_gyro,
        output_prefix="MySensor"
    )
    time.sleep_ms(100)
    example_accel1 = (-0.00111, 0.00111, 0.00111)

    example_gyro1 = (-0.0111, -0.0111, 0.0111)
    time.sleep_ms(100)
    run_folder, logfile = write_sensor_log(
        sensor_id=2,
        accel_data=example_accel1,
        gyro_data=example_gyro1,
        output_prefix="MySensor"
    )
    
    print(f"Wrote sensor 2 data to {logfile} (in {run_folder}/)")
