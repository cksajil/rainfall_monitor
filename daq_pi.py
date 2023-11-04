from os import path
from datetime import datetime
from utils.helper import time_stamp_fnamer
from utils.helper import load_config


config = load_config("config.yaml")

dt_now = datetime.now()
print("Started data logging at", dt_now)

dt_fname = time_stamp_fnamer(dt_now)

with open(path.join(config["data_dir"], dt_fname), "w") as f:
    f.write("sample data")