import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
from os.path import join

from numpy import pi as PI
import matplotlib.pyplot as plt
from keras.utils import Sequence
from keras.models import Sequential
from utils.helper import load_config

from sklearn.metrics import r2_score
from tensorflow.keras.optimizers import Adam
from keras.layers import Dense, LSTM, Reshape
from keras.layers import Conv2D, MaxPooling2D
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint
from cmsisdsp import arm_float_to_q15, arm_mult_q15, arm_rfft_q15
from cmsisdsp import (
    arm_cmplx_mag_q15,
    arm_rfft_instance_q15,
    arm_cos_f32,
    arm_rfft_init_q15,
)

config = load_config("config_ble.yaml", CONFIG_PATH="./config")
DATA_PATH = config["data_dir"]
BASIC_DATA_PATH = join(DATA_PATH, "data_basic.csv")
MODEL_NAME = config["model_name"]
LEARNING_RATE = config["learning_rate"]
Fs = config["sampling_rate"]
WINDOW_SIZE = config["window_size"]
STEP_SIZE = config["step_size"]
SEQ_LEN = config["seq_len"]
