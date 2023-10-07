# Acoustic Rainfall Monitoring
## A project by ICFOSS

Rainfall also known as precipitation is an important part of enviroment stability. Inorder to have a sustainable echo system, it is important for living beings to have access to clean drinking water. Many efforts to attain this objective depends on accurate precipitation monitoring.

Precipitation monitoring devices are broadly classified into manuel, mechanical, and optical. It is desirable to have accurate sensors which are not manuel/mechanical/optical. This project is an attempt to predict precipitation using machine learning techniques and sound intensity as input feature.

### Sensors used

1. [Grove Loudness Sensor](https://wiki.seeedstudio.com/Grove-Loudness_Sensor/)
<img src="https://files.seeedstudio.com/wiki/Grove-Loudness_Sensor/img/Loudness%20Sensor_new.jpg" alt="drawing" width="250"/>

2. [Grove Sound Sensor](https://wiki.seeedstudio.com/Grove-Sound_Sensor/)
<img src="https://files.seeedstudio.com/wiki/Grove_Sound_Sensor/img/page_small_1.jpg" alt="drawing" width="250"/>

### Data
The `recordings` folder contains files with readings from mechanical and sound sensor devices. The data was recorded in-house at ICFOSS.

### Data Aquisition Device (DAQ)

We have used [Arduino Uno](https://en.wikipedia.org/wiki/Arduino_Uno) board as the DAQ device.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Arduino_Uno_-_R3.jpg/440px-Arduino_Uno_-_R3.jpg" width="400"/>


### Supporting scripts to monitor rainfall using acoustic sensors
1. eda_rainfall.ipynb : Contains exploratory data analysis and visualizations to derive insights from data recorded
