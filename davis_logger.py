import pandas as pd
from os import path
from gpiozero import Button
from datetime import datetime
from utils.helper import load_config


config = load_config("config.yaml")
rain_sensor = Button(6)
BUCKET_SIZE = 0.2
count = 0
labels_df = pd.DataFrame(columns=["time", "rainfall"])
dt_start = datetime.now()


def bucket_tipped():
    print("Bucket Tipped")
    global count
    count += 1


def reset_rainfall():
    global count
    count = 0


while True:
    rain_sensor.when_pressed = bucket_tipped
    dt_now = datetime.now()
    elapsed_time = dt_now - dt_start

    if elapsed_time.seconds % 10 == 0:
        rainfall = count * BUCKET_SIZE
        labels_df.loc[len(labels_df)] = (dt_now, rainfall)
        reset_rainfall()
        labels_df.to_csv(
            path.join(config["log_dir"], config["label_file"]), index=False
        )
    else:
        continue
