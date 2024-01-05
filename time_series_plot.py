import datetime
import pandas as pd
from os.path import join
import matplotlib.pyplot as plt


def filter_by_time(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    start_time = datetime.datetime(2024, 1, 5, 2, 0, 0)
    end_time = datetime.datetime(2024, 1, 5, 10, 0, 0)
    row = (df["timestamp"] > start_time) & (df["timestamp"] < end_time)
    df = df[row]
    return df


def format_rainfall(rain_fall):
    rain_fall, unit = rain_fall.split(" ")
    if unit == "µm":
        rain_fall = float(rain_fall) / (10**3)
    elif unit == "mm":
        rain_fall = float(rain_fall)
    return rain_fall


def time_series_plot(df_1, df_2):
    plt.rcParams["figure.figsize"] = (12, 4)
    fig1, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    df_1 = filter_by_time(df_1)
    df_2 = filter_by_time(df_2)
    df_2["rainfall (mm)"] = df_2["rainfall (mm)"].apply(format_rainfall)
    ax1.plot(df_1["timestamp"], df_1["rainfall (mm)"], c="b", label="estimated")
    ax2.plot(df_2["timestamp"], df_2["rainfall (mm)"], c="k", label="mechanical")
    ax1.legend(loc="upper left")
    ax2.legend(loc="lower right")
    plt.xlabel("timestamp")
    plt.ylabel("rainfall (mm)")
    plt.legend()
    plt.show()


def load_csv(filename):
    filepath = join("rain_dataset", filename)
    df = pd.read_csv(filepath)
    return df


if __name__ == "__main__":
    df_1 = load_csv("estimated_05_Jan_2024.csv")
    df_2 = load_csv("actual_05_Jan_2024.csv")
    time_series_plot(df_1, df_2)
