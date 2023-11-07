# Acoustic Rainfall Monitoring
## A project by [ICFOSS](https://icfoss.in/)

Rainfall also known as precipitation is an important part of enviroment stability. Inorder to have a sustainable echo system, it is important for living beings to have access to clean drinking water. It is also important for early flood warning as well. Many efforts to attain this objective depends on accurate precipitation monitoring.

Precipitation monitoring devices are broadly classified into manuel, mechanical, and optical. It is desirable to have accurate sensors which are not manuel/mechanical/optical. This project is an attempt to predict precipitation using machine learning techniques with sound loudness as input feature.


## Project Members
1. Gopika
2. [Sajil](https://github.com/cksajil/)
3. Manu
4. Aishwarya


## Sensors used
1. [Grove Loudness Sensor](https://wiki.seeedstudio.com/Grove-Loudness_Sensor/)
<img src="https://files.seeedstudio.com/wiki/Grove-Loudness_Sensor/img/Loudness%20Sensor_new.jpg" alt="drawing" width="250"/>

2. [Grove Sound Sensor](https://wiki.seeedstudio.com/Grove-Sound_Sensor/)
<img src="https://files.seeedstudio.com/wiki/Grove_Sound_Sensor/img/page_small_1.jpg" alt="drawing" width="250"/>

3. [USB Mic](https://www.amazon.in/USB-Microphone/s?k=USB+Microphone)


## Data Aquisition Devices (DAQs)
1. [Davis AeroCone 6466M Rain Gauge](https://www.amazon.de/-/en/Davis-AeroCone-6466M-Gauge-Sensor/dp/B08629NFVG) is the mechanical raingauge we are using as a reference for comparing rainfall against acoustic readings.
<img src="https://m.media-amazon.com/images/I/612KqYGrL7L._AC_SX466_.jpg" widht="320"/>

2. We have used [Arduino Uno](https://en.wikipedia.org/wiki/Arduino_Uno) board as the DAQ device for Grove sound and loudness sensors.
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Arduino_Uno_-_R3.jpg/440px-Arduino_Uno_-_R3.jpg" width="400"/>

3. We also used [Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi) as a DAQ device for audio recording with high resolution and sampling rate.
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Raspberry_Pi_4_Model_B_-_Side.jpg/1200px-Raspberry_Pi_4_Model_B_-_Side.jpg" alt="raspberrypi" width="400"/>


## Data
### Data from Grove sensors and Arduino
The `recordings` folder contains files with readings from mechanical and sound sensor devices. The data was recorded in-house at ICFOSS. The recording files contains timestamps and its corresponding rainfall/sound readings from mechanical and our DAQ respectively. The dataset after cleaning and preprocessing will look like the one below.

| datetime            | ntips | rainfall (mm) | sound | loudness | timedelta       | timedelta_min |
|---------------------|-------|---------------|-------|----------|-----------------|---------------|
| 2023-10-03 22:52:00 | 2     | 0.56          | 378.0 | 137.0    | 0 days 00:00:00 | 0             |
| 2023-10-03 22:53:00 | 2     | 0.56          | 360.0 | 128.0    | 0 days 00:01:00 | 1             |
| 2023-10-03 23:29:00 | 4     | 1.12          | 380.0 | 141.0    | 0 days 00:36:00 | 36            |
| 2023-10-04 01:44:00 | 1     | 0.28          | 384.0 | 137.0    | 0 days 02:15:00 | 135           |

Here the `timedelta` feature is the time difference between previous tippping time and current tipping time.

### Data from USB mic and Raspberry
The data from USB mic contains audio files saved in wav format with a fixed duration. The parameters of desired audio files (e.g. sampling rate, sample duration, bit size, total recording time, etc.) can be set in the `config.yaml` file. The recorded audio files are further analysed for deep learning modeling.

The recorded wav files are saved with a timestamp (`yyyy_mm_dd_hh_mm_ss_millisec.wav`) file name as shown below.

`2023_11_06_16_13_11_011224.wav`

## Scripts
1. `eda_rainfall.ipynb` : Contains exploratory data analysis and visualizations to derive insights from data recorded.
2. `daq_pi.py` contains Python script for automated audio recording which is added to the `~/.bashrc` profile so that the script is run everytime the device boots up and logs in.

## Results
### Correlation Table

| Pearson correlation            |           |              |
|--------------------------------|-----------|--------------|
|                                | **Sound** | **Loudness** |
| **Rainfall (mm) (mechanical)** | 0.265357  | **0.737172** |
| Spearman correlation           |           |              |
|                                | **Sound** | **Loudness** |
| **Rainfall (mm) (mechanical)** | 0.152554  | **0.839047** |


### Observations
1. There is correlation w.r.t. mechanical readings and acoustic measurements
2. The acoustic feature loudness (`pearson: 0.7371`) is found to be more correlated to mechanical measurements
3. For low volumes of rain (`e.g. <=0.28 mm`), the variation in loudness is not very useful. Hence in these cases a different strategy needs to be devised
4. For low volumes of rain the tipping event happens relatively after longer duration (`10-150 minutes`). Hence loudness measurement in the last 1 minute may not account for the drizzling rain happened from the previous tipping point.