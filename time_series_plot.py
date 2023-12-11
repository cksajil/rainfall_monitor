import datetime
import pandas as pd
from os.path import join
import matplotlib.pyplot as plt


def time_series_plot(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    start_time = datetime.datetime(2023, 12, 8, 17, 0, 0)
    end_time = datetime.datetime(2023, 12, 9, 15, 0, 0)
    row = (df["timestamp"] > start_time) & (df["timestamp"] < end_time)
    df = df[row]
    plt.rcParams["figure.figsize"] = (12, 4)
    plt.plot(df["timestamp"], df["rainfall (mm)"], c="b", label="estimated")
    plt.xlabel("timestamp")
    plt.ylabel("rainfall (mm)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    filepath = join("rain_dataset", "estimate_08_Dec_2023.csv")
    df = pd.read_csv(filepath)
    time_series_plot(df)
