import subprocess
from os import path
from datetime import datetime, timedelta
from utils.helper import load_infer_model_path
from utils.helper import time_stamp_fnamer, influxdb
from utils.estimate import estimate_rainfall, delete_files
from utils.helper import load_config, create_folder, load_estimate_model
from utils.gpio import setup_rain_sensor_gpio, gpio_cleanup
from utils.gpio import enable_rain_sensor, read_rain_sensor, disable_rain_sensor

config = load_config("config.yaml")
db_counter = 0
rain = 0
DB_write_interval = config["DB_writing_interval_min"] / 3
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
# setup_rain_sensor_gpio()
# enable_rain_sensor()
for i in range(1, num_samples + 1):
    dt_now = datetime.now()
    print("Recording sample number {} on {}".format(i, dt_now))
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
        print(mm_hat)
        delete_files(locations)
        print("At {} model {} estimated {}".format(dt_now, model_type, mm_hat))
        locations.clear()
        # rain_sensor_status = read_rain_sensor()
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

            print("At {} API write status: {}".format(dt_now, str(api_status)))

            rain, db_counter = 0, 0
    time_left = dt_stop - dt_now
    days, seconds = time_left.days, time_left.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
dt_end = datetime.now()

# disable_rain_sensor()
# gpio_cleanup()
