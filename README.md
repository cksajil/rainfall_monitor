# Acoustic Rainfall Monitoring
## A project by [ICFOSS](https://icfoss.in/)

### [Click here](https://visualizedev.icfoss.org/d/riYMAg1Ik/non_mech_rain-_gauge?orgId=3&refresh=1m&from=now-24h&to=now) to see live data on Grafana dashboard

Rainfall also known as precipitation is an important part of environment stability. Inorder to have a sustainable echo system, it is important for living beings to have access to clean drinking water. It is also important for early flood warning as well. Many efforts to attain this objective depends on accurate precipitation monitoring.

Precipitation monitoring devices are broadly classified into manuel, mechanical, and optical. It is desirable to have accurate sensors which are not manuel/mechanical/optical. This project is an attempt to predict precipitation using machine learning techniques with sound loudness as input feature.

## Project Members
1. Gopika T G
2. [Sajil C K](https://github.com/cksajil/)
3. Manu Mohan M S
4. Aiswarya Babu 
5. [Harikrishnan K P](https://github.com/Thelastblackpearl)

## Sensor used
1. [USB Mic, Jieli Technology UACDemoV1.0](https://www.amazon.in/USB-Microphone/s?k=USB+Microphone)
<img src="https://images.meesho.com/images/products/293053361/m8ldc_512.webp" width="250"/>

## Data Aquisition Devices (DAQs)
1. [Davis AeroCone 6466M Rain Gauge](https://www.amazon.de/-/en/Davis-AeroCone-6466M-Gauge-Sensor/dp/B08629NFVG) is the mechanical raingauge we are using as a reference for comparing rainfall against acoustic readings.
<img src="https://m.media-amazon.com/images/I/612KqYGrL7L._AC_SX466_.jpg" widht="320"/>

2. We used [Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi) as a DAQ device for audio recording with high resolution and sampling rate.
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Raspberry_Pi_4_Model_B_-_Side.jpg/1200px-Raspberry_Pi_4_Model_B_-_Side.jpg" alt="raspberrypi" width="400"/>

## DAQ Setup
The setup guide can be found [here](https://github.com/cksajil/rainfall_monitor/blob/sajil/rain_gauge_setup.md)

## Data

### Data from USB mic and Raspberry
The data from USB mic contains audio files saved in wav format with a fixed duration. The parameters of desired audio files (e.g. sampling rate, sample duration, bit size, total recording time, etc.) can be set in the `config.yaml` file. The recorded audio files are further analysed for deep learning modeling.

The recorded wav files are saved with a timestamp (`yyyy_mm_dd_hh_mm_ss_millisec.wav`) file name as shown below.

`2023_11_06_16_13_11_011224.wav`

#### Datasets made available on Kaggle
1. [Rain_Data_Master_2023](https://www.kaggle.com/datasets/sajilck/rain-data-master-2023) contains all audio recordings and rainfall data from mechanical rainguage in overlapping time durations collected so far. Please note that files are of different duration (10 sec and 3 sec) and sampling rates (48K & 8K).

2. [Rain_Data_Master_8K](https://www.kaggle.com/datasets/sajilck/rain-data-master-8k) Contains downsamples version of [Rain_Data_Master_2023](https://www.kaggle.com/datasets/sajilck/rain-data-master-2023) so that all files are of same sample rate (i.e. 8K).

## Scripts
1. `daq_pi.py` and `davis_logger.py` are the main script files used for data aquisition and model inference. Here `daq_pi.py` is used for automated audio recording in Raspberry and model inference.  `davis_logger.py` is used to log data from Davis rain gauge using GPIO pins of Raspberry Pi. These scripts can be initiated with the `nohup` command or by adding it to `~/.bashrc` profile.
If added to the `~/.bashrc` profile, the script will run everytime the device boots up/user logs in/terminal opened. 

```bash
nohup home/pi/raingauge/code/daq_pi.py &
nohup /home/pi/raingauge/code/davis_logger.py &
```

OR

```bash
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
