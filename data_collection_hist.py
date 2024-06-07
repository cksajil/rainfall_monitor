import pandas as pd
from tqdm import tqdm
from os import listdir
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

NON_MECH_PATH = "/home/icfoss/Datasets/rain_data_master_8k/rainfall_sound_8k/"
wave_files = sorted(listdir(NON_MECH_PATH))
hour_minutes = []


def extract_datetime(filename):
    year, month, day, hour, min, sec, _ = filename.split(".")[0].split("_")
    return hour, min


for wave_file in tqdm(wave_files):
    hour, min = extract_datetime(wave_file)
    hour_minutes.append(hour)

counts = Counter(hour_minutes)
df = pd.DataFrame.from_dict(counts, orient="index")
df.sort_index(inplace=True)
df.plot(kind="bar")
plt.xticks(rotation=90)
plt.xlabel("Hours of recording")
plt.ylabel("Count")
plt.show()
