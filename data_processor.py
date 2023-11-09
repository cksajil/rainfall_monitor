import numpy as np
from tqdm import tqdm
from os.path import join
from os import listdir
import pandas as pd
from scipy.io import wavfile
import librosa

RECORDING_DIR = "data/rain_mini_dataset"
PROCESSED_DIR = "data/processed_dataset"
CLASSES = ["rain", "ambient"]
SAMPLING_RATE = 16000
SAMPLE_DURATION = 10

file_names = []
target = []

for label in CLASSES:
    fnames = listdir(join(RECORDING_DIR, label))
    num_samples = len(fnames)
    file_names.extend(fnames)
    target.extend([label] * num_samples)

basic_data = pd.DataFrame()
basic_data["filename"] = file_names
basic_data["class"] = target
basic_data["target"] = basic_data["class"].replace({"ambient": 0, "rain": 1})


for index, row in tqdm(basic_data.iterrows(), total=basic_data.shape[0]):
    file_path = join(RECORDING_DIR, row["class"], row["filename"])
    audio, Fs = librosa.load(file_path, sr=SAMPLING_RATE)
    audio /= np.max(np.abs(audio),axis=0)
    audio = audio*65500
    audio = audio.astype(np.int16)
    audio_segments = np.split(audio, 10)
    i = 0
    for x in audio_segments:
        fname = row["filename"].split(".")[0]
        out_file_path = join(PROCESSED_DIR, row["class"], fname+"_"+str(i))
        wavfile.write(out_file_path, SAMPLING_RATE, x)
        i+=1






