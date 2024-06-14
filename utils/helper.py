import os
import yaml
import influxdb_client
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import LSTM, Dense, Reshape, Input
from influxdb_client.client.write_api import SYNCHRONOUS
from requests.exceptions import ConnectionError


def load_config(config_name: str, CONFIG_PATH="./config") -> dict:
    """
    A function to load and return config file in YAML format
    """
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config


# loading config files
config = load_config("config.yaml")


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
    model.add(Input((1025, 2672, 1)))
    model.add(Conv2D(64, kernel_size=(8, 8), activation="relu"))
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
    """
    Loads deep learning model, build it and loads weights
    """
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
        # Configure influxDB credentials
        influxdb_config = load_config("influxdb_api.yaml")
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
