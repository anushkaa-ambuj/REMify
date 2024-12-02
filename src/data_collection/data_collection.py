from machine import SoftI2C, I2C, Pin
from time import sleep
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
from imu import MPU6050
import utime 
import os  

# Function to initialize the MAX30102 sensor
def initialize_max30102():
    i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=400000)
    sensor = MAX30102(i2c=i2c)

    if sensor.i2c_address not in i2c.scan():
        print("MAX30102 Sensor not found.")
        return None
    elif not sensor.check_part_id():
        print("I2C device ID not corresponding to MAX30102 or MAX30105.")
        return None

    sensor.setup_sensor()
    sensor.set_sample_rate(400)
    sensor.set_fifo_average(8)
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
    return sensor

# Function to initialize the MPU6050 sensor
def initialize_mpu6050():
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
    return MPU6050(i2c)

# Function to get the formatted timestamp
def get_formatted_timestamp():
    # Get the current date and time
    current_time = utime.localtime()
    # Format: YYYY-MM-DD hh:MM:ss
    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        current_time[0], current_time[1], current_time[2],
        current_time[3], current_time[4], current_time[5]
    )

# Main function to gather data and save to CSV every minute
def main():
    sensor_max30102 = initialize_max30102()
    sensor_mpu6050 = initialize_mpu6050()

    if not sensor_max30102:
        print("MAX30102 sensor failed to initialize.")
        return
    if not sensor_mpu6050:
        print("MPU6050 sensor failed to initialize.")
        return

    file_path = 'sensor_data_new.csv'

    # Open the CSV file for appending
    with open(file_path, mode='a') as file:
        # Check if the file exists and is empty, then write the header if necessary
        try:
            # Attempt to get file size using os.stat
            if os.stat(file_path)[6] == 0:
                file.write("Timestamp,RED,IR,Ax,Ay,Az,Gx,Gy,Gz,Temperature\n")
        except OSError:
            # File doesn't exist, write header
            file.write("Timestamp,RED,IR,Ax,Ay,Az,Gx,Gy,Gz,Temperature\n")

        last_write_time = utime.time()  # Record the last write time

        while True:
            sensor_max30102.check()
            if sensor_max30102.available():
                # Read data from MAX30102
                red_reading = sensor_max30102.pop_red_from_storage()
                ir_reading = sensor_max30102.pop_ir_from_storage()

                # Read data from MPU6050
                ax = round(sensor_mpu6050.accel.x, 2)
                ay = round(sensor_mpu6050.accel.y, 2)
                az = round(sensor_mpu6050.accel.z, 2)
                gx = round(sensor_mpu6050.gyro.x)
                gy = round(sensor_mpu6050.gyro.y)
                gz = round(sensor_mpu6050.gyro.z)
                temperature = round(sensor_mpu6050.temperature, 2)

                # Get formatted timestamp
                timestamp = get_formatted_timestamp()

                # Check if half minute has passed since the last write
                current_time = utime.time()
                if current_time - last_write_time >= 30:
                    # Write data to CSV
                    file.write(f"{timestamp},{red_reading},{ir_reading},{ax},{ay},{az},{gx},{gy},{gz},{temperature}\n")
                    file.flush()  # Ensure data is written to the file immediately
                    last_write_time = current_time  # Update last write time

                    # Print data to console for monitoring
                    print(f"Data saved at {timestamp}")
                    print(f"Timestamp: {timestamp} | RED: {red_reading} | IR: {ir_reading} | Ax: {ax} | Ay: {ay} | Az: {az} | Gx: {gx} | Gy: {gy} | Gz: {gz} | Temperature: {temperature}", end="\r")

                # Adjust data collection interval as needed
                sleep(0.2)

if __name__ == '__main__':
    main()
