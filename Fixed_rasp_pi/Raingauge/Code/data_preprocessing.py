
import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm
from os import listdir
from os.path import join
from datetime import datetime


DATA_PATH = "/home/gopika/gopika/Office_Docs/rainfall_monitor/Fixed_rasp_pi/Raingauge/"
MECH_FILE_PATH = "/home/gopika/gopika/Office_Docs/rainfall_monitor/Fixed_rasp_pi/Raingauge/Data/mech_data_jan_5_2024.csv"
NON_MECH_PATH = "/home/gopika/gopika/Office_Docs/rainfall_monitor/Fixed_rasp_pi/Raingauge/Data/data/"
Fs = 8000
MAX_LEN = 170*8000  # total number of samples in the 3 min audio files

mech_data = pd.read_csv(join(DATA_PATH, MECH_FILE_PATH))
mech_data["Time"] = pd.to_datetime(mech_data["Time"])
wave_files = sorted(listdir(NON_MECH_PATH))
wave_files = [x for x in wave_files if ".wav" in x]
N = len(wave_files)

mech_data = pd.read_csv(join(DATA_PATH, MECH_FILE_PATH))
mech_data["Time"] = pd.to_datetime(mech_data["Time"])
wave_files = sorted(listdir(NON_MECH_PATH))
wave_files = [x for x in wave_files if ".wav" in x]
N = len(wave_files)


def filename_parser(filename):
    year, month, day, hour, minute, second, _ = map(int, 
                                                    filename.split(".")[0].split("_"))
    return datetime(year, month, day, hour, minute, second)


start_time = filename_parser(wave_files[0])
end_time = filename_parser(wave_files[-1])

row_overlap = (mech_data["Time"] > start_time) & (mech_data["Time"] < end_time)
mech_data = mech_data[row_overlap]


def load_wav(file_path, Fs):
    audio, Fs = librosa.load(file_path, sr=Fs)
    duration = librosa.get_duration(y=audio, sr=Fs)
    return audio, Fs, duration


def format_rainfall(rain_fall):
    rain_fall, unit = rain_fall.split(" ")
    if unit == "µm":
        rain_fall = float(rain_fall)/(10**3)
    elif unit == "mm":
        rain_fall = float(rain_fall)
    return rain_fall


def get_checkpoints(mech_data, wave_files):
    start_time = filename_parser(wave_files[0])
    start_times = []
    checkpoints = []
    targets = []
    for idx, row in mech_data.iterrows():
        checkpoint = row["Time"]
        target = format_rainfall(row["device_frmpayload_data_rainfall"])
        start_times.append(start_time)
        checkpoints.append(checkpoint)
        targets.append(target)
        start_time = checkpoint
    return start_times, checkpoints, targets


start_times, checkpoints, targets = get_checkpoints(mech_data, wave_files)
K = len(checkpoints)
print("Length of start times: ", len(start_times))
print("Length of checkpoints: ", K)
print("Length of targets : ", len(targets))


def file_flagger(file_name, start_time, checkpoint):
    file_name_short = file_name.split("_")[:-1]
    year, month, day, hour, minute, second = map(int, file_name_short)
    fname_time = datetime(year, month, day, hour, minute, second)
    return start_time <= fname_time <= checkpoint


def file_filter(wave_files, start_time, checkpoint):
    filtered_files = [x for x in wave_files if file_flagger(x, start_time,
                                                            checkpoint)]
    return filtered_files


data_basic = pd.DataFrame()
target = np.array([])
for idx in tqdm(range(1, K)):
    if start_times[idx] != checkpoints[idx]:
        selected_files = file_filter(wave_files, start_times[idx],
                                     checkpoints[idx])
        num_files = len(selected_files)
        if num_files:
            audio_sample = np.array([])
            for one_file in selected_files:
                file_path = join(NON_MECH_PATH, one_file)
                audio, Fs, duration = load_wav(file_path, Fs)
                audio_sample = np.append(audio_sample, audio)
            audio_sample = audio_sample[:MAX_LEN]
            with open("audio_{}.npy" .format(idx), "wb") as f:
                np.save(f, audio_sample)
            data_row = {"start_time": start_times[idx],
                        "checkpoint": checkpoints[idx],
                        "num_files": num_files,
                        "fname": "audio_{}.npy".format(idx),
                        "target": targets[idx]}
            data_basic = pd.concat([data_basic, pd.DataFrame([data_row])],
                                   ignore_index=True)          
data_basic.to_csv("rain_data_basic.csv")



