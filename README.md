# Acoustic Rain Gauge
### R & D project by [ICFOSS](https://icfoss.in/)

## Introduction
Rainfall, also known as precipitation, is crucial for environmental stability. Accurate precipitation monitoring is vital for weather forecasting and creating early flood warning systems. In this project we have developed an acoustic rain gauge that estimates rainfall by using sound as input data.

![Experiment Setup](https://raw.githubusercontent.com/cksajil/rainfall_monitor/gitlab/images/experiment_setup.jpeg)

**Figure 1:** Experiment setup

## Installation and Setup
The setup guide can be found [here](https://github.com/cksajil/rainfall_monitor/blob/gitlab/help/rain_gauge_setup_guide.md).

## Live Data and Visualization

![grafana](https://raw.githubusercontent.com/cksajil/rainfall_monitor/gitlab/images/data_visualisation.png)

### [Click here](http://117.223.185.200:3000/d/d6zIvsjIz/rain_pi_2?orgId=3&refresh=1m) to see live data from our acoustic rain gauge


## Components used
#### Sensor Used
1. [USB Mic, Jieli Technology UACDemoV1.0](https://www.amazon.in/USB-Microphone/s?k=USB+Microphone)
<img src="https://images.meesho.com/images/products/293053361/m8ldc_512.webp" width="250"/>

#### Data Acquisition Devices (DAQs)
1. [Davis AeroCone 6466M Rain Gauge](https://www.amazon.de/-/en/Davis-AeroCone-6466M-Gauge-Sensor/dp/B08629NFVG) - The mechanical rain gauge used as a reference for comparing rainfall against acoustic readings.
<img src="https://m.media-amazon.com/images/I/612KqYGrL7L._AC_SX466_.jpg" width="250"/>

2. [Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi) - Used as a DAQ device for high-resolution and high-sampling-rate audio recording.
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Raspberry_Pi_4_Model_B_-_Side.jpg/1200px-Raspberry_Pi_4_Model_B_-_Side.jpg" alt="Raspberry Pi" width="400"/>



## Data Collection

#### Data from USB Mic and Raspberry Pi
The USB mic captures audio files saved in WAV format with a fixed duration. The parameters for the audio files (e.g., sampling rate, sample duration, bit size, total recording time, etc.) can be set in the `config.yaml` file. The recorded audio files are analyzed for deep learning modeling.

The recorded WAV files are saved with a timestamp (`yyyy_mm_dd_hh_mm_ss_millisec.wav`) as shown below:

`2023_11_06_16_13_11_011224.wav`

#### Datasets Available on Kaggle
1. [Rain_Data_Master_2023](https://www.kaggle.com/datasets/sajilck/rain-data-master-2023) - Contains all audio recordings and rainfall data from the mechanical rain gauge collected so far. Note that files have different durations (10 sec and 3 sec) and sampling rates (48K & 8K).
2. [Rain_Data_Master_8K](https://www.kaggle.com/datasets/sajilck/rain-data-master-8k) - Contains a downsampled version of [Rain_Data_Master_2023](https://www.kaggle.com/datasets/sajilck/rain-data-master-2023) with a uniform sample rate of 8K.

## Usage
1. `daq_pi.py` and `davis_logger.py` - These are the main script files for data acquisition and model inference. `daq_pi.py` is used for automated audio recording on Raspberry Pi and model inference. `davis_logger.py` logs data from the Davis rain gauge using the Raspberry Pi's GPIO pins. These scripts can be initiated with the `nohup` command or by adding them to the `~/.bashrc` profile.
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

| Epochs | Model | Features | MAPE   | R²     | Correlation |
|--------|-------|----------|--------|--------|-------------|
| 25     | LSTM  | STFT     | 15.76% | 0.9683 | 0.9033      |
| 25     | LSTM  | Chroma   | 45.15% | 0.9700 | 0.1982      |
| 25     | LSTM  | MFCC     | 96.53% | 0.3418 | 0.4469      |

**Table 1:** Performance of LSTM model on various features

## Team Members
1. [Gopika T G](https://github.com/GopikaTG)
2. [Sajil C K](https://github.com/cksajil/)
3. [Manu Mohan M S](https://github.com/MMS731)
4. [Aiswarya Babu](https://github.com/aiswaryaaishh)
5. [Harikrishnan K P](https://github.com/harikrishnan-kp)

## License
This project is licensed under the MIT License - see the [LICENSE](https://raw.githubusercontent.com/cksajil/rainfall_monitor/gitlab/LICENSE) file for details.

## Contact Information

You can find us at:

**ICFOSS**<br>
Greenfield Stadium,<br>
Opposite University of Kerala Campus, Karyavattom,<br>
Thiruvananthapuram, Kerala 695581

For more information, visit our [website](https://icfoss.in/).
