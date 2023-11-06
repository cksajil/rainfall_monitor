#! /bin/bash

login_time=$(date)
echo "System booted up at: $login_time"
source /home/pi/raingauge/code/ven/bin/activate
python daq_pi.py

stop_time=$(date)
echo "Data aquisition finished at: $login_time"