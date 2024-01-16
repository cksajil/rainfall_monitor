import pandas as pd
from os import path
from gpiozero import Button
from datetime import datetime
from utils.helper import load_config

config = load_config("config.yaml")

rain_sensor = Button(6)
BUCKET_SIZE = 0.2794
count = 0
labels_df = pd.DataFrame(columns=["time", "rainfall"])


def bucket_tipped():
    global count
    count += 1


def reset_rainfall():
    global count
    count = 0


dt_start = datetime.now()

while True:
    rain_sensor.when_pressed = bucket_tipped
    dt_now = datetime.now()
    elapsed_time = dt_now - dt_start
    dt_start = dt_now
    if elapsed_time.seconds == 30:
        rainfall = count * BUCKET_SIZE
        labels_df = labels_df.append(
            {"time": dt_now, "rainfall": rainfall}, ignore_index=True
        )
        reset_rainfall()
        labels_df.to_csv(
            path.join(config["log_dir"], config["label_file"]), index=False
        )
    else:
        continue
