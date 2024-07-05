import subprocess
from os import path
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
            sampling_rate,
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
    davis_duration = config["davis_duration_sec"]
    num_subsamples = davis_duration // wav_duration
    field_deployed = config["field_deployed"]
    infer_model = load_estimate_model(infer_model_path)
    # setup_rain_sensor_gpio()
    # enable_rain_sensor()
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
                    delete_files(locations)
                    locations.clear()
                    # rain_sensor_status = read_rain_sensor()
                    rain_sensor_status = 0
                    rain += mm_hat
                    db_counter += 1

                    if db_counter == DB_write_interval:
                        if rain_sensor_status == 0 and rain >= 0.6:
                            influxdb(mm_hat)
                        else:
                            influxdb(0.0)
                        rain, db_counter = 0, 0
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
