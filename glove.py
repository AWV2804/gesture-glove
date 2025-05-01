from imu import MPU6050
from machine import Pin, I2C
import time
from calibrate import run_calibration
from logger import write_sensor_log

#imu = MPU6050('X')
#print(imu.accel.xyz)
#print(imu.gyro.xyz)
#print(imu.temperature)
#print(imu.accel.z)



# Initialize I2C
i2c = I2C(0, scl=Pin(12), sda=Pin(27), freq=400000)

PCA_ADDR = 0x70
MPU_ADDR = 0x68

def select_channel(channel):
    if 0 <= channel <= 7:
        i2c.writeto(PCA_ADDR, bytes([1 << channel]))
        time.sleep_ms(10)

# Scan for MPU6050s
mpus = []
for ch in range(6):
    select_channel(ch)
    time.sleep_ms(50)
    if MPU_ADDR in i2c.scan():
        mpu = MPU6050('X')
        run_calibration(mpu)
        mpus.append((ch, mpu))
        print(f"MPU6050 found on channel {ch}")
    else:
        print(f"No MPU6050 found on channel {ch}")

# Read loop
while True:
    for ch, mpu in mpus:
        select_channel(ch)
        time.sleep_ms(10)
        acc = mpu.accel.xyz
        gyro = mpu.gyro.xyz
        print(f"CH{ch} | Acc: {acc} | Gyro: {gyro}")
        run_folder, logfile = write_sensor_log(
        sensor_id=ch,
        accel_data=acc,
        gyro_data=gyro,
        output_prefix="MySensor"
        )
    time.sleep(1)
