import os
import yaml
from keras.models import Sequential
from keras.layers import LSTM, Dense, Reshape
from keras.layers import Conv2D, MaxPooling2D
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

def time_stamp_fnamer(tstamp):
    """
    A function to generate filenames from timestamps
    """
    cdate, ctime = str(tstamp).split(" ")
    current_date = "_".join(cdate.split("-"))
    chour, cmin, csec = ctime.split(":")
    csec, cmilli = csec.split(".")
    current_time = "_".join([chour, cmin, csec, cmilli])
    current_date_time_name = "_".join([current_date, current_time])
    return current_date_time_name


def load_config(config_name: str):
    """
    A function to load and return config file in YAML format
    """
    CONFIG_PATH = "/home/pi/raingauge/code/config"
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config


def create_folder(directory: str) -> None:
    """Function to create a folder in a location if it does not exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_log_file(log_folder: str, log_file: str) -> None:
    with open(os.path.join(log_folder, log_file), "a") as f:
        f.write("")


def create_lstm_model_withoutcnn():
    model = Sequential()
    model.add(LSTM(20))
    model.add(Dense(32))
    model.add(Dense(16))
    model.add(Dense(1))
    return model


def create_lstm_model_withcnn():
    model = Sequential()
    model.add(
        Conv2D(64, kernel_size=(8, 8), activation="relu", input_shape=(1025, 2657, 1))
    )
    model.add(MaxPooling2D(pool_size=(8, 8)))
    model.add(Conv2D(32, kernel_size=(4, 4), activation="relu"))
    model.add(MaxPooling2D(pool_size=(4, 4)))
    model.add(Conv2D(16, kernel_size=(2, 2), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Reshape((1, -1)))
    model.add(LSTM(20))
    model.add(Dense(32))
    model.add(Dense(16))
    model.add(Dense(1))
    return model


def load_estimate_model(model_path):
    config = load_config("config.yaml")
    if config["deployed_model_type"] == "withcnn":
        model = create_lstm_model_withcnn()
    else:
        model = create_lstm_model_withoutcnn()

    model.build(input_shape=config["stft_shape"])
    model.load_weights(model_path)
    return model


def influxdb(rain: float) -> bool: 
    """
    function to write data to influxdb
    """
    # Configure influxDB credentials 
    bucket = "<my-bucket>" # use our bucket name instead of <my-bucket>
    org = "<my-org>"       # use our org name instead of <my-org>
    token = "<my-token>"   # use our token instaed of <my-token>
    url="https://us-west-2-1.aws.cloud2.influxdata.com" # Store the URL of your InfluxDB instance

    #creating an object of influxdb_client
    client = influxdb_client.InfluxDBClient(url=url,token=token,org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    p = influxdb_client.Point("ML-prediction").tag("location","greenfield tvm").field("rain",rain)
    write_api.write(bucket=bucket, org=org, record=p)
    client.close()
    return True
