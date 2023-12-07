import logging
import subprocess
from os import path
from datetime import datetime, timedelta
from utils.helper import time_stamp_fnamer
from utils.estimate import estimate_rainfall
from utils.helper import load_config, create_folder, load_estimate_model


config = load_config("config.yaml")
create_folder(config["log_dir"])

logging.basicConfig(
    filename=path.join(config["log_dir"], config["log_filename"]),
    filemode="a+",
    format="%(message)s",
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

d = config["sample_duration_sec"]
file_format = config["file_format"]
resolution = config["resolution"]
sampling_rate = config["sampling_rate"]
record_hours = config["record_hours"]
num_samples = int(config["record_hours"] * (3600 / d))
infer_model_path = path.join(config["infer_model_dir"], config["infer_model_name"])
infer_model = load_estimate_model(infer_model_path)

dt_start = datetime.now()
dt_stop = dt_start + timedelta(hours=record_hours)

logger.info("\n\n\n*******************************************************")
logger.info("Started data logging at {}\n".format(dt_start))
logger.info("Total number of samples to be recorded: {}\n".format(num_samples))

for i in range(num_samples):
    dt_now = datetime.now()
    logger.info("Recording sample number {} on {}".format(i, dt_now))
    dt_fname = time_stamp_fnamer(dt_now) + ".wav"
    location = config["data_dir"] + dt_fname

    subprocess.call(
        [
            "arecord",
            "-q",
            "--duration=" + str(d),
            "-t",
            str(file_format),
            "-f",
            str(resolution),
            "-r",
            sampling_rate,
            location,
        ]
    )
    mm_hat = estimate_rainfall(infer_model, location)
    logger.info("At {} estimated {} \n".format(dt_now, mm_hat))
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
