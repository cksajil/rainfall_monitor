import os
import pandas as pd
from tqdm import tqdm
from os import listdir
from datetime import datetime, timedelta


MECH_FILE_PATH = "/home/icfoss/Downloads/rainpi2_sample/davis_label.csv"

NON_MECH_PATH = "/home/icfoss/Downloads/rainpi2_sample/new data/"

mech_data = pd.read_csv(MECH_FILE_PATH)
mech_data["time"] = pd.to_datetime(mech_data["time"])
wave_files = sorted(listdir(NON_MECH_PATH))


def extract_datetime_from_filename(filename):
    timestamp_str = filename.split(".")[0]
    return datetime.strptime(timestamp_str, "%Y_%m_%d_%H_%M_%S_%f")


def delete_files(filtered_wavefiles, directory):
    for wave_file in filtered_wavefiles:
        file_path = os.path.join(directory, wave_file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            print(f"File not found: {file_path}")


def find_files_to_delete(mech_data, wave_files):
    filtered_wavefiles = []
    for wave_file in wave_files:
        file_datetime = extract_datetime_from_filename(wave_file)
        for checkpoint in mech_data["time"]:
            if checkpoint - timedelta(minutes=3) <= file_datetime <= checkpoint:
                filtered_wavefiles.append(wave_file)
    return list(set(wave_files) - set(filtered_wavefiles))


delete_files(find_files_to_delete(mech_data, wave_files), NON_MECH_PATH)
