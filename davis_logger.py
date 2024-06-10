import pandas as pd
from os import path
import RPi.GPIO as GPIO
from datetime import datetime
from utils.helper import load_config, create_folder, time_stamp_fnamer
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from requests.exceptions import ConnectionError


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
logging_interval = config["davis_log_interval_sec"]


def bucket_tipped():
    print("Bucket Tipped")
    global count
    count += 1


def reset_rainfall():
    global count
    count = 0


def influxdb(rain: float):
    """
    Function to write data to InfluxDB.
    """
    try:
        influxdb_config = load_config("influxdb_api.yaml")
        org = influxdb_config["org"]
        url = influxdb_config["url"]
        bucket = influxdb_config["davis_bucket"]
        token = influxdb_config["davis_token"]

        client = influxdb_client.InfluxDBClient(
            url=url, token=token, org=org, timeout=30_000
        )
        write_api = client.write_api(write_options=SYNCHRONOUS)
        p = (
            influxdb_client.Point("pi_davis_raingauge")
            .tag("location", "greenfield tvm")
            .field("rain", rain)
        )
        write_api.write(bucket=bucket, org=org, record=p)
        client.close()
        return True
    except ConnectionError as e:
        print(f"Connection to InfluxDB failed: {e}")
        return False


def saving_data(label_dir, dt_now):
    rainfall = count * BUCKET_SIZE
    influxdb(rainfall)
    labels_df.loc[len(labels_df)] = (dt_now, rainfall)
    labels_df.to_csv(path.join(label_dir, config["label_file"]), index=False)


GPIO.setmode(GPIO.BCM)
GPIO.setup(interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(
    interrupt_pin, GPIO.RISING, callback=bucket_tipped, bouncetime=300
)

try:
    while True:
        dt_now = datetime.now()
        elapsed_time = dt_now - dt_start
        if elapsed_time.seconds % logging_interval == 0:
            if log_count == 0:
                saving_data(label_dir, dt_now)
                reset_rainfall()
                log_count = 1
        else:
            log_count = 0

except KeyboardInterrupt:
    print("Exiting program")

finally:
    GPIO.cleanup()
