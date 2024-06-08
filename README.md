# Acoustic Rain Gauge
### R & D project at [ICFOSS](https://icfoss.in/)

Rainfall, also known as precipitation, is crucial for environmental stability. To maintain a sustainable ecosystem, it is essential for all living beings to have access to clean drinking water. Accurate precipitation monitoring is also vital for early flood warnings. Many efforts to achieve this goal rely on precise precipitation monitoring.

Precipitation monitoring devices are broadly classified into manual, mechanical, and optical categories. This project aims to develop accurate sensors that do not fall into the manual, mechanical, or optical categories. We attempt to predict precipitation using machine learning techniques with sound loudness as an input feature.

### [Click here](https://visualizedev.icfoss.org/d/riYMAg1Ik/non_mech_rain-_gauge?orgId=3&refresh=1m&from=now-24h&to=now) to see live data from our acoustic rain gauge

## Team Members
1. [Gopika T G](https://github.com/GopikaTG)
2. [Sajil C K](https://github.com/cksajil/)
3. [Manu Mohan M S](https://github.com/MMS731)
4. [Aiswarya Babu](https://github.com/aiswaryaaishh)
5. [Harikrishnan K P](https://github.com/Thelastblackpearl)

## Sensor Used
1. [USB Mic, Jieli Technology UACDemoV1.0](https://www.amazon.in/USB-Microphone/s?k=USB+Microphone)
<img src="https://images.meesho.com/images/products/293053361/m8ldc_512.webp" width="250"/>

## Data Acquisition Devices (DAQs)
1. [Davis AeroCone 6466M Rain Gauge](https://www.amazon.de/-/en/Davis-AeroCone-6466M-Gauge-Sensor/dp/B08629NFVG) - The mechanical rain gauge used as a reference for comparing rainfall against acoustic readings.
<img src="https://m.media-amazon.com/images/I/612KqYGrL7L._AC_SX466_.jpg" width="320"/>

2. [Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi) - Used as a DAQ device for high-resolution and high-sampling-rate audio recording.
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Raspberry_Pi_4_Model_B_-_Side.jpg/1200px-Raspberry_Pi_4_Model_B_-_Side.jpg" alt="Raspberry Pi" width="400"/>

## DAQ Setup
The setup guide can be found [here](https://github.com/cksajil/rainfall_monitor/blob/sajil/rain_gauge_setup.md).

## Data

### Data from USB Mic and Raspberry Pi
The USB mic captures audio files saved in WAV format with a fixed duration. The parameters for the audio files (e.g., sampling rate, sample duration, bit size, total recording time, etc.) can be set in the `config.yaml` file. The recorded audio files are analyzed for deep learning modeling.

The recorded WAV files are saved with a timestamp (`yyyy_mm_dd_hh_mm_ss_millisec.wav`) as shown below:

`2023_11_06_16_13_11_011224.wav`

### Datasets Available on Kaggle
1. [Rain_Data_Master_2023](https://www.kaggle.com/datasets/sajilck/rain-data-master-2023) - Contains all audio recordings and rainfall data from the mechanical rain gauge collected so far. Note that files have different durations (10 sec and 3 sec) and sampling rates (48K & 8K).
2. [Rain_Data_Master_8K](https://www.kaggle.com/datasets/sajilck/rain-data-master-8k) - Contains a downsampled version of [Rain_Data_Master_2023](https://www.kaggle.com/datasets/sajilck/rain-data-master-2023) with a uniform sample rate of 8K.

## Scripts
1. `daq_pi.py` and `davis_logger.py` - These are the main script files for data acquisition and model inference. `daq_pi.py` is used for automated audio recording on Raspberry Pi and model inference. `davis_logger.py` logs data from the Davis rain gauge using the Raspberry Pi's GPIO pins. These scripts can be initiated with the `nohup` command or by adding them to the `~/.bashrc` profile.
If added to the `~/.bashrc` profile, the script will run everytime the device boots up/user logs in/terminal opened. 

```console
nohup home/pi/raingauge/code/daq_pi.py &
nohup /home/pi/raingauge/code/davis_logger.py &
```

OR

```console
nano ~/.bashrc

# Appened the following line to the end of .bashrc file
python3 /home/pi/raingauge/code/daq_pi.py & python3 /home/pi/raingauge/code/davis_logger.py

# Reboot the device
sudo reboot
```

2. `mech_vs_non_mech_dataset_creation.ipynb` contains the Kaggle script to combine wave files recorded along with mechanical rain gauge data to create training data for deep learning modeling.

3. `seq_mech_vs_non_mech.ipynb` contains the LSTM modeling code which uses acoustic and mechanical data for rainfall estimation


## Results

### LSTM Sequential Model Performance
| **EPOCHS** | **MODEL** | **MAPE** |
|------------|-----------|----------|
| 25         | LSTM      | 31.15%   |



# Contact Information

You can find us at:

ICFOSS<br>
Greenfield Stadium,<br>
Opposite University of Kerala Campus, Karyavattom,<br>
Thiruvananthapuram, Kerala 695581

For more information, visit our [website](https://icfoss.in/).