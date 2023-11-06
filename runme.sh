#! /bin/bash

login_time=$(date)
echo "System booted up at: $login_time"
source /home/pi/raingauge/code/venv/bin/activate
python /home/pi/raingauge/code/daq_pi.py

stop_time=$(date)
echo "Data aquisition finished at: $login_time"