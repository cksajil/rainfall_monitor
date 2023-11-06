import subprocess
from os import path
from datetime import datetime, timedelta
from utils.helper import time_stamp_fnamer
from utils.helper import load_config


config = load_config("config.yaml")
sample_duration = config["sample_duration_sec"]
num_samples = int(config["record_hours"]*(3600/sample_duration))


dt_start = datetime.now()
dt_stop = dt_start+timedelta(hours=24)

print("Started data logging at", dt_start)
print("Total number of samples to be recorded: ", num_samples)

d = 1
file_format = "wav"
resolution = "S32"
sampling_rate = "48000"

for i in range(num_samples):
    dt_now = datetime.now()
    print("Recording sample number on ", dt_now)
    dt_fname = time_stamp_fnamer(dt_now)+".wav"
    location = config["data_dir"]+dt_fname

    subprocess.call(["arecord", 
                     "--duration="+str(d), 
                     "-t", file_format,
                     "-f", resolution,
                     "-r", sampling_rate,
                     location])
    
    time_left = dt_stop-dt_now

    days, seconds = time_left.days, time_left.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    print("Time left {} hours {} minutes and {} seconds".format(hours,
                                                                minutes, 
                                                                seconds))
