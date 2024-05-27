import os
import shutil
import pandas as pd
from tqdm import tqdm
from os import listdir, path
from datetime import datetime, timedelta
from utils.helper import create_folder

MECH_FILE_PATH = "/home/icfoss/Downloads/rain_data_mechanical_master.csv"
NON_MECH_PATH = "/home/icfoss/Downloads/rainfall_sound_8k/"

mech_data = pd.read_csv(MECH_FILE_PATH)
mech_data["Time"] = pd.to_datetime(mech_data["Time"])
wave_files = sorted(listdir(NON_MECH_PATH))


def move_files(file_list, src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for file_name in file_list:
        src_file = os.path.join(src_folder, file_name)
        dest_file = os.path.join(dest_folder, file_name)

        if os.path.exists(src_file):
            shutil.move(src_file, dest_file)
            print(f"Moved: {src_file} to {dest_file}")
        else:
            print(f"File not found: {src_file}")


def extract_datetime_from_filename(filename):
    timestamp_str = filename.split(".")[0]
    return datetime.strptime(timestamp_str, "%Y_%m_%d_%H_%M_%S_%f")


def get_files_in_window(wave_files, checkpoint):
    selected_files = []
    for wave_file in wave_files:
        file_datetime = extract_datetime_from_filename(wave_file)
        if checkpoint - timedelta(minutes=3) <= file_datetime <= checkpoint:
            selected_files.append(wave_file)
    return selected_files


for checkpoint in tqdm(mech_data["Time"]):
    folder_name = str(checkpoint)
    src_folder = path.join("/home/icfoss/Downloads/", "rainfall_sound_8k")
    dest_folder = path.join("/home/icfoss/Downloads/", folder_name)
    create_folder(dest_folder)
    checkpoint_files = get_files_in_window(wave_files, checkpoint)
    move_files(checkpoint_files, src_folder, dest_folder)
