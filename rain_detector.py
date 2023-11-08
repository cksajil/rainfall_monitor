import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm
from os.path import join
from os import listdir
import tensorflow as tf
from keras.layers import Dense
import matplotlib.pyplot as plt
from keras.models import Sequential
from utils.helper import EarlyStopper
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.initializers import RandomUniform
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import train_test_split


RECORDING_DIR = "rain_dataset"
CLASSES = ["rain", "ambient"]
EPOCHS = 10
BATCH_SIZE = 16
SAMPLING_RATE = 48000
BIT_DEPTH = np.float32
SAMPLE_DURATION = 10
VALIDATION_SPLIT = 0.25
VALIDATION_LOSS_CUTOFF = 0.02
RESULT_COLS = ["Fs", "BIT_DEPTH", "MODEL", "TEST_ACCURACY", "TEST_LOSS"]

file_names = []
target = []

for label in CLASSES:
    fnames = listdir(join(RECORDING_DIR, label))
    num_samples = len(fnames)
    file_names.extend(fnames)
    target.extend([label] * num_samples)


result_df = pd.DataFrame(columns=RESULT_COLS)
basic_data = pd.DataFrame()
basic_data["filename"] = file_names
basic_data["class"] = target
basic_data["target"] = basic_data["class"].replace({"ambient": 0, "rain": 1})

spectrum_data = np.empty((0, SAMPLING_RATE * SAMPLE_DURATION), int)

for index, row in tqdm(basic_data.iterrows(), total=basic_data.shape[0]):
    file_path = join(RECORDING_DIR, row["class"], row["filename"])
    x, Fs = librosa.load(file_path, sr=SAMPLING_RATE, dtype=BIT_DEPTH)
    xfft = np.abs(np.fft.fft(x))
    spectrum_data = np.vstack([spectrum_data, xfft])

X_train, X_test, y_train, y_test = train_test_split(
    spectrum_data,
    basic_data["target"],
    test_size=VALIDATION_SPLIT,
    shuffle=True,
)


def create_dnn(in_shape):
    model = Sequential()
    model.add(Dense(32, activation="relu", input_shape=in_shape))
    model.add(Dense(64, activation="relu", input_shape=in_shape))
    model.add(
        Dense(
            128,
            kernel_initializer=RandomUniform(minval=-0.05, maxval=0.05),
            kernel_regularizer=l2(0.001),
            activation="relu",
        )
    )
    model.add(
        Dense(
            256,
            kernel_initializer=RandomUniform(minval=-0.05, maxval=0.05),
            kernel_regularizer=l2(0.001),
            activation="relu",
        )
    )
    model.add(
        Dense(
            512,
            kernel_initializer=RandomUniform(minval=-0.05, maxval=0.05),
            kernel_regularizer=l2(0.001),
            activation="relu",
        )
    )
    model.add(Dense(256, activation="relu", kernel_regularizer=l2(0.001)))
    model.add(Dense(128, activation="relu", kernel_regularizer=l2(0.001)))
    model.add(tf.keras.layers.Dropout(0.5))
    model.add(Dense(64, activation="relu", kernel_regularizer=l2(0.001)))
    model.add(
        Dense(
            2,
            kernel_initializer=RandomUniform(minval=-0.05, maxval=0.05),
            kernel_regularizer=l2(0.001),
            activation="softmax",
        )
    )

    model.compile(
        optimizer="Adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model


dnn_model = create_dnn(X_train[0].shape)


cp_callback = ModelCheckpoint(
    filepath="./model/dnn.hdf5",
    monitor="val_loss",
    verbose=1,
    save_best_only=True,
    mode="min",
)

early_stopper_cb = EarlyStopper(VALIDATION_LOSS_CUTOFF)

history = dnn_model.fit(
    X_train,
    y_train,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(X_test, y_test),
    callbacks=[cp_callback, early_stopper_cb],
)

test_loss, test_accuracy = dnn_model.evaluate(X_test, y_test, verbose=2)

result_data = pd.DataFrame(
    {
        "Fs": SAMPLING_RATE,
        "BIT_DEPTH": 32,
        "MODEL": "DNN",
        "TEST_ACCURACY": "{:5.2f}% ".format(100 * test_accuracy),
        "TEST_LOSS": test_loss,
    }
)


plt.plot(history.history["loss"])
plt.plot(history.history["val_loss"])
plt.xlabel("Epochs")
plt.ylabel("log Loss")
plt.legend(["train", "validation"], loc="upper right")
plt.show()

print(result_data)
