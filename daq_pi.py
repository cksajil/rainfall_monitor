import logging
import subprocess
from os import path
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
from utils.helper import load_infer_model_path
from utils.helper import time_stamp_fnamer, influxdb
from utils.estimate import estimate_rainfall, delete_files
from utils.helper import load_config, create_folder, load_estimate_model
from utils.gpio import setup_rain_sensor_gpio, gpio_cleanup
from utils.gpio import enable_rain_sensor, read_rain_sensor, disable_rain_senso

config = load_config("config.yaml")
create_folder(config["log_dir"])

logging.basicConfig(
    filename=path.join(config["log_dir"], config["log_filename"]),
    filemode="a+",
    format="%(message)s",
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

db_counter = 0
rain = 0
DB_write_interval = config["DB_writing_interval_min"] / 3
result_data = []
board = config["board"]
wav_duration = config["sample_duration_sec"]
davis_duration = config["davis_duration_sec"]
file_format = config["file_format"]
resolution = config["resolution"]
sampling_rate = config["sampling_rate"]
record_hours = config["record_hours"]
num_samples = int(config["record_hours"] * (3600 / wav_duration))
num_subsamples = davis_duration // wav_duration
infer_model_path = load_infer_model_path(board)
interpreter = load_estimate_model(infer_model_path)
locations = []
dt_start = datetime.now()
dt_stop = dt_start + timedelta(hours=record_hours)

logger.info("\n\n\n*******************************************************")
logger.info("Started data logging at {}\n".format(dt_start))
logger.info("Total number of samples to be recorded: {}\n".format(num_samples))

# setup_rain_sensor_gpio()
# enable_rain_sensor()

for i in range(1, num_samples + 1):
    dt_now = datetime.now()
    print("Recording sample number {} on {}".format(i, dt_now))
    logger.info("Recording sample number {} on {}".format(i, dt_now))
    dt_fname = time_stamp_fnamer(dt_now) + ".wav"
    location = config["data_dir"] + dt_fname

    subprocess.call(
        [
            "arecord",
            "-q",
            "--duration=" + str(wav_duration),
            "-t",
            str(file_format),
            "-f",
            str(resolution),
            "-r",
            sampling_rate,
            location,
        ]
    )
    print("Recording finished")
    locations.append(location)
    model_type = config["deployed_model_type"]

    if i % num_subsamples == 0:
        mm_hat = estimate_rainfall(interpreter, locations)
        delete_files(locations)
        logger.info("\n\n\n*******************************************************")
        logger.info("At {} model {} estimated {}".format(dt_now, model_type, mm_hat))
        logger.info("*******************************************************\n\n\n")
        locations.clear()
        rain_sensor_status = read_rain_sensor()
        result_data.append(
            {
                "time_stamp": dt_now,
                "rainfall_estimate": mm_hat,
                "rain_sensor_status": rain_sensor_status,
            }
        )
        logger.info(
            "saved recorded data and rainfall estimate to: {}".format(
                config["csv_file_name"]
            )
        )
        # Script for controlling influxdb data writing interval
        rain += mm_hat
        db_counter += 1
        if db_counter == DB_write_interval:  # now sending data in every 3min interval
            # rain_sensor_status = read_rain_sensor()
            rain_sensor_status = 0
            if (
                rain_sensor_status == 0 and rain >= 0.6
            ):  # chance of error when we change data sending interval
                # api_status = influxdb(mm_hat)
                print(mm_hat)
            else:
                # api_status = influxdb(0.0)
                print(0)
            # logger.info("\n\n\n*******************************************************")
            # logger.info("At {} API write status: {}".format(dt_now, str(api_status)))
            # logger.info("*******************************************************\n\n\n")
            rain, db_counter = 0, 0

    time_left = dt_stop - dt_now
    days, seconds = time_left.days, time_left.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    logger.info(
        "Time left {} hours {} minutes and {} seconds\n".format(hours, minutes, seconds)
    )

dt_end = datetime.now()
logger.info("Finished data logging at {}\n".format(dt_end))
logger.info("*******************************************************\n\n\n")
# disable_rain_sensor()
# gpio_cleanup()
