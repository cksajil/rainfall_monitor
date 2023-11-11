import numpy as np
from os.path import join
from scipy.io import wavfile
from keras.models import Sequential
from keras.layers import Dense, Input
from tensorflow.keras.regularizers import l2
from tensorflow.keras.initializers import RandomUniform

FOLDER = "./rain_dataset/rain_drop_data"
FILE_NAME = "2023_11_06_18_46_47_519974_36"
INFERENCE_DURATION = 0.2
TEST_FILE_DURATION = 0.2

file_path = join(FOLDER, FILE_NAME)
Fs, x = wavfile.read(file_path)
segment_len = int(INFERENCE_DURATION * Fs)
n_segments = int(TEST_FILE_DURATION / INFERENCE_DURATION)


def create_dnn_mini(in_shape):
    model = Sequential()
    model.add(Input(shape=in_shape))
    model.add(
        Dense(
            8,
            kernel_initializer=RandomUniform(minval=-0.05, maxval=0.05),
            kernel_regularizer=l2(0.001),
            activation="relu",
        )
    )
    model.add(
        Dense(
            32,
            kernel_initializer=RandomUniform(minval=-0.05, maxval=0.05),
            kernel_regularizer=l2(0.001),
            activation="relu",
        )
    )
    model.add(Dense(16, activation="relu", kernel_regularizer=l2(0.001)))
    model.add(
        Dense(
            5,
            kernel_initializer=RandomUniform(minval=-0.05, maxval=0.05),
            kernel_regularizer=l2(0.001),
            activation="softmax",
        )
    )

    model.compile(
        optimizer="Adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model


in_shape = (segment_len,)
model = create_dnn_mini(in_shape)
model.build(input_shape=in_shape)
model.load_weights("./model/dnn.hdf5")

drops_detected = 0
for i in range(n_segments):
    audio_segment = x[i * segment_len : i * segment_len + segment_len]
    audio_segment = audio_segment.reshape(1, -1)
    y_pred = model.predict(audio_segment)[0]
    print(y_pred)
    # indx = np.argmax(y_pred)
    # drops_detected += indx

# print(drops_detected)
