import pandas as pd
import numpy as np
from tqdm import tqdm
from os.path import join
from scipy.io.wavfile import write

RECORDING_DIR = "recordings"
OUTPUT_DIR = "output_wav"
WIO_PROCESSED_FILE = "wio_processed.csv"
WIO_TERMINAL_FILE = "recordings.txt"
AUDIO_FILE = "sample_audio.wav"
Fs = 8000

data = pd.read_csv(WIO_TERMINAL_FILE, names=["timestamp", "audio"])
data_normalized = pd.DataFrame()
data["audio"] = data["audio"].astype(float)
raw_array = data["audio"]

xmin = np.min(raw_array)
xmax = np.max(raw_array)
raw_array = (raw_array-xmin)/(xmax-xmin)
raw_array-=0.5

data_normalized["raw_audio"] = raw_array
data_normalized.to_csv(join(RECORDING_DIR, WIO_PROCESSED_FILE), index=False)

write(join(OUTPUT_DIR, AUDIO_FILE), Fs, raw_array)
