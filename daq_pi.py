import subprocess
from os import path
from datetime import datetime, timedelta
from utils.helper import time_stamp_fnamer
from utils.helper import load_config


config = load_config("config.yaml")

d = config["sample_duration_sec"]
file_format = config["file_format"]
resolution = config["resolution"]
sampling_rate = config["sampling_rate"]

num_samples = int(config["record_hours"]*(3600/d))

dt_start = datetime.now()
dt_stop = dt_start+timedelta(hours=24)

#f = open(path.join(config["log_dir"], "log.txt"), "w+")

print("Started data logging at {}\n".format(dt_start))
print("Total number of samples to be recorded: {}\n".format(num_samples))


for i in range(num_samples):
    dt_now = datetime.now()
    print("Recording sample number {} on {}".format(i, dt_now))
    dt_fname = time_stamp_fnamer(dt_now)+".wav"
    location = config["data_dir"]+dt_fname

    subprocess.call(["arecord",
                     "-q",
                     "--duration="+str(d), 
                     "-t", str(file_format),
                     "-f", str(resolution),
                     "-r", sampling_rate,
                     location])
    
    time_left = dt_stop-dt_now

    days, seconds = time_left.days, time_left.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    print("Time left {} hours {} minutes and {} seconds\n".format(hours,
                                                                minutes, 
                                                                seconds))
dt_end = datetime.now()
print("Finished data logging at {}\n".format(dt_end))
#f.close()
