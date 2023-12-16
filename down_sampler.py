import librosa
from tqdm import tqdm
import soundfile as sf
from os import listdir
from os.path import join


DATA_PATH = "/Users/sajil/Downloads/rain_data_master/rainfall_sound"
OUTPUT_PATH = "/Users/sajil/Downloads/rain_data_master/rainfall_sound_8k"
filenames = listdir(DATA_PATH)
target_Fs = 8000


for filename in tqdm(filenames):
    filepath = join(DATA_PATH, filename)
    try:
        audio, Fs = librosa.load(filepath, sr=target_Fs)
        sf.write(join(OUTPUT_PATH, filename), audio, target_Fs)
    except:
        print(filename)
