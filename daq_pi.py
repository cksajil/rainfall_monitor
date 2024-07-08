import subprocess
from os import path
import RPi.GPIO as GPIO
from datetime import datetime
from utils.estimate import estimate_rainfall
from utils.helper import (
    time_stamp_fnamer,
    influxdb,
    load_config,
    delete_files,
    load_estimate_model,
    load_infer_model_path,
)
from utils.gpio import (
    setup_rain_sensor_gpio,
    gpio_cleanup,
    enable_rain_sensor,
    read_rain_sensor,
    disable_rain_sensor,
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
            str(sampling_rate),
            file_path,
        ]
    )


def main():
    config = load_config("config.yaml")
    board = config["board"]
    infer_model_path = load_infer_model_path(board)
    db_counter, rain = 0, 0
    DB_write_interval = config["DB_writing_interval_min"]
    wav_duration = config["sample_duration_sec"]
    field_deployed = config["field_deployed"]
    infer_model = load_estimate_model(infer_model_path)
    # setup_rain_sensor_gpio()
    # enable_rain_sensor()
    try:
        if field_deployed:
            i = 1
            while True:
                dt_now = datetime.now()
                print(f"Recording sample number {i} on {dt_now}")
                # rain_sensor = read_rain_sensor()
                rain_sensor = 0
                dt_fname = time_stamp_fnamer(dt_now) + ".wav"
                location = path.join(config["data_dir"], dt_fname)
                record_audio(
                    location,
                    wav_duration,
                    config["file_format"],
                    config["resolution"],
                    config["sampling_rate"],
                )

                mm_hat = estimate_rainfall(infer_model, [location])
                delete_files([location])
                dt_now = datetime.now()
                print(f"At {dt_now} estimated {mm_hat}")

                if rain_sensor == GPIO.LOW and rain >= 0.6:
                    db_write_status = influxdb(mm_hat)
                else:
                    db_write_status = influxdb(0.0)
                print(f"At {dt_now} DB write status {db_write_status}")

                rain, db_counter = 0, 0  # Reset counters
                i += 1

    except KeyboardInterrupt:
        # disable_rain_sensor()
        # gpio_cleanup()
        print("Execution interrupted by user")
    finally:
        pass
        # disable_rain_sensor()
        # gpio_cleanup()


if __name__ == "__main__":
    main()
