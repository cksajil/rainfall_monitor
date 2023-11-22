import librosa
import numpy as np
from os.path import join
from scipy.io import wavfile
from keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras.initializers import RandomUniform
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense


FOLDER = "./rain_dataset/rain_drop_data"
FILE_NAME = "2023_11_06_18_46_47_519974_36"
INFERENCE_DURATION = 0.2
TEST_FILE_DURATION = 0.2
SAMPLE_LENGTH = 9600
LEARNING_RATE = 0.001
N_CLASSES = 3
model_name = "./model/dnn.hdf5"


adamopt = Adam(learning_rate=LEARNING_RATE, beta_1=0.9, beta_2=0.999, epsilon=1e-8)


def create_cnn_model(in_shape):
    model = Sequential()
    model.add(
        Conv2D(
            8,
            kernel_size=(3, 3),
            activation="relu",
            input_shape=(in_shape[0], in_shape[1], 1),
        )
    )
    model.add(Conv2D(16, (2, 2), activation="relu"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(32, (3, 3), activation="relu"))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(16, (3, 3), activation="relu"))
    model.add(Flatten())
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
            N_CLASSES,
            kernel_initializer=RandomUniform(minval=-0.05, maxval=0.05),
            kernel_regularizer=l2(0.001),
            activation="softmax",
        )
    )

    model.compile(
        optimizer=adamopt, loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model


file_path = join(FOLDER, FILE_NAME)
Fs, x = wavfile.read(file_path)
x /= np.max(np.abs(x), axis=0)
x = x.reshape(1, -1)


dim = [1025, 19]


def create_cnn_data(raw_data):
    stft_data = np.empty(shape=[0, dim[0], dim[1]])
    for row in raw_data:
        Zxx = librosa.stft(row)
        stft_sample = np.abs(Zxx)
        stft_data = np.vstack([stft_data, stft_sample[np.newaxis, ...]])
    return stft_data


segment_len = int(INFERENCE_DURATION * Fs)
n_segments = int(TEST_FILE_DURATION / INFERENCE_DURATION)


spectrum_data = create_cnn_data(x)
in_shape = spectrum_data[0].shape
model = create_cnn_model(in_shape)
model.build(input_shape=in_shape)
model.load_weights("./model/dnn.hdf5")


y_pred = model.predict(spectrum_data)[0]
print(y_pred)
indx = np.argmax(y_pred)
print(indx)
