# Acoustic Rainfall Monitoring
## A project by [ICFOSS](https://icfoss.in/)

### [https://non-mechanical-raingauge-icfoss.streamlit.app/](https://non-mechanical-raingauge-icfoss.streamlit.app/)

<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdm15b3gwZ2o3dnoxZWNxd3Bod3l0MXNsdHprdm41M2N0ajdpZ2k0NSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wxpaNs949jOarTPxFZ/giphy.gif" width="600">

Rainfall also known as precipitation is an important part of environment stability. Inorder to have a sustainable echo system, it is important for living beings to have access to clean drinking water. It is also important for early flood warning as well. Many efforts to attain this objective depends on accurate precipitation monitoring.

Precipitation monitoring devices are broadly classified into manuel, mechanical, and optical. It is desirable to have accurate sensors which are not manuel/mechanical/optical. This project is an attempt to predict precipitation using machine learning techniques with sound loudness as input feature.

## Project Members
1. Gopika T G
2. [Sajil C K](https://github.com/cksajil/)
3. Manu Mohan M S
4. Aiswarya Babu 
5. Harikrishnan K P

## Sensor used
1. [USB Mic, Jieli Technology UACDemoV1.0](https://www.amazon.in/USB-Microphone/s?k=USB+Microphone)
<img src="https://images.meesho.com/images/products/293053361/m8ldc_512.webp" width="250"/>

## Data Aquisition Devices (DAQs)
1. [Davis AeroCone 6466M Rain Gauge](https://www.amazon.de/-/en/Davis-AeroCone-6466M-Gauge-Sensor/dp/B08629NFVG) is the mechanical raingauge we are using as a reference for comparing rainfall against acoustic readings.
<img src="https://m.media-amazon.com/images/I/612KqYGrL7L._AC_SX466_.jpg" widht="320"/>

2. We used [Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi) as a DAQ device for audio recording with high resolution and sampling rate.
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Raspberry_Pi_4_Model_B_-_Side.jpg/1200px-Raspberry_Pi_4_Model_B_-_Side.jpg" alt="raspberrypi" width="400"/>


## Data

### Data from USB mic and Raspberry
The data from USB mic contains audio files saved in wav format with a fixed duration. The parameters of desired audio files (e.g. sampling rate, sample duration, bit size, total recording time, etc.) can be set in the `config.yaml` file. The recorded audio files are further analysed for deep learning modeling.

The recorded wav files are saved with a timestamp (`yyyy_mm_dd_hh_mm_ss_millisec.wav`) file name as shown below.

`2023_11_06_16_13_11_011224.wav`

#### Datasets made available on Kaggle
1. [Rain_Data_Master_2023](https://www.kaggle.com/datasets/sajilck/rain-data-master-2023) contains all audio recordings and rainfall data from mechanical rainguage in overlapping time durations collected so far. Please note that files are of different duration (10 sec and 3 sec) and sampling rates (48K & 8K).

2. [Rain_Data_Master_8K](https://www.kaggle.com/datasets/sajilck/rain-data-master-8k) Contains downsamples version of [Rain_Data_Master_2023](https://www.kaggle.com/datasets/sajilck/rain-data-master-2023) so that all files are of same sample rate (i.e. 8K).

3. [Rainfall_Mechanical_22_November_2023](https://www.kaggle.com/datasets/sajilck/rainfall-mechanical-22-november-2023) contains both audio recordings and rainfall data from mechanical rainguage in overlapping time duration (~10 hrs).

4. The dataset [rainfall-mini-dataset](https://www.kaggle.com/datasets/sajilck/rainfall-mini-dataset) contains audio recordings which are classified into two main categories "rain" and "ambient" each class containing 24 samples of 10 seconds duration.

5. [rain-drop-mini-splitted](https://www.kaggle.com/datasets/sajilck/rain-drop-mini-splitted) is a splitted version of [rainfall-mini-dataset](https://www.kaggle.com/datasets/sajilck/rainfall-mini-dataset) where each 10 second audio is splitted into samples of 200 milliseconds duration.

6. [rain-drop-count-basic](https://www.kaggle.com/datasets/sajilck/rain-drop-count-basic) contains the labeled value, i.e the number of rain drops in each of the samples in [rain-drop-mini-splitted](https://www.kaggle.com/datasets/sajilck/rain-drop-mini-splitted)

7. [rainfall-sound-2023-11-13-14-00-00-icfoss](https://www.kaggle.com/datasets/sajilck/rainfall-sound-2023-11-13-14-00-00-icfoss) is the rainfall sound recorded on 13th November 2023 afternoon near ICFOSS premise. The rainfall sound on the metallic enclosure was recorded using Raspberry Pi and USB Mic. The sampling rate was 48Ksamples/sec at 32bit resolution. Each audio file has a duration of 10 seconds. The timestamp corresponding to each file was corrupted (to last known time in the device) due to lack of real-time clock/wifi connectivity in the recording setup.

## Scripts
1. `daq_pi.py` contains Python script for automated audio recording in Raspberry which is added to the `~/.bashrc` profile so that the script is run everytime the device boots up and logs in.
2. `seq_mech_vs_non_mech.ipynb` contains the LSTM modeling code which uses acoustic and mechanical data for rainfall estimation
3. `rain_drop_counter_modeling.ipynb` is a jupyter notebook which trains a deep learning model to predict number of rain drops in every 200 millliseconds. The best model has a test accuracy of 78%.
4. `raindrop_counter.py` is a Python script which can count the number of rain drops in a raspberry pi recorded audio using the deep learning model trained on step 3.

## Launch Streamlit App
```console
streamlit run demo_app.py
```

## Results

#### LSTM Sequential Model Performance
| **EPOCHS** | **MODEL** | **MAPE** |
|------------|-----------|----------|
| 25         | LSTM      | 31.15%   |

### Rain Drop Counting Model Performance
| **Epochs** | **Model** | **Test accuracy** | **Test loss** |
|------------|-----------|-------------------|---------------|
| 50         | DNN       | 75.76%            | 1.966277      |

### Observations
1. The LSTM based sequential model is having a reasonably good performance with a Mean Absolute Percentage Error (MAPE) of 31.15%
2. The test accuracy of DNN model trained on [rain-drop-mini-splitted](https://www.kaggle.com/datasets/sajilck/rain-drop-mini-splitted) dataset is 75%-78%.
