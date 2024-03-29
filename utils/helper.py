import os
import yaml
from keras.models import Sequential
from keras.layers import LSTM, Dense, Reshape
from keras.layers import Conv2D, MaxPooling2D
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from requests.exceptions import ConnectionError


def time_stamp_fnamer(tstamp) -> str:
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


def load_config(config_name: str) -> dict:
    """
    A function to load and return config file in YAML format
    """
    CONFIG_PATH = "/home/pi/raingauge/code/config"
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config


def create_folder(directory: str) -> None:
    """
    Function to create a folder in a location if it does not exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_lstm_model_withoutcnn() -> any:
    """Creates and returns an LSTM model with only Dense blocks"""
    model = Sequential()
    model.add(LSTM(20))
    model.add(Dense(32))
    model.add(Dense(16))
    model.add(Dense(1))
    return model


def create_lstm_model_withcnn() -> any:
    """Creates and returns LSTM models with Conv and Dense blocks"""
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


def load_estimate_model(model_path: str) -> any:
    """Loads deep learning model, build it and loads weights"""
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
    try:
        influxdb_config = load_config("influxdb_api.yaml")

        # Configure influxDB credentials
        bucket = influxdb_config["bucket"]
        org = influxdb_config["org"]
        token = influxdb_config["token"]
        url = influxdb_config["url"]

        # creating an object of influxdb_client
        client = influxdb_client.InfluxDBClient(
            url=url, token=token, org=org, timeout=30_000
        )
        write_api = client.write_api(write_options=SYNCHRONOUS)
        p = (
            influxdb_client.Point("ML-prediction")
            .tag("location", "greenfield tvm")
            .field("rain", rain)
        )

        write_api.write(bucket=bucket, org=org, record=p)
        client.close()
        return True
    except ConnectionError as e:
        print(f"Connection to InfluxDB failed: {e}")
        return False
