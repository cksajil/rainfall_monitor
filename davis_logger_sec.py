import pandas as pd
from os import path
import RPi.GPIO as GPIO
from datetime import datetime
from utils.gpio import disable_rain_sensor, read_rain_sensor
from utils.helper import load_config, create_folder, time_stamp_fnamer
from utils.gpio import setup_rain_sensor_gpio, enable_rain_sensor, gpio_cleanup


dt_start = datetime.now()
config = load_config("config.yaml")
labels_df = pd.DataFrame(columns=["time", "rainfall"])
session_dir = time_stamp_fnamer(dt_start)
label_dir = path.join(config["log_dir"], session_dir)
create_folder(label_dir)

BUCKET_SIZE = 0.2
count = 0
log_count = 0
interrupt_pin = config["interrupt_pin"]


def bucket_tipped(interrupt_pin):
    print("Bucket Tipped")
    global count
    count += 1


def reset_rainfall():
    global count
    count = 0


def saving_data(label_dir, dt_now):
    rainfall = count * BUCKET_SIZE
    labels_df.loc[len(labels_df)] = (dt_now, rainfall)
    labels_df.to_csv(path.join(label_dir, config["label_file_sec"]), index=False)


GPIO.setmode(GPIO.BCM)
GPIO.setup(interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(interrupt_pin, GPIO.RISING, callback=bucket_tipped, bouncetime=50)

setup_rain_sensor_gpio()
enable_rain_sensor()

try:
    while True:
        dt_now = datetime.now()
        rain_sensor_status = read_rain_sensor()
        elapsed_time = dt_now - dt_start
        if (elapsed_time.seconds % 2 == 0) and rain_sensor_status == GPIO.LOW:
            if log_count == 0:
                saving_data(label_dir, dt_now)
                reset_rainfall()
                log_count = 1
        else:
            log_count = 0
except KeyboardInterrupt:
    disable_rain_sensor()
    gpio_cleanup()
