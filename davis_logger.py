import RPi.GPIO as GPIO
from datetime import datetime
import pandas as pd
from os import path
from utils.helper import load_config

interrupt_pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

BUCKET_SIZE = 0.2
count = 0
log_count = 0
dt_start = datetime.now()
config = load_config("config.yaml")
labels_df = pd.DataFrame(columns=["time", "rainfall"])


def bucket_tipped(interrupt_pin):
    print("Bucket Tipped")
    global count
    count += 1


def reset_rainfall():
    global count
    count = 0


def saving_data():
    rainfall = count * BUCKET_SIZE
    labels_df.loc[len(labels_df)] = (dt_now, rainfall)
    labels_df.to_csv(path.join(config["log_dir"], config["label_file"]), index=False)


GPIO.add_event_detect(interrupt_pin, GPIO.RISING, callback=bucket_tipped, bouncetime=50)

try:
    while True:      
        dt_now = datetime.now()
        elapsed_time = dt_now - dt_start
        if elapsed_time.seconds % 10 == 0:  # for storing data in every 10s interval
            if log_count == 0:              # to avoid multiple data logging
                saving_data()
                reset_rainfall() 
                log_count = 1 
        else:
            log_count = 0 
except KeyboardInterrupt:
    GPIO.cleanup()
