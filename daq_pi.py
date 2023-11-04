import subprocess
from os import path
from datetime import datetime
from utils.helper import time_stamp_fnamer
from utils.helper import load_config


config = load_config("config.yaml")
dt_now = datetime.now()

print("Started data logging at", dt_now)
dt_fname = time_stamp_fnamer(dt_now)+".wav"

d = 60
file_format = "wav"
resolution = "S32"
sampling_rate = "48000"
location = config["data_dir"]+dt_fname

subprocess.call(["arecord", 
                 "--duration="+str(d), 
                 "-t", file_format,
                 "-f", resolution,
                 "-r", sampling_rate,
                 location])

# with open(path.join(config["data_dir"], dt_fname), "w") as f:
#     f.write("sample data")