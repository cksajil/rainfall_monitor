import os
import yaml
from os import remove
from os.path import exists
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import LSTM, Dense, Reshape, Input


def load_config(
    config_name: str, CONFIG_PATH="/home/ubuntu/raingauge/code/config"
) -> dict:
    """
    A function to load and return config file in YAML format
    """
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config


# loading config files
config = load_config("config.yaml")


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


def create_folder(directory: str) -> None:
    """
    Function to create a folder in a location if it does not exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def delete_files(file_paths):
    """Function to delete wav files after inference"""
    for file_path in file_paths:
        try:
            if exists(file_path):
                remove(file_path)
                print(f"Deleted: {file_path}")
            else:
                print(f"File does not exist: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


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
