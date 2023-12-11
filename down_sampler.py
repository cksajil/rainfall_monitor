from tqdm import tqdm
from os import listdir
from os.path import join
from scipy.io import wavfile
from scipy.signal import resample

DATA_PATH = "/Users/sajil/Downloads/rain_data_master/rainfall_sound"
OUTPUT_PATH = "/Users/sajil/Downloads/rain_data_master/rainfall_sound_8k"
filenames = listdir(DATA_PATH)
target_Fs = 8000


def downsample(data, Fs, target_Fs):
    resampled_data = resample(data, int(len(data) * target_Fs / Fs))
    return resampled_data


for filename in tqdm(filenames):
    filepath = join(DATA_PATH, filename)
    try:
        Fs, audio = wavfile.read(filepath)
        audio = downsample(audio, Fs, target_Fs)
        wavfile.write(join(OUTPUT_PATH, filename), target_Fs, audio)
    except:
        print(filename)
