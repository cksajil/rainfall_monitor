import logging
import subprocess
import pandas as pd
from os import path
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
from utils.estimate import estimate_rainfall
from utils.connectivity import send_data_via_internet, send_data_via_lorawan

# from plugins.rain_sensor import read_loop, disable_rain_sensor

from utils.helper import (
    time_stamp_fnamer,
    load_config,
    create_folder,
    delete_files,
    load_estimate_model,
)


def record_audio(file_path, duration, file_format, resolution, sampling_rate):
    subprocess.call(
        [
            "arecord",
            "-q",
            "--duration=" + str(duration),
            "-t",
            str(file_format),
            "-f",
            str(resolution),
            "-r",
            sampling_rate,
            file_path,
        ]
    )


def initialize_logging(log_dir, log_filename, start_time, total_samples):
    create_folder(log_dir)
    logging.basicConfig(
        filename=path.join(log_dir, log_filename),
        filemode="a+",
        format="%(message)s",
    )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info("*******************************************************")
    logger.info(f"Started data logging at {start_time}\n")
    logger.info(f"Total number of samples to be recorded: {total_samples}\n")
    return logger


def log_time_remaining(logger, end_time):
    time_left = end_time - datetime.now()
    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    log_message = f"Time left: {days} days {hours} hours {minutes} minutes and {seconds} seconds\n"
    logger.info(log_message)


def write_rain_data_to_csv(result_data, log_dir, csv_filename):
    result_df = pd.DataFrame(result_data)
    result_df.to_csv(path.join(log_dir, csv_filename), index=False)


def send_data(config, mm_hat):
    if config["communication"] == "LORAWAN":
        send_data_via_lorawan(mm_hat)
    else:
        send_data_via_internet(mm_hat)


def main():
    config = load_config("config.yaml")
    db_counter, rain = 0, 0
    DB_write_interval = config["DB_writing_interval_min"]
    result_data = []
    wav_duration = config["sample_duration_sec"]
    infer_inetrval = config["infer_inetrval_sec"]
    num_subsamples = infer_inetrval // wav_duration
    record_hours = config["record_hours"]
    field_deployed = config["field_deployed"]
    end_time = datetime.now() + timedelta(hours=record_hours)
    min_threshold = config["min_threshold"]
    infer_model_path = path.join(
        config["infer_model_dir"],
        (
            config["infer_model_withcnn"]
            if config["deployed_model_type"] == "withcnn"
            else config["infer_model_withoutcnn"]
        ),
    )

    infer_model = load_estimate_model(infer_model_path)
    locations = []

    try:
        if field_deployed:
            i = 1
            while True:
                dt_now = datetime.now()
                print(f"Recording sample number {i} on {dt_now}")
                dt_fname = time_stamp_fnamer(dt_now) + ".wav"
                location = path.join(config["data_dir"], dt_fname)
                record_audio(
                    location,
                    wav_duration,
                    config["file_format"],
                    config["resolution"],
                    config["sampling_rate"],
                )
                locations.append(location)

                if i % num_subsamples == 0:
                    mm_hat = estimate_rainfall(infer_model, locations)
                    print(f"Estimated rainfall: ", mm_hat)
                    delete_files(locations)
                    locations.clear()
                    # rain_sensor_status = read_loop()
                    rain_sensor_status = 0
                    rain += mm_hat
                    db_counter += 1

                    if db_counter == DB_write_interval:
                        if rain_sensor_status == GPIO.LOW and rain >= min_threshold:
                            send_data(config, mm_hat)
                        else:
                            send_data(config, 0.0)
                        rain, db_counter = 0, 0
                i += 1

        else:
            logger = initialize_logging(
                config["log_dir"],
                config["log_filename"],
                datetime.now(),
                int(record_hours * (3600 / wav_duration)),
            )
            for i in range(1, int(record_hours * (3600 / wav_duration)) + 1):
                dt_now = datetime.now()
                logger.info(f"Recording sample number {i} on {dt_now}")
                dt_fname = time_stamp_fnamer(dt_now) + ".wav"
                location = path.join(config["data_dir"], dt_fname)
                record_audio(
                    location,
                    wav_duration,
                    config["file_format"],
                    config["resolution"],
                    config["sampling_rate"],
                )
                locations.append(location)

                if i % num_subsamples == 0:
                    mm_hat = estimate_rainfall(infer_model, locations)
                    # logger.info(f"Estimated rainfall: ", mm_hat)
                    locations.clear()
                    # rain_sensor_status = read_loop()
                    rain_sensor_status = 0
                    result_data.append(
                        {
                            "time_stamp": dt_now,
                            "rainfall_estimate": mm_hat,
                            "rain_sensor_status": rain_sensor_status,
                        }
                    )
                    write_rain_data_to_csv(
                        result_data, config["log_dir"], config["csv_file_name"]
                    )
                    rain += mm_hat
                    db_counter += 1

                    if db_counter == DB_write_interval:
                        if rain_sensor_status == GPIO.LOW and rain >= min_threshold:
                            send_data(config, mm_hat)

                        else:
                            send_data(config, 0.0)
                        rain, db_counter = 0, 0
                log_time_remaining(logger, end_time)
            logger.info(f"Finished data logging at {datetime.now()}\n")

    except KeyboardInterrupt:
        print(f"Execution interrupted by user")
    finally:
        pass
        # disable_rain_sensor()
        # gpio_cleanup()


if __name__ == "__main__":
    main()
