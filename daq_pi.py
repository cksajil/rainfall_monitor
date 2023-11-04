from datetime import datetime
from utils.helper import time_stamp_fnamer

dt_now = datetime.now()
print("Started data logging at", dt_now)

dt_fname = time_stamp_fnamer(dt_now)
print(dt_fname)