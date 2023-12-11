import datetime
import pandas as pd
from os.path import join
import matplotlib.pyplot as plt


def filter_by_time(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    start_time = datetime.datetime(2023, 12, 8, 17, 0, 0)
    end_time = datetime.datetime(2023, 12, 8, 22, 30, 0)
    row = (df["timestamp"] > start_time) & (df["timestamp"] < end_time)
    df = df[row]
    return df


def time_series_plot(df_1, df_2):
    plt.rcParams["figure.figsize"] = (12, 4)
    fig1, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    df_1 = filter_by_time(df_1)
    df_2 = filter_by_time(df_2)
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
    df_1 = load_csv("estimate_08_Dec_2023.csv")
    df_2 = load_csv("actual_08_Dec_2023.csv")
    time_series_plot(df_1, df_2)
