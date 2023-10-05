import numpy as np
import pandas as pd
from os.path import join
from scipy.io.wavfile import write
import matplotlib.pyplot as plt


RECORDING_DIR = "recordings"
OUTPUT_DIR = "output_wav"

col_names = ["raw_audio", "filtered_audio"]
file_path = join(RECORDING_DIR, "doc5.csv")
data = pd.read_csv(file_path, names=col_names).astype(float)

print(data.dtypes)

raw_audio = data["raw_audio"].to_numpy()
filtered_audio = data["filtered_audio"].to_numpy()


def normalize_signal(x):
    x /= np.max(np.abs(x), axis=0)
    x -= 0.5
    return x


Fs = 9600  # 115200
raw_audio = normalize_signal(raw_audio)
filtered_audio = normalize_signal(filtered_audio)
N = len(raw_audio)
time = np.linspace(0, N / Fs, N)


plt.figure(figsize=(12, 4))
plt.plot(time, raw_audio, label="raw_audio")
plt.plot(time, filtered_audio, label="filterd_audio")
plt.xlabel("time")
plt.ylabel("Amplitude")
plt.legend()
plt.show()


wav_file_path = join(OUTPUT_DIR, "test_raw.wav")
write(wav_file_path, Fs, raw_audio)
